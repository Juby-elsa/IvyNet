from opportunities.models import Opportunity

# Aggressive blacklist for title-based purging
strict_blacklist = [
    'department', 'resources', 'calendar', 'all events', 'featured events', 
    'places', 'groups', 'emailer', 'login', 'share on', "i'm interested",
    'submission form', 'navigation', 'menu', 'footer', 'header', 'explore',
    'university', 'institute', 'news', 'portal', 'customized', 'planning',
    'view', 'search', 'home'
]

# We are looking for things that are JUST the department name or resources
opportunities = Opportunity.objects.all()
delete_count = 0

for opp in opportunities:
    title_lower = opp.title.lower()
    # If the title IS exactly a banned word (like "Music Department") or contains it in a noisy way
    if any(banned in title_lower for banned in strict_blacklist):
        opp.delete()
        delete_count += 1

print(f"Aggressively purged {delete_count} noisy opportunities from the database.")
