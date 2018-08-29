#!/usr/bin/env python3


class EnumMeta(type):
    def __new__(cls, name, bases, dct):
        _valid_ = [n for n in dct.keys() if str(n)[:2] != '__' and str(n)[::-1][:2] != '__']
        _member_to_map_ = {}
        _value2member_map_ = {}
        metacls = cls.__class__
        
        for key in _valid_:
            attr_name = str(key)
            attr_val = dct[key]
            if attr_val not in _value2member_map_.keys():
                # if there is no attribute names assigned to
                # this value
                _value2member_map_[attr_val] = attr_name
                _member_to_map_[attr_name] = attr_val
            else:
                dct[key] = dct[_value2member_map_[attr_val]]

        for key in _valid_:
            dct[key] = metacls.__new__(cls, key, bases,
                                       {'name': attr_name,
                                        'value': attr_val,
                                        '__objclass__': name,
                                        '_value2member_map_':_value2member_map_,
                                        '_member_to_map_':_member_to_map_}
                                       )
            # create an instance with valid value
            dct[key] = dct[key](_member_to_map_[key])

        dct['_value2member_map_'] = _value2member_map_
        dct['_member_to_map_'] = _member_to_map_
        return super().__new__(cls, name, bases, dct)

    def __setattr__(cls, name, value):
        raise AttributeError('Cannot reassign members')

    def __iter__(cls):
        return iter(cls._member_to_map_.values())

    def __getitem__(cls, key):
        return cls.__dict__[key]

    def __repr__(cls):
        if cls.__dict__.get('__objclass__'):
            return '<{}.{}: {}>'.format(cls.__objclass__, cls.__name__, cls.value)
        return "<enum '{}'>".format(cls.__name__)


class Enum(metaclass=EnumMeta):

    def __new__(cls, val):
        if val in cls._value2member_map_.keys():
            key = cls._value2member_map_.get(val)
            if not isinstance(cls._member_to_map_.get(key), __class__):
                # create instance only once to preserve same ID
                new_enum = object.__new__(__class__)
                new_enum.__objclass__ = cls.__objclass__
                new_enum.name = key
                new_enum.value = val
                cls._member_to_map_[key] = new_enum
            return cls._member_to_map_[key]
        else:
            raise ValueError('{} is not a valid {}'.format(val, cls.__name__))

    def __str__(self):
            return '<{}.{}: {}>'.format(self.__objclass__, self.name, self.value)


class Direction(Enum):
    north = 0
    east = 90
    south = 180
    west = 270


# for d in Direction:
#     print(d)

# print(id(Direction.north))
# print(id(Direction['north']))
# print(id(Direction(0)))