from functools import wraps

from .core import PipeReducer



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
            results = parser(*args, **kwargs)
            reducer = PipeReducer(context, results)
            if reducer.is_valid():
                reducer.reduce()
            return results
        return pipe
    return wrapper
