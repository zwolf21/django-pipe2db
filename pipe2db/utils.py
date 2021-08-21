from django.apps import apps
from django.db.models import Model

from .vars import  METHOD_CREATE, UNIQUE_KEY


def get(model, unique_key, item):
    if not isinstance(unique_key, (list, tuple, str)):
        raise ValueError(f"{UNIQUE_KEY} must be str, tuple, or list")
    
    if isinstance(unique_key, str):
        unique_key = [unique_key]

    kwargs = {
        key:item[key] for key in unique_key
    }
    
    try:
        object =  model.objects.get(**kwargs)
    except model.MultipleObjectsReturned:
        raise KeyError(f"{unique_key} is not unique filelds in {model._meta.object_name}")
    else:
        return object


def create(model, item):
    return model.objects.create(**item)


def get_model(model_name):
    if isinstance(model_name, str):
        model = apps.get_model(model_name)
    elif issubclass(model_name.__class__, Model):
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

    if method == METHOD_CREATE:
        m2mset = pop_m2m_column(item, m2m_fields)
        item = rename_column(item, rename_fields)
        item = drop_exclude_column(item, exclude_fields)

        if unique_key is None:
            object = create(model, item)
        else:
            try:
                object = get(model, unique_key, item)
            except model.DoesNotExist:
                object = create(model, item)

        add_m2m_items(object, m2mset)

    else:
        try:
            object = get(model, unique_key, item)
        except model.DoesNotExist:
            raise KeyError(
                f"{model._meta.object_name} matching query does not exist. ({unique_key}={item[unique_key]}), Method: {method}; Would you Create {model._meta.object_name} instance first?"
                )
      
    return object

    



