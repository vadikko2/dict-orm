"""Data Classes"""
from typing import Any

from orm_controllers import BaseController
from orm_types import Type


class DataObject:
    """Data class. Contains match data Type and data Value"""

    def __init__(self, type_: Type, value: Any):
        self._type_ = type_
        self._type_.validate(value)
        self._value = value

    def __repr__(self):
        return '<%s: %r>' % (self._type_.name, self._value)

    @property
    def type(self):
        return self._type_

    @property
    def value(self):
        return self._value


class MetaObject(type):
    __controller__ = BaseController

    def _get_manager(cls):
        return cls.__controller__(cls)

    @property
    def objects(cls):
        return cls._get_manager()


class BaseObject(metaclass=MetaObject):
    """Match database model and data values"""
    __attributes_value__ = None
    __model__ = None

    def __init__(self, **row_data):
        self.__model__ = self.__model__()
        self.__attributes_value__ = {}
        for field_name, value in row_data.items():
            type_ = getattr(self.__model__, field_name)
            self.__attributes_value__[field_name] = DataObject(type_=type_, value=value)

    def __repr__(self):
        attrs_format = ", ".join(
            ['%s=%r' % (attr, attr_value.value) for attr, attr_value in self.__attributes_value__.items()]
        )
        return "<%s: (%s)>" % (self.__class__.__name__, attrs_format)

    def __getattr__(self, attr):
        return self.__attributes_value__[attr]
