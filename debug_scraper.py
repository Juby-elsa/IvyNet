import requests
from bs4 import BeautifulSoup
import re

urls = [
    "https://events.brown.edu/",
    "https://events.dartmouth.edu/",
    "https://events.columbia.edu/",
    "https://penntoday.upenn.edu/events"
]
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36'}

for url in urls:
    print(f"\n--- SCRAPING: {url} ---")
    try:
        response = requests.get(url, headers=headers, timeout=15)
        print(f"Status: {response.status_code}")
        if response.status_code != 200: continue
        
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # 1. Look for identifying classes that often contain events
        classes = set()
        for tag in soup.find_all(class_=True):
            for c in tag['class']:
                if any(k in c.lower() for k in ['event', 'item', 'card', 'listing']):
                    classes.add(c)
        
        print(f"Interesting classes found: {list(classes)[:15]}")
        
        # 2. Look for links that might be events
        links = soup.find_all('a', href=re.compile(r'/event|/calendar', re.I))
        print(f"Potential event links found: {len(links)}")
        for l in links[:5]:
            print(f"  LINK: {l.get_text(strip=True)[:50]} -> {l['href']}")
            
        # 3. Check for LiveWhale or Localist signatures
        if soup.find(class_=re.compile(r'lw_')): print("SIGNATURE: LiveWhale detected")
        if soup.find(class_=re.compile(r'em-card|event-card')): print("SIGNATURE: Localist (em-card) detected")

    except Exception as e:
        print(f"Error: {e}")
