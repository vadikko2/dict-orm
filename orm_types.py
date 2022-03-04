"""Types Classes"""
from abc import ABC, abstractmethod


class Validator(ABC):
    """Data validator"""

    def __init__(self, name: str):
        self._name = name

    @property
    def name(self):
        return self._name

    @abstractmethod
    def validate(self, value):
        pass


class Type(Validator):
    """Validated type"""
    _type_ = object

    def validate(self, value):
        if not isinstance(value, self._type_):
            raise ValueError('%r is not instance of %s' % (value, self._type_))

    def __repr__(self):
        return '<%s: %r>' % (self.name, self._type_)

    def __hash__(self):
        return hash(repr(self))


class Str(Type):
    """Validated string"""
    _type_ = str


class Int(Type):
    """Validated number"""
    _type_ = int


class Age(Int):
    """Validated age number"""

    def validate(self, value):
        super(Age, self).validate(value)
        if not (0 < value <= 120):
            raise ValueError('The value %s can`t be age.' % value)
