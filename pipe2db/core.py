from collections import abc
from types import GeneratorType
from pathlib import Path

from .utils import rename, get_or_create
from .vars import *

from django.core.files.base import ContentFile






class PipeReducer:

    def __init__(self, context, results):
        self.context = self._validate_context(context)
        self.results = self._validate_results(results)
    
    def _validate_results(self, results):
        if issubclass(results.__class__, abc.Mapping):
            results = [results]

        if isinstance(results, (GeneratorType, map, filter)):
            results = list(results)
            
        return results
    
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

    
    def reduce(self, many=True):
        '''깊이 탐색 방식으로 재귀호출하여 context와 results 에 내포된 외래키 형식을 처리

        '''
        for rel_type in [FOREIGIN_KEY_FIELDS, MANYTOMANY_FIELDS]:
            for field_name, subcontext in self.context.get(rel_type, {}).items():
                for row in self.results:
                    subresults = row[field_name]
                    if issubclass(subresults.__class__, abc.Mapping):
                        subresults = subresults.copy()
                    if isinstance(subresults, str):
                        subresults = {
                            subcontext[UNIQUE_KEY]: subresults
                        }
                    reducer = self.__class__(subcontext, subresults)
                    row[field_name] = reducer.reduce(many=(rel_type==MANYTOMANY_FIELDS))
                
        for field_name, fieldinfo in self.context.get(CONTENT_FILE_FIELDS, {}).items():
            src_field = fieldinfo[SOURCE_URL_FIELDS]
            for row in self.results:
                fn = Path(row[src_field]).name
                row[field_name] = ContentFile(row[field_name], fn)
        
        if renameset := self.context.get(RENAME_FIELDS):
            self.results = [
                rename(item, renameset) for item in self.results
            ]

        if model_name := self.context.get(MODEL):
            unique_key = self.context.get(UNIQUE_KEY)
            if unique_key is None:
                Warning(f"The unique_key of the model({model_name}) is not specified.")
            self.results = [
                get_or_create(
                    model_name, unique_key, item,
                    m2m_fields=self.context.get(MANYTOMANY_FIELDS),
                    exclude_fields=self.context.get(EXCLUDE_FIELDS)
                )
                for item in self.results
            ]

        return self.results if many else self.results[0]
    


