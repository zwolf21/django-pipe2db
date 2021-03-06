from pipe2db import pipe, setupdb
from django.apps import apps


setupdb()


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



# create
@pipe({
    'model': 'db.Author',
    'unique_key': 'email',
})
def insert(Author):
    qs = Author.objects.values_list()
    for row in qs:
        print(row)
    
    yield author1
    yield author2
    yield author3



# create or update
@pipe({
    'model': 'db.Author',
    'unique_key': 'email',
    'method': 'update'
})
def insert_and_update():
    author1['first_name'] = 'updated'
    yield author2
    yield author3
    yield author1




