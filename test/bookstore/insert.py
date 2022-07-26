from pipe2db import pipe, setupdb
from django.apps import apps


setupdb(default_db_name='pipe2db_test.sqlite3')


author1 = {
    'email': 'xman1@google.com',
    'first_name': 'charse',
    'last_name': 'javie',
    'date_of_birth': '1975-07-25',
    'date_of_death': '1995-07-11'
}
author2 = {
    'email': 'yman1@google.com',
    'first_name': 'jin',
    'last_name': 'gray',
    'date_of_birth': '1925-07-25',
    'date_of_death': '1999-01-21'
}
author3 = {
    'email': 'batman1@google.com',
    'first_name': 'wolverin',
    'last_name': 'jack',
    'date_of_birth': '1988-07-25',
    'date_of_death': None
}


context_author = {
    'model': 'db.Author',
    'unique_key': 'email',
}

# create
@pipe(context_author)
def insert(Author):
    qs = Author.objects.values_list()
    for row in qs:
        print(row)
    
    yield [author1, author2, author3]

context_author['method'] = 'update'
# create or update
@pipe(context_author)
def insert_and_update():
    author1['first_name'] = 'updated1'
    yield from [author1, author2, author3]




