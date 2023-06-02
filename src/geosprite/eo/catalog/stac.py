# Copyright (c) GeoSprite. All rights reserved.
#
# Author: Jia Song
#

from pystac_client import Client, exceptions

from .. import dtypes
from .imagecollection import ImageCollection


class Catalog:
    api_retries = 5

    def __init__(self, stac_api_url):
        self.stac_api_url = stac_api_url
        self.client = Client.open(stac_api_url)

    def search(self, collection_id, start_date=None, end_date=None, cloud_cover=None, bbox=None, assets=(),
               sortby=None):

        collection = ImageCollection(collection_id) \
            .start_date(start_date) \
            .end_date(end_date) \
            .cloud_cover(cloud_cover) \
            .bbox(bbox)

        retries = 0

        while retries < self.api_retries:

            try:
                items = []

                for item in self.client.search(**collection.stac_kwargs(sortby=sortby)).items():
                    if dtypes.is_str_array(assets):
                        item.assets = {k: item.assets[k] for k in assets}

                    items.append(item)

                return items

            except exceptions.APIError as e:
                import warnings

                retries = retries + 1
                warnings.warn(f"Search collection '{collection_id}' failed. Caused by {e}. Retrying ... {retries}/5.")

    def search_item(self, collection_id, item_id, assets=()):
        retries = 0

        while retries < self.api_retries:

            try:
                item = self.client.get_collection(collection_id).get_item(item_id)

                if dtypes.is_str_array(assets):
                    keys = item.assets.keys()
                    item.assets = {k: item.assets[k] for k in assets if k in keys}

                return item

            except exceptions.APIError as e:
                import warnings

                retries = retries + 1
                warnings.warn(f"Get item '{item_id}' failed. Caused by {e}. Retrying ... {retries}/5.")
