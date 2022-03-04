from abc import ABC
from typing import Iterable, Callable, Tuple, Dict

from orm_types import Type


class BaseController(ABC):
    """Interface for data base queries."""
    __slots__ = ('__database__',)

    def __init__(self, object_class):
        self.object_class = object_class
        self.model_class = self.object_class.__model__

    @staticmethod
    def connect(cls):
        raise NotImplementedError

    def select(self, attrs, filters):
        raise NotImplementedError

    def bulk_insert(self, rows: list):
        raise NotImplementedError

    def update(self, new_data: dict):
        raise NotImplementedError

    def delete(self):
        raise NotImplementedError


class DictBaseController(BaseController):
    """Dictionary Data Base controller"""

    @staticmethod
    def connect(db: Dict):
        BaseController.__database__ = db

    def select(self, attrs: Iterable[Type], filters: Iterable[Tuple[Type, Callable]]):
        """Select data from db by filters"""
        table_data = self.__database__.get(self.model_class.__table_name__)
        attr_names = {attr.name for attr in attrs}
        value_filters = {attr.name: filter_ for attr, filter_ in filters}

        for row in table_data:

            check_filter = True

            for attr, filter_func in value_filters.items():
                value = row.get(attr)
                check_filter = filter_func(value) if value else False
                if not check_filter: break

            if not check_filter:
                continue

            row_data = {}
            for key, value in row.items():
                if key in attr_names:
                    row_data[key] = value
            yield self.object_class(**row_data)
