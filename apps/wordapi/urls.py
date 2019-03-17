""" URL routing for API - wordAPI
    
    API level routers and index path.
"""


from django.urls import include, path, re_path
from rest_framework import routers
from . import views


router = routers.DefaultRouter()
router.register(r'words', views.WordViewSet) # aliases? plural
router.register(r'languages', views.LanguageViewSet)
router.register(r'substring', views.WordViewSet) # matches # temporarily using word views. URL param filter needed
#router.register(r'words/sub', views.WordViewSet)
'''
router.register(r'anagram', views.WordViewSet)
router.register(r'substr_anagrams', views.WordViewSet)
'''


urlpatterns = [
    #path('api/test', views.LanguageViewSet),#re_path - testing for regexp for aliases, and staying off index list. +param (fine in router!)
    re_path(r'api/alphagrams/', views.AlphagramQuery.as_view(), name="alphagrams"),
    path('', views.index, name='index'),
    path('api/', include(router.urls)),
] # todo: 404

