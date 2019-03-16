""" Word API Data models

    For Django fc_coding_challenge - wordapi app.

    - This model exist for querying words, across lanaugages/dictionaries, via API.
    - The intended usecase of this model and API is to find word-matches to substring user-queries, and anagrams of those matching words.
    - Alphagrams are used here to assocate words in data that are anagrams to each other.
    - All words that are anagrams of one another will also share the same alphagram– the string resulting from sorting a word/string's letters/characters alphabetically.  https://en.wiktionary.org/wiki/alphagram

    Model overview:
    TODO

"""


import datetime

from django.db import models
from django.utils import timezone


#   Data Models
class WordLanguage(models.Model):
    """ WordLanguage is the dictionary language, associated with words by a many-to-one relationship. The name is cumbersome due to the vague nature of the word 'language'.
    """
    label = models.CharField(max_length=30, unique=True)
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.label

class Alphagram(models.Model):
    """ Alphagrams for association with words by a many to one relationship. Primarily used to find words' anagrams.
    """
    label = models.CharField(max_length=50, unique=True)
    
    def __str__(self):
        return self.label

class Word(models.Model):
    """ Words from dictionary list.
    """
    label = models.CharField(max_length=50) # Not unique. Other words (homographs) may have same spelling, but unique IDs.
    alphagram = models.ForeignKey(Alphagram, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.label