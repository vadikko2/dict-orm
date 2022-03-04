"""Data models classes"""
from typing import Type

from orm_controllers import BaseController
from orm_objects import BaseObject


class BaseModel:
    """Describe data model"""
    __slots__ = ('__tablename__',)

    @classmethod
    def get_object(cls, controller: Type[BaseController]) -> Type[BaseObject]:
        """Return BaseObject instance, generated for described data Model"""
        BaseObject.__controller__ = controller
        BaseObject.__model__ = cls
        return BaseObject
