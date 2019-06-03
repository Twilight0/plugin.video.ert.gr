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
    ert.indexer().root()

elif action == 'addBookmark':
    from tulip import bookmarks
    bookmarks.add(url)

elif action == 'deleteBookmark':
    from tulip import bookmarks
    bookmarks.delete(url)

elif action == 'channels':
    from resources.lib import ert
    ert.indexer().channels()

elif action == 'bookmarks':
    from resources.lib import ert
    ert.indexer().bookmarks()

elif action == 'categories':
    from resources.lib import ert
    ert.indexer().categories()

elif action == 'episodes':
    from resources.lib import ert
    ert.indexer().episodes(url)

elif action == 'recent':
    from resources.lib import ert
    ert.indexer().recent()

elif action == 'live':
    from resources.lib import ert
    ert.indexer().live(url)

elif action == 'radios':
    from resources.lib import ert
    ert.indexer().radios()

elif action == 'radio':
    from resources.lib import ert
    ert.indexer().radio(url)

elif action == 'district':
    from resources.lib import ert
    ert.indexer().district()

elif action == 'search':
    from resources.lib import ert
    ert.indexer().search()

elif action == 'play':
    from resources.lib import ert
    ert.indexer().play(url)

elif action == 'cache_clear':
    from tulip import cache
    cache.clear(withyes=False)

elif action == 'yt_settings':
    from tulip import control
    control.openSettings(id='plugin.video.youtube')
