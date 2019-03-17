""" FC Coding Challenge project - config URL routing

    - Routing for base level of project.
    - Routes at this level are minimal.
    - URL Routing for this project is primarily handled in apps.wordapi.urls, for API layer routing.
    - More routes could be supported if this project were extended or had additional apps.
"""


from django.contrib import admin
from django.urls import include, path, re_path


urlpatterns = [
    re_path(r'^', include('apps.wordapi.urls')), # Default index-path is to API
    path('admin/', admin.site.urls),
]
