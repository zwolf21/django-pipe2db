from functools import wraps

from .core import PipeReducer



def pipe2db(context):
    ''' 'model'
        'unique_key'
        'foreignkey_fields'
        'manytomany_fields'
        'source_url_fields'
        'contentfile_fields'
        'rename_fields'
        'exclude_fields'
    '''
    def wrapper(parser):
        @wraps(parser)
        def pipe(*args, **kwargs):
            results = parser(*args, **kwargs)
            reducer = PipeReducer(context, results)
            reducer.reduce()
            return results
        return pipe
    return wrapper