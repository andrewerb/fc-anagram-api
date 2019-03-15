"""FC Coding Challenge project URL Configuration
"""
from django.contrib import admin
from django.urls import include, path, re_path


urlpatterns = [
    # Project URL routes are minimal
    # URL Routing is primarily handled by the wordapi app's urls.py, for API layer routing.
    # ( More routes could be supported if this project were extended, in theory. )
    re_path(r'^', include('apps.wordapi.urls')), # Default path is to API
    path('admin/', admin.site.urls),
]
