from pipe2db import pipe, setupdb
from pipe2db.utils import find_module
from samples import *

import bookstore

setupdb('bookstore.db')


@pipe({
    'model': 'db.Author',
    'unique_key': 'email',
    'method': 'update'
})
def insert():
    # find_module('bookstore.db')
    yield
    # yield author1
    # yield author2
    # yield author3

