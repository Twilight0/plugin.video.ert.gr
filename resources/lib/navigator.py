# -*- coding: utf-8 -*-

'''
    ERTflix Addon
    Author Twilight0

    SPDX-License-Identifier: GPL-3.0-only
    See LICENSES/GPL-3.0-only for more information.
'''

from __future__ import absolute_import

import json, re
from .constants import *
from .utils import geo_detect
from tulip import bookmarks as bms, directory, client, cache, control
from tulip.compat import iteritems, range, concurrent_futures
from tulip.parsers import parseDOM
from tulip.url_dispatcher import urldispatcher
from youtube_resolver import resolve as yt_resolver


cache_function = cache.FunctionCache().cache_function


# @cache_function(5760)
# def _plot(url):
#
#     pass
#
#
# def meta_viewer(url):
#
#     heading = control.infoLabel('Listitem.Label')
#
#     control.dialog.textviewer(heading=heading, text=_plot(url))


@urldispatcher.register('root')
def root():

    menu = [
        {
            'title': control.lang(30001),
            'action': 'live',
            'icon': 'channels.jpg'
        }
        ,
        # {
        #     'title': control.lang(30002),
        #     'action': 'recent',
        #     'icon': 'recent.jpg'
        # }
        # ,
        {
            'title': control.lang(30015),
            'action': 'enter_yt_channel',
            'icon': 'youtube.jpg',
            'url': ''.join(
                ['plugin://plugin.video.youtube/channel/', CHANNEL_ID, '/?addon_id=', control.addonInfo('id')]
            ),
            'isFolder': 'False', 'isPlayable': 'False'
        }
        # ,
        # {
        #     'title': control.lang(30011),
        #     'action': 'index',
        #     'icon': 'index.jpg'
        # }
        # ,
        # {
        #     'title': control.lang(30004),
        #     'action': 'listing',
        #     'url': NEWS_LINK,
        #     'icon': 'news.jpg'
        # }
        # ,
        # {
        #     'title': control.lang(30049),
        #     'action': 'listing',
        #     'icon': 'movies.jpg',
        #     'url': MOVIES_LINK
        # }
        # ,
        # {
        #     'title': control.lang(30020),
        #     'action': 'shows',
        #     'icon': 'shows.jpg'
        # }
        # ,
        # {
        #     'title': control.lang(30038),
        #     'action': 'series',
        #     'icon': 'series.jpg'
        # }
        # ,
        # {
        #     'title': control.lang(30003),
        #     'action': 'listing',
        #     'url': SPORTS_LINK,
        #     'icon': 'sports.jpg'
        # }
        # ,
        # {
        #     'title': control.lang(30009),
        #     'action': 'music',
        #     'icon': 'music.jpg'
        # }
        # ,
        # {
        #     'title': control.lang(30060),
        #     'action': 'kids',
        #     'icon': 'kids.jpg'
        # }
        # ,
        # {
        #     'title': control.lang(30055),
        #     'action': 'listing',
        #     'url': ARCHIVE_LINK,
        #     'icon': 'archive.jpg'
        # }
        # ,
        # {
        #     'title': control.lang(30013),
        #     'action': 'search',
        #     'icon': 'search.jpg',
        #     'isFolder': 'False', 'isPlayable': 'False'
        # }
        ,
        {
            'title': control.lang(30012),
            'action': 'bookmarks',
            'icon': 'bookmarks.jpg'
        }
        ,
        {
            'title': control.lang(30026),
            'action': 'radios',
            'icon': 'radio.jpg'
        }
    ]

    settings_menu = {
            'title': control.lang(30044),
            'action': 'settings',
            'icon': 'settings.jpg',
            'isFolder': 'False', 'isPlayable': 'False'
        }

    exit_button = {
        'title': control.lang(30048),
        'action': 'exit',
        'icon': 'exit.jpg',
        'isFolder': 'False', 'isPlayable': 'False'
    }

    if control.setting('settings_boolean') == 'true':
        menu.append(settings_menu)

    if control.setting('show_exit') == 'true':
        menu.append(exit_button)

    for item in menu:

        clear_cache = {'title': 30036, 'query': {'action': 'clear_cache'}}
        settings = {'title': 30039, 'query': {'action': 'settings'}}
        item.update({'cm': [clear_cache, settings]})

    directory.add(menu, content='videos')


@urldispatcher.register('bookmarks')
def bookmarks():

    self_list = bms.get()

    if not self_list:
        na = [{'title': control.lang(30058), 'action': None}]
        directory.add(na)
        return

    for i in self_list:
        bookmark = dict((k, v) for k, v in iteritems(i) if not k == 'next')
        bookmark['delbookmark'] = i['url']
        i.update({'cm': [{'title': 30502, 'query': {'action': 'deleteBookmark', 'url': json.dumps(bookmark)}}]})

    if control.setting('bookmarks_clear_boolean') == 'true':

        clear_menu = {
            'title': control.lang(30059), 'action': 'clear_bookmarks', 'isFolder': 'False', 'isPlayable': 'False'
        }

        self_list.insert(0, clear_menu)

    control.sortmethods()
    control.sortmethods('title')

    directory.add(self_list, content='videos')


@cache_function(3600)
def get_live():

    FilterNowOnTvTiles = client.request(FILTER_NOW_ON_TV_TILES, output='json')

    channels = FilterNowOnTvTiles['Channels']

    fnotvtiles_channel_list = []

    for channel in channels:

        c = {'id': channel['Id']}
        fnotvtiles_channel_list.append(c)

    post = '{"platformCodename":"www","requestedTiles":%s}' % json.dumps(fnotvtiles_channel_list).replace(' ', '')

    GetTiles = client.request(GET_TILES, post=post, output='json')

    stations = GetTiles['tiles']

    self_list = []

    for station in stations:

        title = station['title']
        image = station['images'][0]['url']
        fanart = station['images'][1]['url']
        try:
            codename = station['tileChannel']['codename']
        except KeyError:
            codename = station['codename']
        acquire_content = client.request(ACQUIRE_CONTENT.format(DEVICE_KEY, codename), output='json')
        url = acquire_content['MediaFiles'][0]['Formats'][0]['Url']

        data = {'title': title.replace(' LIVE', ''), 'image': image, 'fanart': fanart, 'url': url}

        self_list.append(data)

    return self_list


@urldispatcher.register('live')
def live():

    self_list = get_live()

    for i in self_list:
        i.update({'action': 'play', 'isFolder': 'false'})

    directory.add(self_list)


@urldispatcher.register('radios')
def radios():

    images = [
        ''.join([RADIO_LINK, i]) for i in [
            '/wp-content/uploads/2016/06/proto.jpg', '/wp-content/uploads/2016/06/deytero.jpg',
            '/wp-content/uploads/2016/06/trito.jpg', '/wp-content/uploads/2016/06/kosmos.jpg',
            '/wp-content/uploads/2016/06/VoiceOgGreece.png', '/wp-content/uploads/2016/06/eraSport.jpg',
            '/wp-content/uploads/2016/06/958fm.jpg', '/wp-content/uploads/2016/06/102fm.jpg'
        ]
    ]

    names = [control.lang(n) for n in list(range(30028, 30036))]

    urls = [
        ''.join([RADIO_STREAM, i]) for i in [
            '/ert-proto', '/ert-deftero', '/ert-trito', '/ert-kosmos', '/ert-voiceofgreece', '/ert-erasport',
            '/ert-958fm', '/ert-102fm'
        ]
    ]

    _radios = map(lambda x, y, z: (x, y, z), names, images, urls)

    self_list = []

    for title, image, link in _radios:

        self_list.append(
            {
                'title': title, 'url': link, 'image': image, 'action': 'play', 'isFolder': 'False',
                'fanart': control.addonmedia('radio_fanart.jpg')
            }
        )

    _district = {
        'title': control.lang(30027), 'action': 'district', 'icon': 'district.jpg',
        'fanart': control.addonmedia('radio_fanart.jpg')
    }

    self_list.append(_district)

    directory.add(self_list)


def _radio_loop(station):

    title = parseDOM(station, 'a')[0]
    href = parseDOM(station, 'a', ret='href')[0]
    html = client.request(href, as_bytes=True)
    html = html.decode('windows-1253')
    link = parseDOM(html, 'iframe', ret='src')[0]
    embed = client.request(link)
    url = re.search(r'mp3: [\'"](.+?)[\'"]', embed).group(1).replace('https', 'http')
    image = parseDOM(html, 'img', ret='src')[0]

    data = {'title': title, 'image': image, 'url': url}

    return data


@cache_function(5760)
def district_list():

    result = client.request(DISTRICT_LINK, as_bytes=True)
    result = result.decode('windows-1253')
    _radios = parseDOM(result, 'td')
    stations = [r for r in _radios if r]

    self_list = []

    with concurrent_futures.ThreadPoolExecutor(5) as executor:

        threads = [executor.submit(_radio_loop, station) for station in stations]

        for future in concurrent_futures.as_completed(threads):

            item = future.result()

            if not item:
                continue

            self_list.append(item)

    return self_list


@urldispatcher.register('district')
def district():

    self_list = district_list()

    for i in self_list:
        i.update({'action': 'play', 'isFolder': 'False', 'fanart': control.addonmedia('radio_fanart.jpg')})

    directory.add(self_list)


def yt_session(yt_id):

    streams = yt_resolver(yt_id)

    try:
        addon_enabled = control.addon_details('inputstream.adaptive').get('enabled')
    except KeyError:
        addon_enabled = False

    if not addon_enabled:

        streams = [s for s in streams if 'mpd' not in s['title'].lower()]

    stream = streams[0]['url']

    return stream


@urldispatcher.register('enter_yt_channel', ['url'])
def enter_yt_channel(url):

    control.execute('Container.Update({},return)'.format(url))
