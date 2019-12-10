# -*- coding: utf-8 -*-

'''
    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
'''
from __future__ import absolute_import

from sys import argv
from tulip.compat import parse_qsl
from tulip.control import infoLabel

syshandle = int(argv[1])
sysaddon = argv[0]
params = dict(parse_qsl(argv[2].replace('?','')))

########################################################################################################################

action = params.get('action')
url = params.get('url')

########################################################################################################################

if 'audio' in infoLabel('Container.FolderPath') and action is None:
    action = 'radios'

if action is None:
    from resources.lib import ert
    ert.Indexer().root()

elif action == 'addBookmark':
    from tulip import bookmarks
    bookmarks.add(url)

elif action == 'deleteBookmark':
    from tulip import bookmarks
    bookmarks.delete(url)

elif action == 'channels':
    from resources.lib import ert
    ert.Indexer().channels()

elif action == 'bookmarks':
    from resources.lib import ert
    ert.Indexer().bookmarks()

elif action == 'index':
    from resources.lib import ert
    ert.Indexer().index()

elif action == 'sports':
    from resources.lib import ert
    ert.Indexer().sports()

elif action == 'episodes':
    from resources.lib import ert
    ert.Indexer().episodes(url)

elif action == 'series':
    from resources.lib import ert
    ert.Indexer().series()

elif action == 'series_episodes':
    from resources.lib import ert
    ert.Indexer().series_episodes(url)

elif action == 'recent':
    from resources.lib import ert
    ert.Indexer().recent()

elif action == 'radios':
    from resources.lib import ert
    ert.Indexer().radios()

elif action == 'district':
    from resources.lib import ert
    ert.Indexer().district()

elif action == 'play':
    from resources.lib import ert
    ert.Indexer().play(url)

elif action == 'cache_clear':
    from tulip import cache
    cache.clear(withyes=False)
