""" Word API Views
"""


import datetime

from django.http import Http404
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render

from rest_framework import viewsets
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

from .serializers import * #UserSerializer, GroupSerializer
from .models import *


class WordViewSet(viewsets.ModelViewSet):
    """ API endpoint that allows words to be viewed or edited. # TODO!
    """
    queryset = Word.objects.all().order_by('label')
    serializer_class = WordSerializer


class AlphagramQuery(APIView):
    """ Returns a list of all alphagrams
    """
    def get(self, request, format=None):
        alpha_set = Alphagram.objects.all()
        serializer = AlphaSerializer(alpha_set, many=True)
        return Response(serializer.data)


class LanguageViewSet(viewsets.ModelViewSet):
    """ API endpoint that allows WordLanguages to be viewed or edited. # TODO!
    """
    queryset = WordLanguage.objects.all()
    serializer_class = LanguageSerializer
    

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
