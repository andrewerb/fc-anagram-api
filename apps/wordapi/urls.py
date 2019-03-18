""" URL routing for API - wordAPI
    
    API level routers and index path.

    TODO: 
        Backup 'api/' path to config URLs; and move templates?
        Elaborate on paths & routing
        Fix a lot of routes
"""


from django.urls import include, path, re_path
from rest_framework import routers
from . import views


# Django Rest routing for API - publicly visible at API index:
router = routers.DefaultRouter()
router.register(r'words', views.WordViewSet) # aliases? plural
router.register(r'languages', views.LanguageViewSet)
# TODO: stub None view for redundancy - substrings, anagrams, anagramsbysubstring, None / 404
# TODO: singular wording for redundancy

# router.register(r'substring', views.WordViewSet)
# router.register(r'words', views.WordViewSet)


urlpatterns = [
    
    # ex: /api/substrings/foo
    re_path(r'^api/substrings?\/(?P<search_id>.+)/$', views.WordBySubstringView.as_view(), name="substrings"),
    re_path(r'api/anagrams?\/', views.AnagramView.as_view(), name="anagrams"),
    # router.register(r'substr_anagrams', views.WordViewSet)  #  TODO!
    # TODO: word router by label
    

    # For testing:
    re_path(r'api/alphagrams?\/', views.AlphagramView.as_view(), name="alphagrams"),
    
    # Non-API paths:
    path('', views.index, name='index'), ## TODO: Move up to base and point to app views and templates. Drop 'API/' everywhere.
    path('api/', include(router.urls)),
]
