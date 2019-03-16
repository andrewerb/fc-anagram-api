""" Word API Data models

For Django fc_coding_challenge - wordapi app.

- This model exist for querying words, across lanaugages/dictionaries, via API.
- The intended usecase of this model and API is to find word-matches to substring user-queries, and anagrams of those matching words.
- Alphagrams are used here to assocate words in data that are anagrams to each other.
- All words that are anagrams of one another will also share the same alphagram– the string resulting from sorting a word/string's letters/characters alphabetically.  https://en.wiktionary.org/wiki/alphagram

Models:
    WordLanguage
    Alphagram
    Word
    WordDefinition : Not really used at this point, but available.

TODO: 
    - SAVE override methods for anagrams!
    - ORDER BY
    - label - string to lower (even if handled elsewhere)
    - created_date

"""


import datetime

from django.db import models
from django.utils import timezone


#   Data Models
class WordLanguage(models.Model):
    """ Language of words and dictionary entries.
    
    Associated with words by a many-to-one relationship. The name is cumbersome due to the vague nature of the word 'language'.

    Attributes:
        label, creeated_date
    """
    label = models.CharField(max_length=30, unique=True)
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.label
    ## TODO: META, sort, SAVE
    ## SORT

class Alphagram(models.Model):
    """ Alphagram - alphabetically sorted string/word.

    For association with words by a many to one relationship. Primarily used to find words' anagrams.

    Note: Alphagrams have no language attribute, and are language agnostic. (Because words across languages can be anagrams. That can be specified in a query filter.)

    Attributes:
        label
    """

    label = models.CharField(max_length=50, unique=True)
    
    def __str__(self):
        return self.label

class Word(models.Model): #### ORDER_BY
    """ Words from dictionary list.

    label, language, alphagrams
    """

    label = models.CharField(max_length=50) # Not unique. Other words (homographs) may have same spelling, but unique IDs.
    language = models.ForeignKey(WordLanguage, blank=True, null=True, on_delete=models.CASCADE) # make required
    alphagram = models.ForeignKey(Alphagram, on_delete=models.CASCADE)
    # homograph_count = models.IntegerField(default=0) # use if able to initialize. Reference by lookup.
    # is_palindrome = models.BooleanField(default=False)
    
    def __str__(self):
        return self.label
    
    def save(self, *args, **kwargs):
        # Enforcing lowercase in database, for uniformity
        self.label = self.label.lower()
        print("word-label is: " + self.label + "  -- SAVED!")

        # Find alphagram (sorted label)
        alpha_str = "".join( sorted(list(self.label)) )
        
        if Alphagram.objects.filter(label=alpha_str).exists():
            self.alphagram = Alphagram.objects.get(label=alpha_str)
        else:
            new_alpha = Alphagram()
            new_alpha.label = alpha_str
            new_alpha.save()
            self.alphagram = new_alpha

        super(Word, self).save(*args, **kwargs)

class WordDefinition(models.Model):
    """ Dictionary definition. Usable for multiple definition entries, classed by language. Possibly in need of extending.
        
    Has many-to-one relationships with Language of the definition, and with the Word the definiton is for. (Definition and language can theoretically be different languages).
    
    Attributes:
        label, detail, word, language
    """
    label = models.CharField(max_length=30, blank = False)
    detail = models.TextField(blank=False)
    word = models.ForeignKey(Word, blank=False, null=False, on_delete=models.CASCADE)
    language = models.ForeignKey(WordLanguage, blank=False, null=False, on_delete=models.CASCADE)

    def __str__(self):
        return self.label