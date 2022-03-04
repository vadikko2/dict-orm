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
    def connect():
        """Connect to database method"""
        raise NotImplementedError

    @staticmethod
    def disconnect():
        """Disconnect method"""
        raise NotImplementedError

    def select(self, attrs, filters):
        """Select Query"""
        raise NotImplementedError

    def insert(self, row):
        """Insert Query"""
        raise NotImplementedError

    def bulk_insert(self, rows: Iterable):
        """Bulk Insert Query"""
        raise NotImplementedError

    def update(self, row, filters):
        """Update Query"""
        raise NotImplementedError

    def delete(self, filters):
        """Delete Query"""
        raise NotImplementedError


class DictController(BaseController):
    """Dictionary Data Base controller"""

    @staticmethod
    def connect(db: Dict):
        BaseController.__database__ = db

    @staticmethod
    def disconnect():
        BaseController.__database__ = None

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

    def insert(self, row):
        """Insert BaseObject to database"""
        self.__database__[self.model_class.__table_name__].append(row.as_dict())

    def bulk_insert(self, rows: Iterable):
        """Bulk Insert BaseObjects to database"""
        self.__database__[self.model_class.__table_name__] += [row.as_dict() for row in rows]

    def update(self, row, filters: Iterable[Tuple[Type, Callable]]):
        """Update BaseObject attributes in database"""
        pass

    def delete(self, filters: Iterable[Tuple[Type, Callable]]):
        """Delete BaseObject from database"""
        pass
