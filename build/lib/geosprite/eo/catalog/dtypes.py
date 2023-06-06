# Copyright (c) GeoSprite. All rights reserved.
#
# Author: Jia Song
#


import arrow


def is_date_string(date_string):
    if isinstance(date_string, str):
        try:
            arrow.get(date_string)
            return True
        except TypeError:
            return False
    else:
        return False
