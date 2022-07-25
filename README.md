# django-pipe2db


## Contents
  - [Concepts](#concepts)
  - [Features](#features)
  - [Install and Import](#install-and-import)
  - [Quick Start](#quick-start)
    - [1. Using django orm as standalone](#1-using-django-orm-as-standalone)
    - [2. Using with django project](#2-using-with-django-project)
  - [Tutorial](#tutorial)
    - [Argument of pipe decorator as context](#argument-of-pipe-decorator-as-context)
      - [model](#model)


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
## Tutorial

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




