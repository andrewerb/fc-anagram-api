""" Dictionary-Words / Anagram API app Views

    API endpoints only have GET methods in this app iteration, no additional HTTP request methods.
"""


import datetime

from django.http import Http404
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render

from rest_framework import viewsets
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

from .serializers import *
from .models import *


def response_404_none():
    """ Return "None" and 404 status code
        For GET requests from API endpoints, where/when queries yield no result
    """
    return Response("None", status=status.HTTP_404_NOT_FOUND)


##  API Views  ##
class WordViewSet(viewsets.ModelViewSet):
    """ API endpoint for dictionary words
    """
    queryset = Word.objects.all().order_by('label')
    serializer_class = WordSerializer


class LanguageViewSet(viewsets.ModelViewSet):
    """ API endpoint that allows WordLanguages to be viewed or edited. # TODO!
    """
    queryset = WordLanguage.objects.all()
    serializer_class = LanguageSerializer


# Words Bylabel


class WordBySubstringView(APIView):
    def get(self, request, format=None, search_id=""):
        """ API's GET method, for substring-input

            Queries Word model (dictionary words) for set of Words for which input is a substring.
        """
        substr_input = search_id
        
        try:
            # Query filtering for case-insentive containment of the input-string (as a substring) in Word entry labels
            queryset = Word.objects.filter(label__icontains=substr_input)
        except:
            # 404/"None" if no results
            return response_404_none()

        # Continue if queryset found
        serializer = WordSerializer(queryset, many=True)
        return Response(serializer.data)


class AnagramView(APIView): # TODO - URL param
    """ Anagram fetching by Subject-Word label
        
        Queries alphagram of subject-word, filters for words associated, and returns that list sans the subject-word.
        Returns a set of Word objects
    """
    def get(self, request, format=None): ## TODO!!! TAKE PARAM FROM URL ROUTER

        # TODO: regexp check for alpha chars useful here
        label_input = "listen" # TODO - UPDATE!!! PARAMS, for non-exist - try, or filter; combine/join!!
        
        if label_input: # If input isn't blank
            try:
                subject_word = Word.objects.get(label=label_input) # Check for subject-word
            except:
                # Subject word doesn't exist. No anagrams. Return none.
                return response_404_none()
            
            # If subject-word object was found
            queryset = subject_word.alphagram.word_set.all().exclude(id=subject_word.id)  # The anagram queryset is the set of words sharing the same alphagram as the subject-word, excluding the subject-word itself.
            
            serializer = WordSerializer(queryset, many=True)
            return Response(serializer.data)

            # TODO: params, combine/join
        else:
            return Response("None") ## 404!!

class AnagramBySubstringView(APIView): # TODO
    def get(self, request, format=None):
        pass
        ## 1st: regular anagra - query params
        ## test random or appended list

class AlphagramView(APIView): # TODO: Fix 404
    """ Returns a list of all alphagrams

        TODO: FIX THIS A LOT! - errors?
    """
    def get(self, request, format=None):
        queryset = Alphagram.objects.all()
        serializer = AlphaSerializer(queryset, many=True)
        return Response(serializer.data)


####################################        
##  Web Views (non-API)  ##
def index(request):
    #word_list = Word.objects.all()
    all_words = []
    for w in Word.objects.order_by('label'):
        all_words.append(str(w) )
    s = ", ".join(all_words)

    return HttpResponse( ## TODO: view index, jinja, css
        "<p>Word API Views index </p><br />" +
        "<h3>Words: " + str( Word.objects.count() ) + "</h3> "+
        s+"<br / >"+
        "<p><a href='/api/'>API</a></p>"
        )
