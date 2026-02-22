from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Opportunity, Application, University
from accounts.models import StudentProfile
from .scraper import scrape_ivy_league
from django.contrib import messages

def university_dashboard(request):
    universities = University.objects.all()
    return render(request, 'opportunities/university_dashboard.html', {'universities': universities})

def university_detail(request, slug):
    university = get_object_or_404(University, slug=slug)
    opportunities = university.opportunities.all().order_by('-posted_date')
    opportunities = university.opportunities.all().order_by('-posted_date')
    return render(request, 'opportunities/university_detail.html', {
        'university': university,
        'opportunities': opportunities
    })

def opportunity_feed(request):
    
    domain_filter = request.GET.get('domain')
    univ_filter = request.GET.get('univ')
    
    opportunities = Opportunity.objects.filter(is_active=True).order_by('-posted_date')
    
    if domain_filter:
        opportunities = opportunities.filter(domain=domain_filter)
    if univ_filter:
        opportunities = opportunities.filter(university__name=univ_filter)
    
    # Recommendation logic: if user is logged in, prioritize their domain
    user_domain = None
    if request.user.is_authenticated:
        try:
            user_domain = request.user.profile.domain_interest
        except:
            pass
        
    universities = University.objects.all()
        
    return render(request, 'opportunities/feed.html', {
        'opportunities': opportunities,
        'user_domain': user_domain,
        'universities': universities
    })

@login_required
def apply_opportunity(request, pk):
    opportunity = get_object_or_404(Opportunity, pk=pk)
    Application.objects.get_or_create(student=request.user.profile, opportunity=opportunity)
    messages.success(request, f"Successfully applied to {opportunity.title}!")
    return redirect('opportunity_feed')

def refresh_opportunities(request):
    """
    Manually trigger the real-time scraper.
    """
    count = scrape_ivy_league()
    if count > 0:
        messages.success(request, f"Scraped {count} new real-time academic opportunities!")
    else:
        messages.info(request, "Feed is already up to date with official sources.")
    return redirect(request.META.get('HTTP_REFERER', 'opportunity_feed'))

def shortlist_candidates(request):
    """
    Smart shortlisting of top students for a specific academic domain.
    """
    domain = request.GET.get('domain', 'AI')
    top_candidates = StudentProfile.objects.filter(domain_interest=domain).order_by('-incoscore')[:10]
    return render(request, 'opportunities/shortlist.html', {
        'top_candidates': top_candidates,
        'domain': domain,
        'domain_display': dict(StudentProfile.DOMAIN_CHOICES).get(domain, domain)
    })
