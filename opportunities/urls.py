from django.urls import path
from . import views

urlpatterns = [
    path('feed/', views.opportunity_feed, name='opportunity_feed'),
    path('universities/', views.university_dashboard, name='university_dashboard'),
    path('university/<slug:slug>/', views.university_detail, name='university_detail'),
    path('apply/<int:pk>/', views.apply_opportunity, name='apply_opportunity'),
    path('refresh/', views.refresh_opportunities, name='refresh_opportunities'),
    path('shortlist/', views.shortlist_candidates, name='shortlist'),
]
