#!/usr/bin/env python3


class EnumMeta(type):
    def __new__(cls, name, bases, dct):
        _ignore_ = ('__main__', '__module__', '__doc__', '__new__',
                    '__qualname__', '__init__', '__str__')
        _member_to_map_ = {}
        _value2member_map_ = {}
        metacls = cls.__class__
        for key in dct.keys():
            if key not in _ignore_:
                attr_name = str(key)
                attr_val = dct[key]
                if attr_val not in _value2member_map_.keys():
                    # if there is no attribute names assigned to
                    # this value
                    _value2member_map_[attr_val] = attr_name
                    _member_to_map_[attr_name] = attr_val
                    dct[key] = metacls.__new__(cls, key, bases,
                                               {'name': attr_name,
                                                'value': attr_val,
                                                '__objclass__': name}
                                               )
                else:
                    # if value is already in one of Enum attributes
                    # create link to it's instance instead of
                    # instantiating a new Enum object
                    dct[key] = dct[_value2member_map_[attr_val]]

        dct['_value2member_map_'] = _value2member_map_
        dct['_member_to_map_'] = _member_to_map_
        return super().__new__(cls, name, bases, dct)

    def __setattr__(cls, name, value):
        raise AttributeError('Cannot reassign members')

    def __iter__(cls):
        yield sorted([member for member in cls._member_to_map_.values()])

    def __getitem__(cls, key):
        return cls.__dict__[key]

    def __repr__(cls):
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


class Direction(Enum):
    north = 0
    east = 90
    south = 180
    west = 270
