from pipe2db import pipe, setupdb
from samples import *



setupdb('bookstore')


@pipe({
    'model': 'bookstore.Author',
    'unique_key': 'email',
    'method': 'update'
})
def insert():
    yield author1
    yield author2
    yield author3

