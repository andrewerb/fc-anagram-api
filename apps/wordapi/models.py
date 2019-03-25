""" Dictionary-Words / Anagram API app - Data models

For Django FC_coding_challenge - wordapi app
This model exists for querying words and their anagrams, across lanaugages/dictionaries, via web API.


- The intended usecase of this model and API is to find word-matches for which user-submitted queries/input are a substring, and anagrams of those matching subject-words.
- Anagrams are recombinations of the order of letters (preserving the same count) of a subject-word, into another word.
- All words that are anagrams of one another will also share the same alphagram– the string resulting from sorting a word/string's letters/characters alphabetically.  https://en.wiktionary.org/wiki/alphagram
- Alphagrams are used here to assocate words in data that are anagrams to each other. Views can query the alphagram of a subject-word to get other words with that alphagram, which are the subject-word's anagrams.


Models:
    WordLanguage
    Alphagram
    Word
    WordDefinition : Not really used at this point, but available.


A lot of the heavy lifting in the Word model. This is because:
    - Words are most of the data
    - Words are queried the most / make sense to query much of the time
    - Words need to have some form of relationship with their alphagram or anagram. (Here, the have a many-to-one relationship witht their alphagram, by which anagrams can be queried and associated).

    In Word's overridden save() method, alphagrams are solved, saved in data if needed, and set as a foreign relation to word.
    A caveat here is that it is very hard (slow) to bulk initialize the word list, because it relies so heavily on the save() method, and alphagrams aren't currently designed to be left blank.


Future optimizations are very possible, especially in this data model:

    - Moving where alphagrams are generated out of solely the save() method.
        
        This would primarily be to optimize the inital database setup Django's bulk_create method.
        
        A complication/caveat in this current implementation is the overhead in initialization with file reads and either queuing alphagrams in-memory or making many calls to the database anyway to check for alphagram values. The whole point of bulk_create is to limit database access a bit, and those value checks wouldn't help much.

        ** A likely solution would be to fix the alphagram model's requirements, bulk_create words in data from a dictionary file, and go over those values later to assign alphagrams. It's not really fast either way, but splits up work.

    - Associating words with their anagram results directly. 
        
        This would require a lot more work and overhead when saving words (updating a value in data for EVERY word that is an anagram of another being entered or updated). But, it would save a significant amount of time in user-querying. This could even be stored as a static text field in a Word's data table, saving an entire second query when pulling a queryset of subject-words.
        
        Again, it's a lot more overhead to set up, so it's ommitted here.

    - A separate data model for substring queries would help optimization and would be an interesting/useful enhancement to this project.
        
        Particularly in a frontend implementation where API data is requested for updates as the user types, shorter substrings (API input-params/search strings) for "contains" are VERY slow. They require the DB to look over too many entries.

        An optimization for this is to pre-process those results beforehand and shift them over entirely to another model/data-table for short substrings. For all 3 characters, all alphabetical, the database size would be 2^3: 17576 entries. Compared to a data table of nearly 35,000 words, this would be more efficient.

        Furthermore, rather than using an "icontains" query-filter, these search references would represent exact matches to string input, which is quicker to search in a sorted data table. This could even be served by a separate database (diverting traffic and machine work), called via a separate API endpoint by the client, or an in-memory data-store.

        Depending on size, something like single letter query data could be pre-cached by the client. 26 entries. But they'd have to be designed to not be overwhelming to serve.
"""


import datetime

from django.db import models
from django.utils import timezone


###################
##  Data Models  ##
###################
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
    
    # TODO: Order by label


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
    label = models.CharField(max_length=50, db_index=True)  # Labels are not unique, because other words in DB (homographs) may have same spelling w/ unique IDs.
    language = models.ForeignKey(WordLanguage, blank=True, null=True, on_delete=models.CASCADE)

    ##  Non-editable attributes  ##
    alphagram = models.ForeignKey(Alphagram, editable=False, on_delete=models.CASCADE)
    is_palindrome = models.BooleanField(default=False, editable=False)
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    
    # TODO: homograph_count = models.IntegerField(default=0) # use if able to initialize (would require updating other words with same label).
    
    def __str__(self):
        return self.label
    
    def save(self, *args, **kwargs):
        """ Save overrides, for setting up attribute-fields from the word's label.
        
        Attributes checked here: label-lowercasing, alphagram object, language
        """

        ##  Enforcing lowercase in database, for uniformity  ##
        self.label = self.label.lower()
        print("word-label is: " + self.label + "  -- SAVED!")

        ##  Check for palindrome (if word is same reversed)  ##
        # Uses extended slice syntax for reversal, for efficiency
        if self.label == self.label[::-1]:
            self.is_palindrome = True
        else:
            self.is_palindrome = False

        ##  Default language - set language if there is only 1 present in data.  ##
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
