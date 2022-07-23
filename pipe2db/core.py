import os, sys, inspect, importlib
from collections import abc
from types import GeneratorType
from pathlib import Path
from copy import deepcopy

from django.conf import settings
from django.core.management import execute_from_command_line
from django.core.files.base import ContentFile

from .utils import get_or_create, get_base_module_name, get_module_dir, find_models_module
from .vars import *



class PipeReducer:

    def __init__(self, context, results):
        self.context = self._validate_context(context)
        self.results = self._validate_results(results)
    
    def _validate_results(self, results):
        if isinstance(results, str):
            results = [results]

        if isinstance(results, abc.Mapping):
            results = [results]

        if isinstance(results, (GeneratorType, map, filter)):
            results = list(results)
        
        if not results or not results[0]:
            return
                    
        return deepcopy(results)
    
    def _validate_context(self, context, stauts='model', pwd='top-level'):

        for key, val in context.items():
            if key not in VALIDATE_KEYS:
                raise KeyError(f"{key}: not a valid key name. (value:{val})")

            if key in [FOREIGIN_KEY_FIELDS, MANYTOMANY_FIELDS]:
                if not isinstance(val, dict):
                    raise ValueError(f"The value({val}) of the foreign key({key}) must be a dict type. not {type(val)}")
                for field_name, subcontext in val.items():
                    self._validate_context(subcontext, stauts='model', pwd=field_name)
            
        if stauts == 'model':
            if not context.get('model'):
                raise KeyError(f"The '{pwd}' field must have a 'model'")    
        return context
    
    def _val2obj(self, item):
        if isinstance(item, (str, int)):
            if unique_key_name := self.context.get(UNIQUE_KEY):
                item = {unique_key_name: item}
            else:
                raise KeyError(
                    f"When method is '{METHOD_GET}', the key of 'unique_key' is required in manytomany_fields"
                )
        return item

    def reduce(self, many=True):
        '''깊이 탐색 방식으로 재귀호출하여 context와 results 에 내포된 외래키 형식을 처리
        '''
        method = self.context.get(METHOD, METHOD_CREATE)

        if method in [METHOD_UPDATE, METHOD_CREATE]:
            for field_name, fk_context in self.context.get(FOREIGIN_KEY_FIELDS, {}).items():
                for item in self.results:
                    fk_item = item[field_name]
                    # if issubclass(fk_item.__class__, abc.Mapping):
                    #     fk_item = deepcopy(fk_item)
                    subreducer = self.__class__(fk_context, fk_item)
                    item[field_name] = subreducer.reduce(many=False)


            for field_name, m2m_context in self.context.get(MANYTOMANY_FIELDS, {}).items():
                for item in self.results:
                    m2m_item_list = item[field_name]
                    if not isinstance(m2m_item_list, list):
                        raise TypeError(
                            f"The value of key {field_name} type error: list type is required as the value of manytomany_fields, not {type(m2m_item_list)}"
                        )
                    subreducer = self.__class__(m2m_context, m2m_item_list)
                    item[field_name] = subreducer.reduce(many=True)

        
            for field_name, fieldinfo in self.context.get(CONTENT_FILE_FIELDS, {}).items():
                src_field = fieldinfo[SOURCE_URL_FIELDS]
                for row in self.results:
                    fn = Path(row[src_field]).name
                    row[field_name] = ContentFile(row[field_name], fn)
        

        self.results = [
            self._val2obj(item) for item in self.results
        ]                    
   
        if model_name := self.context.get(MODEL):
            unique_key = self.context.get(UNIQUE_KEY)
            if unique_key is None:
                Warning(f"The unique_key of the model({model_name}) is not specified.")
            self.results = [
                get_or_create(
                    model_name, unique_key, item,
                    m2m_fields=self.context.get(MANYTOMANY_FIELDS),
                    exclude_fields=self.context.get(EXCLUDE_FIELDS),
                    rename_fields=self.context.get(RENAME_FIELDS),
                    method=method
                )
                for item in self.results
            ]

        return self.results if many else self.results[0]
    


def setupdb(*db_apps, db_settings:dict=None, default_db_name='pipe2db.sqlite3', **extra_settings):
    '''Enables Django's orm and management to be used as a standalone db
        need to be run before import models

    :param db_app: package as module which models.py is located, if null, finding db app automatically
    :param db_settings: database setting in django's settings.py, defaults to sqlite
    :default_db_name: Specify db name when using sqlite as default
    :extra_settings: config for django's settings.py
    
    ```python
    # auto find and setup db with no args
    setupdb()

    # specifiy db app witch contains models.py
    # ..../.../bookstore/db/models.py
    setupdb('bookstore.db')

    # db_settings example for sqlite
    settings = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': 'your_db_file_name.sqlite3'
        }
    }
    setupdb('bookstore.db', db_settigns=settings)

    # extra_settings examples
    setupdb('bookstore.db', TIME_ZONE='Asia/Seoul', USE_TZ=False)

    from db.models import Author
    ```
    
    '''
    if module := os.environ.get('DJANGO_SETTINGS_MODULE'):
        print(f"DJANGO_SETTINGS_MODULE already setted as {module}")
        return

    if settings.configured:
        print("Settings already configured.")
        return

    apps = []
    if db_apps:
        for db_app in db_apps:
            if isinstance(db_app, str):
                db_app = importlib.import_module(db_app)

            if inspect.ismodule(db_app):
                module_dir = get_module_dir(db_app)
            else:
                raise ValueError(f'{db_app} must be packages which contains models.py') 
            if module_dir not in sys.path:
                sys.path.append(module_dir)
            app = get_base_module_name(db_app)
            apps.append(app)
    else:
        path = find_models_module()
        module_dir, app = os.path.split(path)
        apps.append(app)
        if module_dir not in sys.path:
            sys.path.append(module_dir)
    
    settings.configure(
        INSTALLED_APPS=apps,
        DATABASES = db_settings or {
            'default': {
                'ENGINE': 'django.db.backends.sqlite3',
                'NAME': default_db_name
            }
        },
        DEFAULT_AUTO_FIELD='django.db.models.BigAutoField',
        **extra_settings
    )
    commands='makemigrations', 'migrate',
    for app in apps:
        for commmand in commands:
            execute_from_command_line(['_', commmand, app])
