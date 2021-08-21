from django.test import TestCase

from .test_data import *
from .models import *
from pipe2db import pipe


def destroyall():
    Author.objects.all().delete()
    Genre.objects.all().delete()

def destorybook():
    Book.objects.all().delete()

def destorybookinstance():
    BookInstance.objects.all().delete()


@pipe({
    'model': 'bookstore.BookInstance',
    'foreignkey_fields':{
        'book':{
            'model': 'bookstore.Book',
            'unique_key': ['isbn', 'title'],
            'rename_fields': {
                'descriptions': 'summary',
            },
            'foreignkey_fields': {
                'author': {
                    'model': 'bookstore.Author',
                    'unique_key': 'email',
                }
            },
            'manytomany_fields': {
                'genre': {
                    'model': 'bookstore.Genre',
                    'unique_key': 'name',
                }
            }
        }
    }
})
def insert_book_instance():
    destroyall()
    yield bookinstance1_nested_all
    yield bookinstance2_nested_all
    yield bookinstance3_nested_all
    yield bookinstance4_nested_all
    yield bookinstance5_nested_all

@pipe({
    'model': 'bookstore.Book',
    'unique_key': 'isbn',
    'foreignkey_fields': {
        'author': {
            'model': 'bookstore.Author',
            'unique_key': 'email',
        }
    },
    'manytomany_fields': {
        'genre': {
            'model': 'bookstore.Genre',
            'unique_key': 'name'
        }
    },
    'rename_fields': {
        'descriptions': 'summary'
    }
})
def insert_booK_by_author_key_genre_key():
    insert_book_instance()
    destorybook()
    yield book1_with_key_author_key_genre
    yield book2_with_key_author_key_genre
    yield book3_with_key_author_key_genre
    yield book4_with_key_author_key_genre
    yield book5_with_key_author_key_genre





