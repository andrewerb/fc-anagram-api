""" Dictionary-Word/Anagram API - Data Serializers

    - Seriealizers extend Django Rest Framework serializers classes
    - Serializers create JSON http-responses from data-queries in views.py
    - Serializers exist by model type, to handle that model's attributes accordingly. More than one can be made as needed by API views. 
    - Fields specify what attributes/data-tables go into JSON responses in API.
"""


from rest_framework import serializers
from .models import *


class WordSerializer(serializers.ModelSerializer): # check type, ID/label # HyperlinkedModelSerializer
    """ Word serializer - the most used for this app
    """
    class Meta:
        model = Word
        fields = ('id', 'label')
        # TODO: Display related language?


class LanguageSerializer(serializers.ModelSerializer):
    """ Languages Serializer
    """
    class Meta:
        model = WordLanguage
        fields = ('url', 'label')


class AlphaSerializer(serializers.ModelSerializer):
    """ Alphagram serializer, for testing. Not in API.
    """
    class Meta:
        model = Alphagram
        fields = ('id', 'label')
