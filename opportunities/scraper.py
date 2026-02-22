import requests
from bs4 import BeautifulSoup
from datetime import datetime
import re
from urllib.parse import urljoin
from .models import Opportunity, University
from .classifier import classify_opportunity
from django.utils import timezone
import json

# Banned keywords for UI noise, meta-elements, and navigation
UI_BANNED_KEYWORDS = [
    'share on facebook', 'share on linkedin', 'share on twitter', 
    'i\'m interested', 'i am interested', 'submission form', 
    'explore this portal', 'event submission', 'add to calendar',
    'follow us', 'newsletter', 'subscribe', 'copyright', 'all rights reserved',
    'skip to content', 'skip to events menu', 'submit an event', 'navigation',
    'search', 'menu', 'sidebar', 'footer', 'header', 'login', 'sign up',
    'all events', 'featured events', 'calendar', 'resources', 'department',
    'share', 'submit', 'emailer', 'places', 'groups', 'register'
]

def clean_text(text):
    if not text: return ""
    for noise in UI_BANNED_KEYWORDS:
        pattern = re.compile(re.escape(noise), re.IGNORECASE)
        text = pattern.sub("", text)
    text = " ".join(text.split())
    text = re.sub(r'^[,;:\s]+|[,;:\s]+$', '', text)
    return text.strip()

def normalize_title(title):
    if not title: return ""
    title = re.sub(r'(?:Mon|Tue|Wed|Thu|Fri|Sat|Sun),?\s+(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec).*$', '', title, flags=re.I).strip()
    words = title.split()
    normalized_words = []
    acronyms = ['AI', 'GIS', 'DNA', 'RNA', 'HIV', 'STEM', 'LPU', 'IVY', 'MIT', 'PhD', 'MBA', 'US', 'USA']
    for w in words:
        if w.upper() in acronyms:
            normalized_words.append(w.upper())
        else:
            normalized_words.append(w.capitalize())
    return " ".join(normalized_words)

class BaseScraper:
    def __init__(self, target, headers):
        self.target = target
        self.headers = headers
        self.univ_obj = University.objects.filter(name__icontains=target['univ']).first()

    def get_soup(self):
        try:
            response = requests.get(self.target['url'], headers=self.headers, timeout=15)
            if response.status_code == 200:
                return BeautifulSoup(response.content, 'html.parser')
            print(f"Fetch failed for {self.target['univ']} (Status {response.status_code})")
        except Exception as e:
            print(f"Error fetching {self.target['univ']}: {e}")
        return None

    def scrape(self):
        raise NotImplementedError

class JsonScraper(BaseScraper):
    """For sites like Brown that provide a JSON feed."""
    def scrape(self):
        try:
            response = requests.get(self.target['url'], headers=self.headers, timeout=15)
            if response.status_code != 200: return 0
            data = response.json()
            if not isinstance(data, list): data = data.get('events', [])
            
            print(f"Scraping JSON for {self.target['univ']} ({len(data)} items)")
            count = 0
            for item in data:
                try:
                    raw_title = item.get('title', '')
                    if not raw_title or len(raw_title) < 5: continue
                    
                    title = normalize_title(raw_title)
                    link = item.get('url') or item.get('link')
                    if not link: continue
                    
                    # Deduplication check
                    if Opportunity.objects.filter(title=title, university=self.univ_obj).exists():
                        continue

                    Opportunity.objects.create(
                        title=title,
                        university=self.univ_obj,
                        description=clean_text(item.get('summary', item.get('description', '')))[:500] or f"Featured event at {self.target['univ']}.",
                        domain=classify_opportunity(title.lower()),
                        link=link,
                        location=clean_text(item.get('location', ''))[:255],
                        event_date=item.get('date_dt', item.get('date', '')),
                        is_active=True
                    )
                    count += 1
                except: continue
            return count
        except Exception as e:
            print(f"JSON Error for {self.target['univ']}: {e}")
            return 0

class LocalistScraper(BaseScraper):
    def scrape(self):
        soup = self.get_soup()
        if not soup: return 0
        events = soup.select('.em-card, .event-card, .event_item, article, .event-list-item')
        if not events:
            events = soup.find_all(['li', 'div', 'article'], class_=re.compile(r'event|item|card', re.I))
            
        print(f"Scraping {self.target['univ']} ({len(events)} nodes)")
        count = 0
        seen_keys = set()
        for item in events:
            try:
                # Localist specific link patterns
                a_tag = item.select_one('h3 a, h4 a, .em-card_title a, a.event-link, .title a') or item.find('a', href=re.compile(r'/event/'))
                if not a_tag: continue
                
                raw_title = a_tag.get_text(" ", strip=True)
                if not raw_title or len(raw_title) < 5: continue
                
                title = normalize_title(raw_title)
                title_key = title.lower()
                if any(banned in title_key for banned in UI_BANNED_KEYWORDS): continue
                
                link = urljoin(self.target['url'], a_tag['href'])
                
                # Metadata
                date_str = ""
                date_tag = item.select_one('.em-card_date, .event-date, .date, .time, .when, .lw_event_date')
                if date_tag: date_str = clean_text(date_tag.get_text())
                
                location = ""
                loc_tag = item.select_one('.em-card_location, .event-location, .location, .where, .venue, .lw_event_location')
                if loc_tag: location = clean_text(loc_tag.get_text())
                
                desc_tag = item.select_one('.em-card_description, .description, .summary, p, .lw_event_description')
                description = clean_text(desc_tag.get_text()) if desc_tag else ""
                
                unique_key = f"{title_key}|{date_str}|{self.target['univ']}"
                if unique_key in seen_keys: continue
                seen_keys.add(unique_key)
                
                if Opportunity.objects.filter(title=title, university=self.univ_obj).exists():
                    continue

                Opportunity.objects.create(
                    title=title,
                    university=self.univ_obj,
                    description=description or f"Featured event at {self.target['univ']}.",
                    domain=classify_opportunity(title_key + " " + description),
                    link=link,
                    location=location[:255],
                    event_date=date_str[:100],
                    is_active=True
                )
                count += 1
            except: continue
        return count

class CustomScraper(BaseScraper):
    def scrape(self):
        soup = self.get_soup()
        if not soup: return 0
        
        count = 0
        # More aggressive link finding for Penn and others
        event_links = soup.find_all('a', href=re.compile(r'/event|/calendar|upenn\.edu|harvard\.edu'))
        print(f"Scraping {self.target['univ']} ({len(event_links)} links)")
        
        seen_links = set()
        for a_tag in event_links:
            try:
                raw_title = a_tag.get_text(" ", strip=True)
                # Filter out short menu items but keep potential event titles
                if not raw_title or len(raw_title) < 10 or len(raw_title) > 200: continue
                
                title = normalize_title(raw_title)
                title_key = title.lower()
                if any(banned in title_key for banned in UI_BANNED_KEYWORDS): continue
                
                link = urljoin(self.target['url'], a_tag['href'])
                if link in seen_links: continue
                seen_links.add(link)
                
                parent = a_tag.find_parent(['div', 'li', 'article', 'section']) or a_tag.parent
                block_text = parent.get_text(" ", strip=True)
                
                if Opportunity.objects.filter(title=title, university=self.univ_obj).exists():
                    continue

                Opportunity.objects.create(
                    title=title,
                    university=self.univ_obj,
                    description=clean_text(block_text.replace(raw_title, ""))[:500] or "University featured event.",
                    domain=classify_opportunity(title_key),
                    link=link,
                    is_active=True
                )
                count += 1
            except: continue
        return count

def scrape_ivy_league():
    # Optimizing targets for better accessibility
    targets = [
        {"univ": "Harvard University", "url": "https://www.harvard.edu/events/", "strategy": "custom"},
        {"univ": "Yale University", "url": "https://events.yale.edu/", "strategy": "localist"},
        {"univ": "Cornell University", "url": "https://events.cornell.edu/", "strategy": "localist"},
        {"univ": "Princeton University", "url": "https://www.princeton.edu/events", "strategy": "custom"},
        {"univ": "Brown University", "url": "https://events.brown.edu/live/json/events/", "strategy": "json"},
        {"univ": "Columbia University", "url": "https://www.columbia.edu/", "strategy": "custom"}, # Try main page for links
        {"univ": "University of Pennsylvania", "url": "https://penntoday.upenn.edu/events", "strategy": "custom"},
        {"univ": "Dartmouth College", "url": "https://home.dartmouth.edu/events", "strategy": "custom"}, # Different source
    ]

    total_new = 0
    # Use a more modern User-Agent to bypass some bot checks
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36'}

    for target in targets:
        print(f"--- Processing {target['univ']} ---")
        strategy_name = target.get('strategy', 'custom')
        
        try:
            if strategy_name == 'localist':
                scraper = LocalistScraper(target, headers)
            elif strategy_name == 'json':
                scraper = JsonScraper(target, headers)
            else:
                scraper = CustomScraper(target, headers)
                
            total_new += scraper.scrape()
        except Exception as e:
            print(f"Critical error on {target['univ']}: {e}")
            
    return total_new
