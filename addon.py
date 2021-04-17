# -*- coding: utf-8 -*-

'''
    ERTflix Addon
    Author Twilight0

    SPDX-License-Identifier: GPL-3.0-only
    See LICENSES/GPL-3.0-only for more information.
'''

from __future__ import absolute_import

from sys import argv
from tulip.compat import parse_qsl
from tulip.control import infoLabel, openSettings, quit_kodi
from tulip import bookmarks, cache
# noinspection PyUnresolvedReferences,PyProtectedMember
from resources.lib import ert

params = dict(parse_qsl(argv[2][1:]))

########################################################################################################################

action = params.get('action')
url = params.get('url')

########################################################################################################################

if 'audio' in infoLabel('Container.FolderPath') and action is None:
    action = 'radios'

if action is None:
    ert.Indexer(argv).root()

elif action == 'addBookmark':
    bookmarks.add(url)

elif action == 'deleteBookmark':
    bookmarks.delete(url)

elif action == 'clear_bookmarks':
    ert.clear_bookmarks()

elif action == 'channels':
    ert.Indexer(argv).channels()

elif action == 'bookmarks':
    ert.Indexer(argv).bookmarks()

elif action == 'index':
    ert.Indexer(argv).index()

elif action == 'sports':
    ert.Indexer(argv).sports()

elif action == 'listing':
    ert.Indexer(argv).listing(url)

elif action == 'series':
    ert.Indexer(argv).series()

elif action == 'shows':
    ert.Indexer(argv).shows()

elif action == 'kids':
    ert.Indexer(argv).kids()

elif action == 'recent':
    ert.Indexer(argv).recent()

elif action == 'radios':
    ert.Indexer(argv).radios()

elif action == 'district':
    ert.Indexer(argv).district()

elif action == 'play':
    ert.Indexer(argv).play(url)

elif action == 'youtube':
    ert.Indexer(argv).yt(url)

elif action == 'search':
    ert.Indexer(argv).search()

elif action == 'info':
    ert.meta_viewer(url)

elif action == 'cache_clear':
    cache.FunctionCache().reset_cache(notify=True)

elif action == 'settings':
    openSettings()

elif action == 'exit':
    quit_kodi()
