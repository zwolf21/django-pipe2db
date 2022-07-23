from functools import wraps

from django.apps import apps

from .core import PipeReducer
from .utils import get_kwargnames, select_kwargs


def pipe(context):
    '''
    @pipe({
        'model': 'bookstore.BookInstance',
        # 'method': 'create', # insert mode as default
        # 'method': 'update', # update mode
        'foreignkey_fields':{
            'book':{
                'model': 'bookstore.Book',
                'unique_key': ['isbn', 'title'],
                'rename_fields': {
                    'descriptions': 'summary',
                },
                'foreignkey_fields': {
                    'author': {
                        'model': 'bookstore.Author',
                        'unique_key': 'email',
                    }
                },
                'manytomany_fields': {
                    'genre': {
                        'model': 'bookstore.Genre',
                        'unique_key': 'name',
                    }
                },
                'contentfile_fields': {
                    'book_image': {
                        'source_url_field': 'src'
                    }
                }
            }
        }
    })
    def parse(self, response=None):
        author1 = {'
    '''
    def wrapper(parser):
        @wraps(parser)
        def pipe(*args, **kwargs):
            models_kwargs = {
                m.__name__:m for m in apps.get_models()
            }
            results = select_kwargs(parser, *args, **kwargs, **models_kwargs)
            reducer = PipeReducer(context, results)
            if reducer.is_valid():
                reducer.reduce()
            return results
        return pipe
    return wrapper
