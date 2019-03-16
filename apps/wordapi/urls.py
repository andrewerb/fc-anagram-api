""" wordsapi urls.py
    The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.urls import path, re_path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    ## more patterns and routes for API
]
    # Index: basics. Server is live. Dev or Prod
    # Langages: 1 and list.
    # Words: None
    ## For each language, print lang then word count

    # path not found is 404
    ## For all: if language, use that. Else, nah.
    ##### IF QUERY IS AN ISSUE, DUMP LANGUAGE FROM THE PATH
    # language/word/ ... none = None, else that word(dict later)
    # language/substring/ ... None, else matching word search (substring)
    ### SHOULD WE USE LANGUAGE PATH AT ALL??? (No? Keep in model though...)
    ## If queryset none...
    ## hard coded nested path would limit input
    # language/substring-anagram/ ...
    ## language/substring/anagram/

    # language will give word count OR 404



    #### queries: substring, is many-to-one of substring's alphagram. Is English...