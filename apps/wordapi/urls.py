""" Dictionary-Words / Anagram API app - URL Routing

    API level routers and index path.

    # TODO: move API/ directory path routing back to project config's urls.py
"""


from django.urls import include, path, re_path
from rest_framework import routers
from . import views


# Django Rest Framework routing for API defaults - publicly visible at API index:
router = routers.DefaultRouter()
router.register(r'words', views.WordViewSet)
router.register(r'languages', views.LanguageViewSet)
# For testing - dump of alphagrams in model:
router.register(r'alphagrams', views.AlphagramViewSet)


urlpatterns = [
    ##################
    ##  API routes  ##
    ##################
    # substring routes - Words containing substring
    # ex: /api/substrings/foo
    re_path(r'^api/substrings?\/$', views.WordBySubstringView.as_view(), name="substrings"),
    re_path(r'^api/substrings?\/(?P<substr_input>.+)/$', views.WordBySubstringView.as_view(), name="substrings"),
    
    # anagram API routes - anagrams for words by label
    # ex: /api/anagrams/listen
    re_path(r'^api/anagrams?\/$', views.AnagramView.as_view(), name="anagrams"),
    re_path(r'^api/anagrams?\/(?P<label_input>.+)/$', views.AnagramView.as_view(), name="anagrams"),
    
    # Substring Anagram API routes - Anagrams of words containing queried substring, sorted by 2nd character
    # ex: /api/substringanagrams/foo
    re_path(r'^api/substringanagrams?\/$', views.AnagramBySubstringView.as_view(), name="anagrams_by_substring"), 
    re_path(r'^api/substringanagrams?\/(?P<substr_input>.+)/$', views.AnagramBySubstringView.as_view(), name="anagrams_by_substring"),
    

    ####################
    ##  Non-API paths ##
    ####################
    path('', views.index, name='index'), ## TODO: Move up to base and point to app views and templates. Drop 'API/' everywhere.
    path('api/', include(router.urls)),
]
