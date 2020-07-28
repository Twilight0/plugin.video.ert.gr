# -*- coding: utf-8 -*-

'''
    ERTflix Addon
    Author Twilight0

    SPDX-License-Identifier: GPL-3.0-only
    See LICENSES/GPL-3.0-only for more information.
'''


import json
from tulip.bookmarks import add
from tulip.control import get_info_label, transPath

url = {
    'title': get_info_label('ListItem.Label'), 'image': get_info_label('ListItem.Art(thumb)'),
    'fanart': get_info_label('ListItem.Art(fanart)'), 'plot': get_info_label('ListItem.Plot'),
    'bookmark': get_info_label('ListItem.FolderPath'), 'url': get_info_label('ListItem.FolderPath')
}

if 'playlist' not in url['url']:
    url.update({'action': 'play', 'isFolder': 'False'})
else:
    url.update({'action': 'youtube', 'isFolder': 'False', 'isPlayable': 'False'})

path = transPath('special://profile/addon_data/plugin.video.ert.gr/bookmarks.db')

add(json.dumps(url), path)
