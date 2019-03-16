""" Word API Data models

    For Django fc_coding_challenge - wordapi app.

    - This model exist for dictionaries of words, across lanaugages/dictionaries, to be quieried by an API
    - This model and API is for finding substring matches to a word in data, 
    - All words that are anagrams of one another will also share the same alphagram– the resulting string from sorting a word/string's letters/characters alphabetically.  https://en.wiktionary.org/wiki/alphagram
    - Alphagrams are used here to assocate words in data that are anagrams.

    Model overview:

"""


import datetime

from django.db import models
from django.utils import timezone


#   Data Models
class WordLanguage(models.Model):
    label = models.CharField(max_length=30, unique=True)
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.label

class Alphagram(models.Model):
    label = models.CharField(max_length=50, unique=True)
    
    def __str__(self):
        return self.label

class Word(models.Model):
    label = models.CharField(max_length=50) # Not unique. Other words (homographs) may have same spelling, but unique IDs.
    alphagram = models.ForeignKey(Alphagram, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.label