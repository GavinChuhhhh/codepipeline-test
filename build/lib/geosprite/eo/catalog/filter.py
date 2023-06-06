# Copyright (c) GeoSprite. All rights reserved.
#
# Author: Jia Song
#

from .. import dtypes
from .dtypes import is_date_string


class Filter:

    def __init__(self):
        self._start_date = None
        self._end_date = None
        self._bbox = None
        self._geometry = None

    def start_date(self, date_string):

        if is_date_string(date_string):
            self._start_date = date_string
        else:
            self._start_date = None

        return self

    def end_date(self, date_string):

        if is_date_string(date_string):
            self._end_date = date_string
        else:
            self._end_date = None

        return self

    def bbox(self, bbox):

        if dtypes.is_bbox(bbox):
            self._bbox = bbox
        else:
            self._bbox = None

        return self

    def geometry(self, geometry):

        if dtypes.is_geometry(geometry):
            self._geometry = geometry
        else:
            self._geometry = geometry

        return self

    def shapefile(self, filename):

        if isinstance(filename, str):
            import fiona

            try:
                with fiona.open(filename, 'r') as shp:
                    self._geometry = [feature['geometry'] for feature in shp]
            except ValueError as e:
                self._geometry = None
                raise ValueError(f'Can not open file {filename}. ({e})')
        else:
            self._geometry = None

        return self

    def stac_kwargs(self, **kwargs):

        if self._start_date:
            datetime = self._start_date

            if self._end_date:
                datetime = f"{datetime}/{self._end_date}"
            else:
                datetime = f"{datetime}/.."

            kwargs["datetime"] = datetime

        if self._geometry:
            kwargs["intersects"] = self.geometry

        if self._bbox:
            kwargs["bbox"] = self._bbox

        return kwargs

    @staticmethod
    def span_dates(start: str, end: str, frame=None, interval=None):
        _start_date = start
        _end_date = end
        _date_frame = None
        _date_interval = None
        _first_date = None
        _last_date = None

        if frame is not None:
            if isinstance(interval, int):
                _date_interval = interval

            _date_frame = frame
            _first_date = start or _first_date or _start_date
            _last_date = end or _last_date or _end_date

        if _date_frame is not None:
            import arrow

            if _date_interval is None:
                return [(start.format('YYYY-MM-DD'), end.format('YYYY-MM-DD')) for start, end in
                        arrow.Arrow.span_range(_date_frame, arrow.get(_first_date).datetime,
                                               arrow.get(_last_date).datetime)]
            else:
                return [(start.format('YYYY-MM-DD'), end.format('YYYY-MM-DD')) for start, end in
                        arrow.Arrow.interval(_date_frame, arrow.get(_first_date).datetime,
                                             arrow.get(_last_date).datetime, _date_interval)]
        else:
            return [(_start_date, _end_date)]
