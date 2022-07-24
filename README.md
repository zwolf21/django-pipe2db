# django-pipe2db


## Contents
- [Features](##Features)
- [Install](##Install)
- [Quickstart](##Quick-Start)
- [Tutorial](##Tutorial)


## Concepts
- A decorator that written by wrapping orm method of django models
- It maps the relationship between the models and data via nested dictionary


## Features
- It bridges Python functions and django models
- Create and update data to database via models
- Load minimum django settings for can use django orm as standalone that without using the django project


## Install

```bash
pip install django-pipe2db
```

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


#### Quick Result

|id|email|first_name|last_name|date_of_birth|date_of_death|
|--|--|--|--|--|--|
|1|xman1@google.com	|charse|javie|1975-07-25|1995-07-11|
|2|yman1@google.com	|jin|gray|1925-07-25|1999-01-21|
|3|batman1@google.com|wolverin|jack|1988-07-25|NULL|

