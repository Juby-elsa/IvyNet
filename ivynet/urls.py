from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from opportunities.views import opportunity_feed

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', opportunity_feed, name='home'),
    path('accounts/', include('accounts.urls')),
    path('opportunities/', include('opportunities.urls')),
    path('community/', include('community.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
