#!/usr/bin/env python3


class EnumMeta(type):
    # cls, name, ... получает потому что наследуется от type?
    def __new__(cls, name, bases, dct):
        _ignore_ = {'__main__', '__module__', '__doc__', '__new__', '__qualname__', '__init__', '__str__'}
        _member_to_map_ = {}
        _value2member_map_ = {}
        for key in dct.keys():
            if key not in _ignore_:
                attr_name = key
                attr_val = dct[key]
                _member_to_map_[attr_name] = attr_val
                _value2member_map_[attr_val] = attr_name
        dct['_value2member_map_'] = _value2member_map_
        dct['_member_to_map_'] = _member_to_map_
        return super().__new__(cls, name, bases, dct)

    def __setattr__(cls, name, value):
        raise AttributeError('Cannot reassign members')


    def __repr__(cls):
        return "<enum '{}'>".format(cls.__name__)

class Enum(metaclass=EnumMeta):

    def __new__(cls, member=None):
        # if member not in cls._member_to_map_.keys():
        #     raise ValueError('{} is not a valid {}'.format(member, cls.__name__))
        # else:
        #     return cls._member_to_map_[member]
        # # super().__init__()
        # for member in cls._member_to_map_.keys():

        return super().__new__(cls)

    def __init__(self, member=None):
        pass

    name = None
    value = None

print(type(Enum))
# e = Enum()
# print(e._value2member_map_)
# Enum.a = 11

class Direction(Enum):
    north = 0
    east = 90
    south = 180
    west = 270

print(type(Direction.north))
print(Direction.__dict__)