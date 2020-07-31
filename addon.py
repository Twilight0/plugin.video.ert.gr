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
from tulip.control import infoLabel, bookmarksFile, refresh, sleep, openSettings
from tulip import bookmarks, cache
# noinspection PyUnresolvedReferences
from resources.lib import ert

syshandle = int(argv[1])
sysaddon = argv[0]
params = dict(parse_qsl(argv[2][1:]))

########################################################################################################################

action = params.get('action')
url = params.get('url')

########################################################################################################################

if 'audio' in infoLabel('Container.FolderPath') and action is None:
    action = 'radios'

if action is None:
    ert.Indexer().root()

elif action == 'addBookmark':
    bookmarks.add(url)

elif action == 'deleteBookmark':
    bookmarks.delete(url)

elif action == 'clear_bookmarks':
    bookmarks.clear('bookmark', withyes=True, file_=bookmarksFile, notify=False, label_yes_no=30025)
    sleep(200)
    refresh()

elif action == 'channels':
    ert.Indexer().channels()

elif action == 'bookmarks':
    ert.Indexer().bookmarks()

elif action == 'index':
    ert.Indexer().index()

elif action == 'sports':
    ert.Indexer().sports()

elif action == 'listing':
    ert.Indexer().listing(url)

elif action == 'series':
    ert.Indexer().series()

elif action == 'shows':
    ert.Indexer().shows()

elif action == 'kids':
    ert.Indexer().kids()

elif action == 'recent':
    ert.Indexer().recent()

elif action == 'radios':
    ert.Indexer().radios()

elif action == 'district':
    ert.Indexer().district()

elif action == 'play':
    ert.Indexer().play(url)

elif action == 'youtube':
    ert.Indexer().yt(url)

elif action == 'search':
    ert.Indexer().search()

elif action == 'cache_clear':
    cache.clear(withyes=False)

elif action == 'settings':
    openSettings()
