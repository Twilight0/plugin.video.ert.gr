# -*- coding: utf-8 -*-

'''
    ERTflix Addon
    Author Twilight0

    SPDX-License-Identifier: GPL-3.0-only
    See LICENSES/GPL-3.0-only for more information.
'''

from tulip import kodi, bookmarks
from urldispatcher import urldispatcher

try:
    from pickled import FunctionCache
    _cache = FunctionCache(kodi.cacheDirectory)
except Exception:
    _cache = None


@urldispatcher.register('clear_cache')
def clear_cache():
    if _cache is not None:
        _cache.reset_cache()
    kodi.infoDialog(kodi.i18n(30402))


@urldispatcher.register('settings')
def settings():
    kodi.openSettings()


@urldispatcher.register('exit_kodi')
def exit_kodi():
    kodi.quit_kodi()


@urldispatcher.register('addBookmark', ['url'])
def add_bookmark(url):
    bookmarks.add(url)


@urldispatcher.register('deleteBookmark', ['url'])
def delete_bookmark(url):
    bookmarks.delete(url)


@urldispatcher.register('clear_bookmarks')
def clear_bookmarks():
    bookmarks.clear(['bookmark'], path=kodi.bookmarksFile)
    kodi.sleep(200)
    kodi.refresh()
