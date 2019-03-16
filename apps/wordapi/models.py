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
    - ORDER BY
    - created_date

"""


import datetime

from django.db import models
from django.utils import timezone


##  Data Models  ##
class WordLanguage(models.Model):
    """ Language, for words and dictionary entries.
    
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
    Referenced by words as many-to-one relationship. Used to find words' anagrams. Unique by label; redundancy would make this useless as an anagram-key.

    Attributes: label
    """

    label = models.CharField(max_length=50, unique=True)
    
    def __str__(self):
        return self.label

    class Meta:
        ordering = ['label']


class Word(models.Model): #### ORDER_BY
    """ Words from dictionary list.

    Attributes: label, language, alphagrams
    """

    # Labels are not unique, because other words in DB (homographs) may have same spelling w/ unique IDs.
    label = models.CharField(max_length=50) 
    language = models.ForeignKey(WordLanguage, blank=True, null=True, on_delete=models.CASCADE) # TODO: Required
    alphagram = models.ForeignKey(Alphagram, on_delete=models.CASCADE)
    
    # homograph_count = models.IntegerField(default=0) # use if able to initialize.
    # is_palindrome = models.BooleanField(default=False)
    
    def __str__(self):
        return self.label
    
    def save(self, *args, **kwargs):
        """ Save overrides, for setting up attribute-fields from the word's label.
        
        Attributes checked here: label-lowercasing, alphagram object
        TODO: Add Homograph count and efault language if there's only one. Make more abstract?
        """
        # Enforcing lowercase in database, for uniformity
        self.label = self.label.lower()
        print("word-label is: " + self.label + "  -- SAVED!")

        #homograph
        #language

        ## Alphagram setup ##
        # Find alphagram (sorted label)
        alpha_str = "".join( sorted(list(self.label)) )
        
        if Alphagram.objects.filter(label=alpha_str).exists():
            # If alphagram is in data, set it as foreign key.
            self.alphagram = Alphagram.objects.get(label=alpha_str)
        else:
            # Create alphagram object, save it, and set it as foreign key.
            new_alpha = Alphagram()
            new_alpha.label = alpha_str
            new_alpha.save()
            self.alphagram = new_alpha

        super(Word, self).save(*args, **kwargs)

    class Meta:
        ordering = ['label']
    ## Sort by
    
    #if getattr(self, '_image_changed', True):
    
    ## save homograph - ?


class WordDefinition(models.Model):
    """ Dictionary definition. Usable for multiple definition entries, classed by language. Possibly in need of extending.
        
    Has many-to-one relationships with Language (of the definition), and with Word (which the definiton is for). Definition and word can be different languages.
    
    Attributes:
        label, detail, word, language
    """
    label = models.CharField(max_length=30, blank = False)
    detail = models.TextField(blank=False)
    word = models.ForeignKey(Word, blank=False, null=False, on_delete=models.CASCADE)
    language = models.ForeignKey(WordLanguage, blank=False, null=False, on_delete=models.CASCADE)

    def __str__(self):
        return self.label
