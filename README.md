# django-pipe2db


## Contents
- [django-pipe2db](#django-pipe2db)
  - [Contents](#contents)
  - [Concepts](#concepts)
  - [Features](#features)
  - [Install and Import](#install-and-import)
  - [Quick Start](#quick-start)
    - [1. Using django orm as standalone](#1-using-django-orm-as-standalone)
    - [2. Using with django project](#2-using-with-django-project)
  - [Useage](#useage)
    - [Argument of pipe decorator as context](#argument-of-pipe-decorator-as-context)
      - [model](#model)
      - [unique_key](#unique_key)
      - [method](#method)
      - [rename_fields](#rename_fields)
      - [exclude_fields](#exclude_fields)
      - [foreignkey_fields](#foreignkey_fields)



## Concepts
- A decorator that written by wrapping orm method of django models
- It maps the relationship between the models and data via nested dictionary

---
## Features
- It bridges Python functions and django models
- Create and update data to database via models
- Automatically create and modify tables by wrapping manage.py commands from django as makemigrations and migrate
- Load minimum django settings for can use django orm as standalone that without using the django project
- Insertion of data with the same relationship as foreignkey and manytomany fields
- Inserting a content file object as an image field

---
## Install and Import

```bash
pip install django-pipe2db
```
```python
# crawler.py
from pipe2db import pipe
from pipe2db import setupdb
```
---
## Quick Start


### 1. Using django orm as standalone
- Create models.py in the directory that will be used as the Django app
- example for minimum project directory structure. [see](https://github.com/zwolf21/django-pipe2db/tree/master/test)
```bash
Project
│  __main__.py
│
└─bookstore
    │  insert.py
    │  
    └─db
          models.py
```

```python
# models.py
from django.db import models


class Author(models.Model):
    email = models.EmailField('Email', unique=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    date_of_birth = models.DateField(null=True, blank=True)
    date_of_death = models.DateField('Died', null=True, blank=True)

    class Meta:
        db_table = 'author'
```
```python
# insert.py
from pipe2db import pipe, setupdb


setupdb() # find models automatically
# setupdb('bookstore.db') # or more explicitly 

# The key of the data and the field names of the model are matched
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


@pipe({
    'model': 'db.Author', 
    'unique_key': 'email', # unique values of table as pk
    # 'method': 'update' # If uncomment, works in update mode
})
def insert(*args, Author, **kwargs):
    # You Can get model class via argumenting at generator function

    # from django.apps import apps # or via get_model method of django
    # Author = apps.get_model('db.Author') 

    queryset = Author.objects.all()

    yield from [author1, author2, author3]

```

- run examples
```bash
python bookstore/insert.py
```


### 2. Using with django project
- Since DJANGO_SETTINGS_MODULE is already setted, it's not need to call setupdb
- [django site example](https://github.com/zwolf21/django-pipe2db/tree/master/testsite/bookstore)

> run via shell which excuted by 'python manage.py shell' command of django manage
> ```bash
> python manage.py shell
> ```
>```python
>In [1]: from yourpackage.insert import insert
>In [2]: insert()
>```


|id|email|first_name|last_name|date_of_birth|date_of_death|
|--|--|--|--|--|--|
|1|xman1@google.com	|charse|javie|1975-07-25|1995-07-11|
|2|yman1@google.com	|jin|gray|1925-07-25|1999-01-21|
|3|batman1@google.com|wolverin|jack|1988-07-25|NULL|



--- 
## Useage

### Argument of pipe decorator as context
- A context is a dictionary that describes the relationship between the model and the data
- In the following examples, the elements that make up the context are explained step by step

#### model
- django model to pipe data written as string literals
```python
# some_crawler.py
from pip2db import pipe

@pipe({
    'model': 'db.Author'
})
def abc_crawler():
    ...
    yield row
```
> It is also a good way to assign and use a variable to increase reusability
> When expressing nested relationships in relational data, not assigning them as variables can result in repeatedly creating the same context.
```python
# assign to variable crawler.py

# It seems to better way
context_author = {
    'model': 'db.Author'
}

@pipe(context_author)
def abcd_crawler(*args, **kwargs):
    yield ..
```

- It is also possible to specify the model by directly importing it, but in the case of standalone, you must declare setupdb before importing the model
  
```python
# dose not look good.py

from pipe2db import setupdb, pipe

setupdb()
from .db.models import Author

context_author = {'model': Author}

@pipe(context_author)
def abc():
    yield ..
```

> Another way to refer to the model class
> 1. Using Django's apps module
>   ```python
>   from django.apps import apps
>
>   Author = apps.get_model('db.Author')
>   ```
> 2. Specify the model name as an argument to the generator function
>   ```python   
>   # An example of controlling a generator based on data in a database
>   @pipe(context_author)
>   def abc_crawler(rows, response, Author):
>       visited = Author.objects.values_list('review_id', flat=True)
>       for row in rows:
>           if row['id'] in visited:
>               break
>           yield row
>   ```

#### unique_key
- key to identify data like as primary key
- If you don't specify it, creating data will be duplicated
- To identify data with one or several keys as unique_together

```python
# models.py

# unique key model
class Author(models.Model):
    ...
    first_name = models.CharField(max_length=100, unique=True)
    ...
```

```python
# uniqufy_by_one.py

context_author = {
    'model': 'db.Author',
    'unique_key': 'first_name'
}
```

> If uniqueness is not guaranteed with one key, add another
>```python
># models.py
>
># unique together model
>class Author(models.Model):
>    ...
>    first_name = models.CharField(max_length=100)
>    last_name = models.CharField(max_length=100)
>
>    class Meta:
>        unique_together = ['first_name', 'last_name']
>    ...
>```
>```python
>#unique_together.py
>
>context_author = {
>    'model': 'db.Author',
>    'unique_key': ['first_name', 'last_name']
>}
>```


#### method
- Creates or updates data with a unique key specified
- Defaults is create
- In create mode, data is inserted based on unique.
- In update mode as wrapper update_or_create of django method, creates records if they don't exist, otherwise modifies existing records


```python
# incorrect create.py

author_incorrect = {
    'email': 'batman1@google.com',
    'first_name': 'who', # incorrect
    'last_name': 'jackman',
    'date_of_birth': '1988-07-25', # incorrect
    'date_of_death': None
}

context = {
    'model': 'db.Author',
    'unique_key': 'email',
    # 'method': 'create' no need to specify if create
}

@pipe(context)
def gen_author(...):
    yield author_incorrect
```
> result table
>
>|id|email|first_name|last_name|date_of_birth|date_of_death|
>|--|--|--|--|--|--|
>|3|batman1@google.com|who|jackman|1988-07-25|NULL|


```python
# correct as update.py

author_corrected = {
    'email': 'batman1@google.com',
    'first_name': 'Hugh', # correct
    'last_name': 'jackman',
    'date_of_birth': '1968-10-12', # correct
    'date_of_death': None
}

context = {
    'model': 'db.Author',
    'unique_key': 'email',
    'method': 'update', # for update record by corrected data
}

@pipe(context)
def gen_author(...):
    yield author_corrected
```
> result table
>
>|id|email|first_name|last_name|date_of_birth|date_of_death|
>|--|--|--|--|--|--|
>|3|batman1@google.com|Hugh|jackman|1968-10-12|NULL|


#### rename_fields
- Dictionary of between data and model as key:field mapping
- Used when the data key and the model field name are different

```python
# models.py
class Author(models.Models):
    ...
    ...

class Book(models.Model):
    title = models.CharField(max_length=200) 
    isbn = models.CharField('ISBN', max_length=13, unique=True)

    class Meta:
        db_table = 'book'
```

```python
# book_crawler.py

context = {
    'model': 'db.Book',
    'unique_key': 'isbn',
    'rename_fields': {
        'header' : 'title', 
        'book_id': 'isbn',
    }
}
# map header -> title, book_id -> isbn

@pipe(context)
def book_crawler(abc, defg, jkl=None):
    book_list = [
        {
            'header': 'oh happy day', # header to title
            'book_id': '1234640841',
        },
        {
            'header': 'oh happy day',
            'book_id': '9214644250',
        },
    ]
    yield from book_list
```

#### exclude_fields
- List of keys to excluds
- Used when the data has a key that is not in the field names in the model
- Filter too much information from data that model cannot consume
  
```python
# bookcrawler.py
...
...

context = {
    'model': 'db.Book',
    'unique_key': 'isbn',
    'rename_fields': {
        'header' : 'title', 
        'book_id': 'isbn',
    },
    'exclude_fields': ['status'] # exclude
}

@pipe(context)
def book_crawler(abc, defg, jkl=None):
    book_list = [
        {
            'header': 'oh happy day', # header to title
            'book_id': '1234640841',
            'status': 'on sales', # status is not needed in Book model
        },
        {
            'header': 'oh happy day',
            'book_id': '9214644250',
            'sstatus': 'no stock',
        },
    ]
    yield from book_list

```

--- 
Mapping of Relative Data

#### foreignkey_fields
- Creat records by generation according to the foreign key relationship between tables
- Recursively nest parent data to children data
- There are two way of create relationship data

```python
# models.py
# two models of related with foreign key
from django.db import models


class Author(models.Model):
    email = models.EmailField('Email', unique=True)
    name = models.CharField(max_length=100)

    class Meta:
        db_table = 'author'


class Book(models.Model):
    author = models.ForeignKey('Author', on_delete=models.CASCADE, null=True) # fk
    isbn = models.CharField('ISBN', max_length=13, unique=True)
    title = models.CharField(max_length=200)

    class Meta:
        db_table = 'book'
```

```python
# some crawler.py
# 1. Generate data of book author nested

context_author = {
    'model': 'db.Author',
    'unique_key': 'email',
    'method': 'update'
}

context_book = {
    'model': 'db.Book',
    'unique_key': 'isbn',
    'foreignkey_fields': {
        'book': context_author
    }
}

# author data is nested in book data
@pipe(context_book)
def parse_book():
    author1 = {
        'email': 'pbr112@naver.com',
        'name': 'hs moon',
    }
    book = {
        'author': author1,
        'title': 'django-pipe2db',
        'isbn': '291803928123'
    }
    yield book

```

```python
# some crawler.py 
# 2. Generate data of author and book sequentially

@pipe(context_author)
def parse_author():
    author1 = {
        'email': 'pbr112@naver.com',
        'name': 'hs moon',
    }
    yield author1

# create author first
author1 = parse_author()

# create book after and connect fk relation to author
@pipe(context_book)
def parse_book():
    book = {
        'author': author1['email'], # Since the author has already been created, it possible to pass email as pk of author only
        # 'author': author1, # or same as above
        'title': 'django-pipe2db',
        'isbn': '291803928123'
    }
    yield book
```


