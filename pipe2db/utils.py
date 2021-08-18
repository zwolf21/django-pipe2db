from django.apps import apps



def get_or_create(model_name, unique_key, item, m2m_fields=None, exclude_fields=None):
    def drop_exclude_column(item, exclude_fields):
        excluded = {
            k:v for k, v in item.items() if k not in (exclude_fields or [])
        }
        return excluded or item

    model = apps.get_model(model_name)
    if unique_key is None:
        return model.objects.create(**item)

    m2mset = {
        field:item.pop(field) for field in m2m_fields or []
    }

    try:
        object = model.objects.get(**{unique_key: item[unique_key]})
    except model.DoesNotExist:
        excluded = drop_exclude_column(item, exclude_fields)
        object = model.objects.create(**excluded)
    for field, m2m_list in m2mset.items():
        getattr(object, field).add(*m2m_list)

    return object


def rename(item, oldnewset):
    existing = {
        k: item[k] for k in item if k not in oldnewset.keys()
    }
    new = {
        n: item[o] for o, n in oldnewset.items()
    }
    existing.update(new)
    return existing