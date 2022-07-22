import inspect, itertools, os

from django.apps import apps
from django.db import models

from .vars import *


def _validate_uniquekey(unique_key):
    if not isinstance(unique_key, (list, tuple, str)):
        raise ValueError(f"{UNIQUE_KEY} must be str, tuple, or list")
    if isinstance(unique_key, str):
        unique_key = [unique_key]
    return unique_key


def get(model, unique_key, item):
    unique_key = _validate_uniquekey(unique_key)

    kwargs = {
        key:item[key] for key in unique_key
    }
    try:
        object = model.objects.get(**kwargs)
    except model.MultipleObjectsReturned:
        raise KeyError(f"{unique_key} is not unique filelds in {model._meta.object_name}")            
    return object


def update(model, unique_key, item):
    object = get(model, unique_key, item)
    unique_keys = _validate_uniquekey(unique_key)
    
    pkset = {k:v for k, v in item.items() if k in unique_keys}
    defaults = {k:v for k, v in item.items() if k not in unique_keys}
    
    obj, created = model.objects.update_or_create(defaults=defaults, **pkset)
    return obj


def create(model, item):
    return model.objects.create(**item)


def get_model(model_name):
    if isinstance(model_name, str):
        model = apps.get_model(model_name)
    elif issubclass(model_name, models.Model):
        model = model_name
    else:
        raise ValueError(f"The type of {model_name} must be str or model class")
    return model


def pop_m2m_column(item, m2m_fields):
    if m2m_fields:
        m2mset = {
            field:item.pop(field) for field in m2m_fields
        }
        return m2mset


def add_m2m_items(object, m2mset):
    if m2mset:
        for field, m2m_list in m2mset.items():
            getattr(object, field).add(*m2m_list)
    return object


def drop_exclude_column(item, exclude_fields):
    if exclude_fields:
        excluded = {
            k:v for k, v in item.items() if k not in (exclude_fields)
        }
        return excluded
    return item


def rename_column(item, oldnewset):
    if oldnewset:
        existing = {
            k: item[k] for k in item if k not in oldnewset.keys()
        }
        new = {
            n: item[o] for o, n in oldnewset.items()
        }
        existing.update(new)
        return existing
    return item


def get_or_create(
    model_name, unique_key, item,
    m2m_fields=None, exclude_fields=None, rename_fields=None,
    method=METHOD_CREATE
):

    model = get_model(model_name)

    if method in [METHOD_CREATE, METHOD_UPDATE]:
        m2mset = pop_m2m_column(item, m2m_fields)
        item = rename_column(item, rename_fields)
        item = drop_exclude_column(item, exclude_fields)

        if unique_key is None:
            object = create(model, item)
        else:
            try:
                object = get(model, unique_key, item)
            except model.DoesNotExist:
                # if method == METHOD_UPDATE:
                #     raise ValueError(f"When the method is {METHOD_UPDATE}, the value of the item corresponding to the unique key({unique_key}) of the model cannot be changed.")
                object = create(model, item)
            except model.MultipleObjectsReturned:
                raise KeyError(f"{unique_key} is not unique filelds in {model._meta.object_name}")            
            else:
                if method == METHOD_UPDATE:
                    object = update(model, unique_key, item)
        add_m2m_items(object, m2mset)

    else:
        try:
            object = get(model, unique_key, item)
        except model.DoesNotExist:
            raise KeyError(
                f"{model._meta.object_name} matching query does not exist. ({unique_key}={item[unique_key]}), Method: {method}; Would you Create {model._meta.object_name} instance first?"
                )
      
    return object

    
def module2dict(module):
    return dict(itertools.takewhile(lambda i: i[0] != '__builtins__', inspect.getmembers(module)))


def get_base_module_name(module):
    *_, base = module.__name__.split('.')
    return base

def get_module_dir(module):
    return os.path.dirname(module.__path__[0])

from glob import glob
import os

def find_module(module_name):
    root = os.path.dirname(os.path.abspath('.'))
    root = os.path.abspath('.')
    root = os.path.join(root, 'test')
    print(root)
    for path in glob('./**/*.py', recursive=True, root_dir=root):
        print(path)
