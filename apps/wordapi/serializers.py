""" Django Rest Framework Serializers for Word API
"""

#from django.contrib.auth.models import User, Group
from rest_framework import serializers
from .models import *


class WordSerializer(serializers.HyperlinkedModelSerializer): # check type, ID/label
    class Meta:
        model = Word
        fields = ('url', 'id', 'label') # language-label, or print that ull object

class AlphaSerializer(serializers.ModelSerializer): # ALPHAGRAM serializer - WIP 
    class Meta:
        model = Alphagram
        fields = ('id', 'label')#no url

class LanguageSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = WordLanguage
        fields = ('url', 'label')
