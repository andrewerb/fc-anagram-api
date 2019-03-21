""" Populate Database words to App's DB, from dictionary

    Reads dictionary of words from data/dictionary.txt
    
    NOTE: An area of this module that is significantly needed is batching of ORM/model objects before insertion. 
    This is currently ommitted due to complication with alphagram/anagram creation, foreign key setting, and the lack of time saved by it.
    This ommission really extends the setup time, is inefficient, and would be a priority enhancement to the project with more time.
"""

import os, sys

from collections import defaultdict
from django.core.management.base import BaseCommand
from apps.wordapi.models import *


class Command(BaseCommand):
    """ Command methods for manage.py call to populate_db module

        Command is the class manage.py will look to for methods when this module is referenced to it.
    """

    help = 'Populates the database.' # help attribute For info on module/command

    def __set_language(self, lang_label="English"):
        """ Helper method to handle() for language object
            Callable by handle() to save a language object. Defaults to English, for this project's dictionary purposes. A different language label can be passed.
        """
        if lang_label: # Ignore setup if blank value passed
            if WordLanguage.objects.filter(label=lang_label).count():
                # Setup only proceeds if there isn't already a language in data by this label
                pass
            else:
                lang = WordLanguage(label=lang_label)
                lang.save()
        
    def __read_dict_to_words(self, dict_file="data/dictionary.txt"):
        dict_file = "data/_shortlist.txt"
        
        input_file_word_count = 0 # for count at the end of file read/insertion
        
        with open(dict_file, "r") as f:
            for line in f.readlines():
                # Read file by line to insert new word
                new_word_label = line.strip().lower()
                if not new_word_label:
                    pass #raise ValueError('empty string')
                else:
                    input_file_word_count += 1
                    w = Word(label=new_word_label)
                    w.save()
                    

        print( "\n\nTotal number of lines/words:\t" + str(input_file_word_count) )
    
    def handle(self, *args, **options):
        """ Code run by manage.py and commands for this module
            Checks for words in data. Sets up English as a default if missing.
            Reads word-input/dictionary, batches Word objects, saves objects into DB.
        """

        print("Initializing...")

        if not WordLanguage.objects.count(): # If no languages are already set up
            self.__set_language() # Add English language by default, from helper method

        self.__read_dict_to_words() # Read and add words from helper method
        


def main():
    print("Please run this file using:\n python manage.py populate_db ")

if __name__ == "__main__":
    main()