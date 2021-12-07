# -*- coding: utf-8 -*-

'''
    ERTflix Addon
    Author Twilight0

    SPDX-License-Identifier: GPL-3.0-only
    See LICENSES/GPL-3.0-only for more information.
'''

from __future__ import absolute_import

import json
from base64 import b64decode
from zlib import decompress
from .constants import SCRAMBLE, GET_REGIONS
from tulip.control import openSettings, quit_kodi
from tulip.url_dispatcher import urldispatcher
from tulip import bookmarks, cache, control, client
from youtube_registration import register_api_keys


cache_function = cache.FunctionCache().cache_function


@urldispatcher.register('clear_cache')
def clear_cache():
    cache.FunctionCache().reset_cache(notify=True)


@urldispatcher.register('settings')
def settings():
    openSettings()


@urldispatcher.register('exit_kodi')
def exit_kodi():
    quit_kodi()


@urldispatcher.register('addBookmark', ['url'])
def add_bookmark(url):
    bookmarks.add(url)


@urldispatcher.register('deleteBookmark', ['url'])
def delete_bookmark(url):
    bookmarks.delete(url)


@urldispatcher.register('clear_bookmarks')
def clear_bookmarks():

    bookmarks.clear('bookmark', withyes=True, file_=control.bookmarksFile, notify=False, label_yes_no=30025)
    control.sleep(200)
    control.refresh()


def keys_registration():

    setting = control.addon('plugin.video.youtube').getSetting('youtube.allow.dev.keys') == 'true'

    if setting:

        keys = json.loads(decompress(b64decode(SCRAMBLE)))

        register_api_keys(control.addonInfo('id'), keys['api_key'], keys['id'], keys['secret'])


def collection_post(collection, page=None, limit=48):

    if isinstance(collection, str):
        collection = [collection]

    if not page:
        page = 1

    return json.dumps({
        "platformCodename": "www", "page": page, "limit": limit, "orCollectionCodenames": collection,
        "orProductCodenames": [], "sort": [{"field": "PublishDate", "direction": 1}], "tileTypes": None,
        "productType": "", "andCategoryCodenames": [], "advancedFilters": [], "isPurchased": False
    }).replace(' ', '')


def tiles_post(tiles):

    return json.dumps({"platformCodename": "www", "requestedTiles": tiles}).replace(' ', '')


def live_post(channel_list):

    return '{"platformCodename":"www","requestedTiles":%s}' % json.dumps(channel_list).replace(' ', '')


# def search_post(query):
#
#     post = '{"platformCodename":"www","tokenValue":null,"query":"%s","queryFilters":{},"applicationTag":null}' % query
#
#     return post


@cache_function(11520)
def get_regions():

    _json = client.request(GET_REGIONS, output='json')

    regions = _json['regions']

    codenames = [r['codename'] for r in regions]

    return codenames


@cache_function(11520)
def geo_detect():

    _json = client.request('https://geoip.siliconweb.com/geo.json', output='json')

    if 'GR' in _json['country']:
        return True
