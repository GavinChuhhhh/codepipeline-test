# Copyright (c) GeoSprite. All rights reserved.
#
# Author: Jia Song
#


import numbers


def is_number(obj):
    return isinstance(obj, numbers.Number)


def is_string(obj):
    return isinstance(obj, str)


def is_array(obj):
    return isinstance(obj, (list, tuple)) and len(obj) > 0


def is_str_array(obj):
    if is_array(obj):
        for collection in obj:
            if not is_string(collection):
                return False
        return True if len(obj) > 0 else False
    else:
        return False


def is_bbox(obj):
    if isinstance(obj, list) and len(obj) == 4:
        for e in obj:
            if not is_number(e):
                return False
        return True
    else:
        return False


def is_geometry(obj):
    if isinstance(obj, dict) and "coordinates" in obj and "type" in obj:
        return isinstance(obj["coordinates"], list) and is_string(obj["type"])
    else:
        return False
