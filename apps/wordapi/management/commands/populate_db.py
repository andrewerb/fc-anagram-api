""" Populate Database words to App's DB, from dictionary

"""

import os, sys

from django.core.management.base import BaseCommand
from apps.wordapi.factory import *

class Command(BaseCommand):
    help = 'Populates the database.'

    """
    def add_arguments(self, parser):
        parser.add_argument('--users',
            default=200,
            type=int,
            help='The number of fake users to create.')
    """

    
    def handle(self, *args, **options):
        """ Code run by manage.py and commands for this module
        """
        input_file = "data/dictionary.txt"
        # get count of languages. set if 0.


        print("Running!")
        
        input_file_line_count = 0

        
        with open(input_file, "r") as f:
            for i, line in enumerate( f.readlines() ):
                new_word = line.strip().lower()
                WordFactory.create(label=new_word)
                if not new_word:
                    raise ValueError('empty string')
                
                input_file_line_count += 1

        print( "\n\nTotal number of lines/words:\t" + str(input_file_line_count) )


        # TODO: make a language if not already there. If count is greater than zero.


def main():
    print("Please run this file using:\n python manage.py populate_db ")

if __name__ == "__main__":
    main()