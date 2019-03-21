""" Dictionary-Words / Anagram API - Factories

    - Factories are database data-instantiation objects
    - Using the package factory_boy
    - As an alternative to Django fixtures, factories use Django's ORM and data models to create default or test data in a Django project DB.

    Here, only a Word model factory is provided.
    TODO: Word Language for English
"""


import factory
import factory.django

from .models import *


class WordFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Word

    label = ""


def main():
    print("This is a Word factory class for initializing database data.")

if __name__ == "__main__":
    main()
