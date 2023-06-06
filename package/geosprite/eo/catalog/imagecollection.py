# Copyright (c) GeoSprite. All rights reserved.
#
# Author: Jia Song
#

from .. import dtypes
from .filter import Filter


class ImageCollection(Filter):

    def __init__(self, collection_id):
        super(ImageCollection, self).__init__()

        if dtypes.is_string(collection_id):
            self.id = collection_id
        else:
            self.id = None

        self._cloud_cover = None

    def cloud_cover(self, cloud_cover):

        if dtypes.is_number(cloud_cover):
            self._cloud_cover = cloud_cover
        else:
            self._cloud_cover = cloud_cover

        return self

    def stac_kwargs(self, **kwargs):
        kwargs = super(ImageCollection, self).stac_kwargs(**kwargs)

        query = {}

        if self._cloud_cover:
            query["eo:cloud_cover"] = {"lte": self._cloud_cover}

        if self.id:
            kwargs["collections"] = [self.id]

        kwargs.update({"query": query})

        return kwargs
