""" Dictionary-Words / Anagram API app Views

    API endpoints only have GET methods in this app iteration, no additional HTTP request methods.

    API Views:
    words, languages, words by substring (containing input) match, anagrams, anagrams by substring

    This file also includes a customized 404 response "None" for empty queries, and a view for the web index page
"""


import datetime, re

from django.http import Http404
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render

from rest_framework import viewsets
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

from .serializers import *
from .models import *


#############################################
##  BEHAVIORAL ABSTRACTIONS FOR API VIEWS  ##
#############################################
def response_404_none():
    """ Return "None" and 404 status code
        For GET requests from API endpoints, where/when queries yield no result
    """
    return Response("None", status=status.HTTP_404_NOT_FOUND)

class ValidParamView():
    def response_404_none(self):
        """ Return "None" and 404 status code
            For GET requests from API endpoints, where/when queries yield no result
        """
        return Response("None", status=status.HTTP_404_NOT_FOUND)

    def has_numbers(self, inputString=""):
        return bool(re.search(r'\d', inputString))

    def valid_param(self, param_str=""):
        """ Boolean
        """
        if not param_str:
            return False #return self.__response_404_none()

        elif self.has_numbers(param_str):
            return False

        else:
            return True

    def long_valid_param(self, param_str="", param_len=2):
        """ Return 404 response if query parameter is too short or isn't valid

            This is a hack for not processing very short queries on the DB, primarily for anagrams by substring.
            NOTE: An expanded build would ideally encorpoate API views to a data model to handle shorter substring queries.
        """
        if len(param_str) < param_len:
            return False
        else:
            return self.valid_param



#################
##  API Views  ##
#################
class WordBySubstringView(ValidParamView, APIView):
    """ API view for Get word matching query-substring
    """
    def get(self, request, format=None, substr_input=""):
        """ API's GET method, for substring-input

            Queries Word model (dictionary words) for set of Words for which input is a substring.
        """
        if self.valid_param(substr_input):
            # Validate query param
            try:
                # Query filtering for case-insentive containment of the input-string (as a substring) in Word entry labels
                queryset = Word.objects.filter(label__icontains=substr_input)
                print(str(queryset))
                if not queryset:
                    return self.response_404_none()
                else:
                    # Continue if queryset found
                    serializer = WordSerializer(queryset, many=True)
                    return Response(serializer.data)
            except:
                # 404/"None" if no results
                return self.response_404_none()

        else:
            # 404 if empty or invalid param
            return self.response_404_none()


class AnagramView(APIView): # TODO - URL param
    """ Anagram fetching by Subject-Word label
        
        Queries alphagram of subject-word, filters for words associated, and returns that list sans the subject-word.
        Returns a set of Word objects
    """
    def get(self, request, format=None, label_input=""): ## TODO!!! TAKE PARAM FROM URL ROUTER

        # TODO: regexp check for alpha chars useful here
        #label_input = "listen" # TODO - UPDATE!!! PARAMS, for non-exist - try, or filter; combine/join!!
        
        if label_input: 
            # If input isn't empty
            try:
                subject_word = Word.objects.get(label=label_input) # Check for subject-word
            except:
                # Subject word doesn't exist. No anagrams. Return none.
                return response_404_none()
            
            # If subject-word object was found
            queryset = subject_word.alphagram.word_set.all().exclude(id=subject_word.id)  # The anagram queryset is the set of words sharing the same alphagram as the subject-word, excluding the subject-word itself.
            
            if queryset.count():
                serializer = WordSerializer(queryset, many=True)
                return Response(serializer.data)

            # TODO: params, combine/join
        
        return response_404_none()


class AnagramBySubstringView(APIView): # TODO - less copy pasta?
    def get(self, request, format=None, substr_input=""):
        if not substr_input:
            # 404 if the search query is empty
            return response_404_none()
        else:
            # substr_input isn't empty

            subject_word_set = Word.objects.filter(label__icontains=substr_input) # Queryset of words containing input-string as a substring. Used as subject-words for anagram fetching.
            
            if subject_word_set.count():
                # Proceed with anagram search if subject words were found.

                anagram_set = [] # list for anagrams

                # Nested iterator for anagrams of all subject-words (substring-matches) into anagram list:
                for subject in subject_word_set:
                    # Iterate every subject-word in queryset
                    anagrams = subject.alphagram.word_set.all().exclude(id=subject.id) # Set of anagrams of the current subject-word (excluding the subject word itself)
                    for ana in anagrams: # Iterate current set of anagrams
                        print ("Currently viewing:  " + ana.label) # Testing
                        if not ana in anagram_set: # Add to anagram_set if it's not already in the list
                            anagram_set.append(ana)
                            print("Appended to list!") # Testing
                
                if anagram_set:
                    # Anagram set isn't empty
                    anagram_set = sorted(anagram_set, key=lambda x: x.label[1:], reverse=False)[:10] # First 10 items of set of results, after sorting by their 2nd character
                    serializer = WordSerializer(anagram_set, many=True)
                    return Response(serializer.data)
                else:
                    return response_404_none() # 404 - None if set was empty
            
            else:
                return response_404_none()

#############################
##  Default API View Sets  ##
#############################
# Django Rest Framework boilerplate for Model API views
# Useful, but non-essential to this API
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


class AlphagramViewSet(viewsets.ModelViewSet):
    """ API endpoint that allows Alphagrams to be viewed or edited. # TODO!
    """
    queryset = Alphagram.objects.all()
    serializer_class = LanguageSerializer


###########################
##  Web Views (non-API)  ##
###########################
def index(request):
    return HttpResponse( ## TODO: view index, jinja, css
        "<p>Word API Views index </p><br />" +
        "<h3>Words: " + str( Word.objects.count() ) + "</h3> "+
        # s+"<br / >"+
        "<p><a href='/api/'>API</a></p>"
        )
