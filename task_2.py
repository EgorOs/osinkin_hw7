#!/usr/bin/env python3


class EnumMeta(type):
    # cls, name, ... получает потому что наследуется от type?
    def __new__(cls, name, bases, dct):
        _ignore_ = {'__main__', '__module__', '__doc__', '__new__', '__qualname__', '__init__', '__str__'}
        _member_to_map_ = {}
        _value2member_map_ = {}
        metacls = cls.__class__
        for key in dct.keys():
            if key not in _ignore_:
                attr_name = str(key)
                attr_val = dct[key]
                _member_to_map_[attr_name] = attr_val
                if attr_val not in _value2member_map_.keys():
                    # if several attributes have the same value,
                    # will be returned the first attribute name
                    # this value was assigned to
                    _value2member_map_[attr_val] = attr_name
                dct[key] = metacls.__new__(cls, key, bases, {'name':attr_name, 'value':attr_val, '__objclass__':name})

        dct['_value2member_map_'] = _value2member_map_
        dct['_member_to_map_'] = _member_to_map_
        # a = metacls.__new__(cls, 'DAAAM_DANIEL', bases, _member_to_map_)
        # for key in _member_to_map_.keys():
            # dct[key] = metacls.__new__(cls, str(key), bases, {'name':key, 'value':_member_to_map_[key]})
        # dct['d'] = a
        return super().__new__(cls, name, bases, dct)


    def __setattr__(cls, name, value):
        raise AttributeError('Cannot reassign members')

    def __getitem__(cls, key):
        return cls.__dict__[key]

    def __repr__(cls):
        # return "<enum '{}'>".format(cls.__name__)
        if cls.__dict__.get('__objclass__'):
            return '<{}.{}: {}>'.format(cls.__objclass__, cls.__name__, cls.value)
        return "<enum '{}'>".format(cls.__name__)


class Enum(metaclass=EnumMeta):

    def __new__(cls, val):
        if val not in cls._value2member_map_.keys():
            raise ValueError('{} is not a valid {}'.format(val, cls.__name__))

        else:
            key = cls._value2member_map_[val]
            return cls.__dict__[key]


# print(type(Enum))
# e = Enum()
# print(e._value2member_map_)
# Enum.a = 11

class Direction(Enum):
    north = 0
    east = 90
    south = 180
    west = 270

class jojos(Enum):
    joseph = 'joestar'
    jonathan = 'joestar'

print(jojos('joestar'))
print(id(Direction(180)))
print(id(Direction(180)))
# print(Direction._member_to_map_)
print(Direction)
print(Direction['north'])