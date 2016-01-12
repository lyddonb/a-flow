import re

from collections import namedtuple


first_cap_re = re.compile('(.)([A-Z][a-z]+)')
all_cap_re = re.compile('([a-z0-9])([A-Z])')

def _convert(name):
    s1 = first_cap_re.sub(r'\1_\2', name)
    return all_cap_re.sub(r'\1_\2', s1).lower()


def build_tuple(obj_name, schema, obj_map):
    properties = {}

    for key, value in schema.iteritems():
        lower_name = _convert(key)
        map_value = obj_map.get(key)

        # Is an object itself and needs converted to a tuple
        if isinstance(value, dict):
            # If there's a result passed in, otherwise it will be none.
            if map_value:

                # Can't use only python capitalize because it lowers the rest of
                # the string :(
                map_value = build_tuple(
                    key[0].capitalize() + key[1:], value, obj_map.get(key, {}))

        properties[lower_name] = map_value

    obj = namedtuple(obj_name, properties.keys())
    obj.__new__.__defaults__ = (None,) * len(obj._fields)

    return obj(**properties)
