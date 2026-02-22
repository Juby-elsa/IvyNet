from django.urls import path
from . import views

urlpatterns = [
    path('feed/', views.community_feed, name='community_feed'),
    path('post/create/', views.create_post, name='create_post'),
    path('post/<int:pk>/like/', views.like_post, name='like_post'),
    path('post/<int:pk>/comment/', views.add_comment, name='add_comment'),
]
