from pipe2db import pipe, setupdb
from pipe2db.utils import find_models_module
from samples import *

# import db

setupdb()


@pipe({
    'model': 'db.Author',
    'unique_key': 'email',
    'method': 'update'
})
def insert():
    # find_models_module()
    yield author1
    # yield author2
    # yield author3

