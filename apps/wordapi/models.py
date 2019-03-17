""" Word API Data models

For Django FC_coding_challenge - wordapi app.

- This model exist for querying words, across lanaugages/dictionaries, via API.
- The intended usecase of this model and API is to find word-matches for which user-submitted queries are a substring, and anagrams of those matching subject-words.
- Anagrams are recombinations of the order of letters (preserving the same count) of a subject-word, into another word.
- All words that are anagrams of one another will also share the same alphagram– the string resulting from sorting a word/string's letters/characters alphabetically.  https://en.wiktionary.org/wiki/alphagram
- Alphagrams are used here to assocate words in data that are anagrams to each other. Views can query the alphagram of a subject-word to get other words with that alphagram, which are the subject-word's anagrams.

Models:
    WordLanguage
    Alphagram
    Word
    WordDefinition : Not really used at this point, but available.

TODO: 
    - ORDER BY
    - created_date
    - FIX EDITABLE VALUES - date, anagram etc
    - Deletion!
    - Subtract result list from anagram list before sort.
    - Append dict

"""


import datetime

from django.db import models
from django.utils import timezone


##  Data Models  ##
class WordLanguage(models.Model):
    """ Language, for words and dictionary entries.
    
    Associated with words by a many-to-one relationship. The name is cumbersome due to the vague nature of the word 'language'. Unique, by label.
    """

    ##  Attributes  ##
    label = models.CharField(max_length=30, unique=True)

    ##  Non-editable attributes  ##
    created_at = models.DateTimeField(auto_now_add=True, editable=False)

    def __str__(self):
        return self.label
    ## TODO: META, sort, SAVE
    ## SORT


class Alphagram(models.Model):
    """ Alphagram - alphabetically sorted string/word. 
    Referenced by words as many-to-one relationship. Used to find words' anagrams. Unique by label; redundancy would make this useless as an anagram-key.
    """

    ##  Attributes  ##
    label = models.CharField(max_length=50, unique=True)

    ##  Non-editable attributes  ##
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.label

    class Meta:
        ordering = ['label']


class Word(models.Model): #### ORDER_BY
    """ Words (singular entries) from dictionary list.
    """

    ##  Attributes  ## 
    label = models.CharField(max_length=50)  # Labels are not unique, because other words in DB (homographs) may have same spelling w/ unique IDs.
    language = models.ForeignKey(WordLanguage, blank=True, null=True, on_delete=models.CASCADE)

    ##  Non-editable attributes  ##
    alphagram = models.ForeignKey(Alphagram, editable=False, on_delete=models.CASCADE)
    is_palindrome = models.BooleanField(default=False, editable=False)
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    
    #TODO: homograph_count = models.IntegerField(default=0) # use if able to initialize (would require updating other words with same label).
    
    def __str__(self):
        return self.label
    
    def save(self, *args, **kwargs):
        """ Save overrides, for setting up attribute-fields from the word's label.
        
        Attributes checked here: label-lowercasing, alphagram object, language
        """

        # Enforcing lowercase in database, for uniformity
        self.label = self.label.lower()
        print("word-label is: " + self.label + "  -- SAVED!")

        # Check for palindrome (if word is same reversed)
        # Uses extended slice syntax for reversal, for efficiency
        if self.label == self.label[::-1]:
            self.is_palindrome = True
        else:
            self.is_palindrome = False

        # Default language - set language if there is only 1 present in data.
        if WordLanguage.objects.count() == 1:
            self.language = WordLanguage.objects.get(id=1)

        # TODO: Update Homograph count (would need to maintain count across words with same spelling).
        #       Could also set a boolean value, for if a word is a homograph at all.
        
        ##  Alphagram setup  ##
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


class WordDefinition(models.Model):
    """ Dictionary definition. Usable for multiple definition entries, classed by language. Possibly in need of extending.
        
    Has many-to-one relationships with Language (of the definition), and with Word (which the definiton is for). Definition and word can be different languages.
    
    Attributes:
        label, detail, word, language
    """
    ##  Attributes  ##
    label = models.CharField(max_length=30, blank = False)
    detail = models.TextField(blank=False)
    word = models.ForeignKey(Word, blank=False, null=False, on_delete=models.CASCADE)
    language = models.ForeignKey(WordLanguage, blank=False, null=False, on_delete=models.CASCADE)
    
    ##  Non-editable attributes  ##
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.label
