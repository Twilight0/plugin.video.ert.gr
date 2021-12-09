# -*- coding: utf-8 -*-

'''
    ERTflix Addon
    Author Twilight0

    SPDX-License-Identifier: GPL-3.0-only
    See LICENSES/GPL-3.0-only for more information.
'''

from __future__ import absolute_import

import json, re
from os.path import split
from .constants import *
from .utils import geo_detect, collection_post, tiles_post, live_post, search_post
from tulip import bookmarks as bms, directory, client, cache, control
from tulip.compat import iteritems, range, concurrent_futures, quote, parse_qs
from tulip.parsers import parseDOM, itertags
from tulip.url_dispatcher import urldispatcher
from youtube_resolver import resolve as yt_resolver


cache_function = cache.FunctionCache().cache_function


@urldispatcher.register('root')
def root():

    menu = [
        {
            'title': control.lang(30001),
            'action': 'live',
            'icon': 'channels.jpg'
        }
        ,
        {
            'title': control.lang(30002),
            'action': 'listing',
            'url': 'vods',
            'icon': 'recent.jpg'
        }
        ,
        {
            'title': control.lang(30015),
            'action': 'enter_yt_channel',
            'icon': 'youtube.jpg',
            'url': ''.join(
                ['plugin://plugin.video.youtube/channel/', CHANNEL_ID, '/?addon_id=', control.addonInfo('id')]
            ),
            'isFolder': 'False', 'isPlayable': 'False'
        }
        ,
        {
            'title': control.lang(30004),
            'action': 'listing',
            'url': NEWS_LINK,
            'icon': 'news.jpg'
        }
        ,
        {
            'title': control.lang(30049),
            'action': 'listing' if control.setting('nest_movies') == 'false' else 'categories',
            'icon': 'movies.jpg',
            'url': MOVIES_LINK
        }
        ,
        {
            'title': control.lang(30020),
            'action': 'categories',
            'url': SHOWS_LINK,
            'icon': 'shows.jpg'
        }
        ,
        {
            'title': control.lang(30038),
            'action': 'categories',
            'url': SERIES_LINK,
            'icon': 'series.jpg'
        }
        ,
        {
            'title': control.lang(30017),
            'action': 'listing' if control.setting('nest_movies') == 'false' else 'categories',
            'icon': 'documentaries.jpg',
            'url': DOCUMENTARIES_LINK
        }
        ,
        {
            'title': control.lang(30003),
            'action': 'categories',
            'url': SPORTS_LINK,
            'icon': 'sports.jpg'
        }
        ,
        {
            'title': control.lang(30005),
            'action': 'categories',
            'url': INFO_LINK,
            'icon': 'interviews.jpg'
        }
        ,
        {
            'title': control.lang(30055),
            'action': 'categories',
            'url': ARCHIVE_LINK,
            'icon': 'archive.jpg'
        }
        ,
        {
            'title': control.lang(30060),
            'action': 'categories',
            'url': KIDS_LINK,
            'icon': 'kids.jpg'
        }
        ,
        {
            'title': control.lang(30019),
            'action': 'index',
            'icon': 'index.jpg'
        }
        ,
        # {
        #     'title': control.lang(30013),
        #     'action': 'search',
        #     'icon': 'search.jpg',
        #     'isFolder': 'False', 'isPlayable': 'False'
        # }
        # ,
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
        'action': 'exit_kodi',
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

    GetTiles = client.request(GET_TILES, post=live_post(fnotvtiles_channel_list), output='json')

    stations = GetTiles['tiles']

    self_list = []

    for station in stations:

        if station['isRegionRestrictionEnabled'] and not geo_detect:
            continue

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


@cache_function(2880)
def index_listing():

    html = client.request(INDEX_LINK)

    li = parseDOM(html, 'li')

    li.extend(parseDOM(html, 'li', attrs={'class': 'hideli'}))

    items = [i for i in li if 'title' in i]

    self_list = []

    for item in items:

        title = client.replaceHTMLCodes(parseDOM(item, 'a')[0])
        url = parseDOM(item, 'a', ret='href')[0]

        self_list.append({'title': title, 'url': url})

    self_list.sort(key=lambda k: k['title'].lower())

    return self_list


@urldispatcher.register('index')
def index():

    try:
        self_list = index_listing()
    except Exception:
        return

    for i in self_list:
        i.update({'action': 'sub_index'})

    for i in self_list:
        bookmark = dict((k, v) for k, v in iteritems(i) if not k == 'next')
        bookmark['bookmark'] = i['url']
        i.update({'cm': [{'title': 30006, 'query': {'action': 'addBookmark', 'url': json.dumps(bookmark)}}]})

    directory.add(self_list, content='videos')


@urldispatcher.register('sub_index', ['url'])
def sub_index(url):

    self_list = sub_index_listing(url)

    for i in self_list:
        try:
            bookmark = dict((k, v) for k, v in iteritems(i) if not k == 'next')
            bookmark['bookmark'] = i['url']
            bookmark['title'] = i['title'].rpartition(' - ')[0]
            i.update({'cm': [{'title': 30501, 'query': {'action': 'addBookmark', 'url': json.dumps(bookmark)}}]})
        except KeyError:
            pass

    directory.add(self_list, content='videos')


@cache_function(3600)
def sub_index_listing(url):

    html = client.request(url)

    name = client.parseDOM(html, 'h1', attrs={'class': 'tdb-title-text'})[0]

    links = [l for l in list(itertags(html, 'a')) if 'su-button' in l.attributes.get('class', '')]

    if not links:
        links = [l for l in list(itertags(html, 'a')) if l.text and u'Επεισόδια' in l.text]

    description = client.replaceHTMLCodes(client.stripTags(client.parseDOM(html, 'div', attrs={'class': 'tdb-block-inner td-fix-index'})[-2]))

    if '</div>' in description:
        description = client.stripTags(description.partition('</div>')[2])
    else:
        description = client.stripTags(description)

    image_div = [i for i in list(itertags(html, 'div')) if 'sizes' in i.text]
    image = re.search(r'w, (http.+?\.(?:jpg|png)) 300w', image_div[0].text).group(1)
    fanart = re.search(r'(http.+?\.(?:jpg|png))', image_div[0].text).group(1)

    self_list = []

    for link in links:

        title = ' - '.join([name, client.stripTags(link.text).strip()])
        url = client.replaceHTMLCodes(link.attributes['href'])

        action = 'listing'

        if 'series' in link.attributes['href']:
            url = split(url)[1].split('-')[0]
            url = GET_SERIES_DETAILS.format(url)
        elif 'vod' in link.attributes['href']:
            action = 'play'

        data = {'title': title, 'url': url, 'image': image, 'fanart': fanart, 'plot': description, 'action': action}

        if data['action'] == 'play':
            data.update({'title': name, 'label': title, 'isFolder': 'False'})

        self_list.append(data)

    if not self_list:
        self_list.append({
        'title': ''.join([name, ' - ', control.lang(30022)]), 'action': 'read_plot', 'isFolder': 'False',
        'isPlayable': 'False', 'plot': description, 'image': image, 'fanart': fanart
    })

    plot_item = {
        'title': ''.join(['[B]', name, ' - ', control.lang(30021), '[/B]']), 'action': 'read_plot', 'isFolder': 'False',
        'isPlayable': 'False', 'plot': description, 'image': image, 'fanart': fanart
    }

    self_list.append(plot_item)

    return self_list


@urldispatcher.register('read_plot')
def read_plot():

    heading = control.infoLabel('Listitem.Title')
    plot = control.infoLabel('Listitem.Plot')

    control.dialog.textviewer(heading=heading, text=plot)


@cache_function(1800)
def list_items(url):

    page = 1

    if url.startswith('https'):

        if BASE_API_LINK not in url:
            html = client.request(url)
            script = client.parseDOM(html, 'script')[0]
            _json = json.loads(script.replace('var ___INITIAL_STATE__ = ', '')[:-1])
        else:
            _json = client.request(url, output='json')

        if '/list' in url:

            codename = split(url)[1].partition('=')[2]
            total_pages = _json['pages']['sectionsByCodename'][codename]['totalPages']
            page = _json['pages']['sectionsByCodename'][codename]['fetchedPage']
            tiles = _json['pages']['sectionsByCodename'][codename]['tilesIds']
            tiles_post_list = [{'id': i} for i in tiles]

        else:

            tiles = []
            if 'GetSeriesDetails' in url:

                episode_groups = _json['episodeGroups']

                for group in episode_groups:
                    episodes = group['episodes']
                    for episode in episodes:
                        codename = episode['id']
                        tiles.append(codename)

                tiles_post_list = [{'id': i} for i in tiles]
                total_pages = 1

            else:

                codenames = list(_json['pages']['sectionsByCodename'].keys())
                for codename in codenames:
                    tiles_list = _json['pages']['sectionsByCodename'][codename]['tilesIds']
                    tiles.extend(tiles_list)
                tiles_post_list = [{'id': i} for i in tiles]
                total_pages = 1

    else:

        if url.startswith('{"platformCodename":"www"'):
            collection_json = json.loads(url)
            url = collection_json['orCollectionCodenames']
            page = collection_json['page']

        filter_tiles = client.request(FILTER_TILES, post=collection_post(url, page), output='json')
        total_pages = filter_tiles['pagination']['totalPages']
        page = filter_tiles['pagination']['page']
        tiles = filter_tiles['tiles']
        tiles_post_list = [{'id': i['id']} for i in tiles]

    if total_pages > 1 and page < total_pages:
        page = page + 1
        next_post = collection_post(url, page)
    else:
        next_post = None

    get_tiles = client.request(GET_TILES, post=tiles_post(tiles_post_list), output='json')
    tiles_list = get_tiles['tiles']

    self_list = []

    for tile in tiles_list:

        if tile['isRegionRestrictionEnabled'] and not geo_detect:
            continue

        title = tile['title']
        if 'subtitle' in tile:
            title = ' - '.join([title, tile['subtitle']])
        try:
            if tile.get('isEpisode'):
                try:
                    season = ' '.join([control.lang(30063), str(tile['season']['seasonNumber'])])
                except KeyError:
                    season = None
                if not season:
                    subtitle = ' '.join([control.lang(30064), str(tile['episodeNumber'])])
                else:
                    try:
                        subtitle = ''.join(
                            [
                                season, ', ', control.lang(30064),
                                ' ', str(tile['episodeNumber'])
                            ]
                        )
                    except KeyError:
                        subtitle = tile['publishDate'].partition('T')[0]
                        subtitle = '/'.join(subtitle.split('-')[::-1])
                title = '[CR]'.join([title, subtitle])
        except Exception:
            pass
        images = tile['images']
        if len(images) == 1:
            image = images[0]['url']
            fanart = control.fanart()
        else:
            try:
                image = [i['url'] for i in images if i['isMain']][0]
            except IndexError:
                try:
                    image = [i['url'] for i in images if i['role'] == 'hbbtv-icon'][0]
                except IndexError:
                    try:
                        image = [i['url'] for i in images if i['role'] == 'photo'][0]
                    except IndexError:
                        image = [i['url'] for i in images if i['role'] == 'hbbtv-background'][0]
            try:
                fanart = [i['url'] for i in images if i['role'] == 'photo-details'][0]
            except IndexError:
                try:
                    fanart = [i['url'] for i in images if i['role'] == 'hbbtv-background'][1]
                except IndexError:
                    try:
                        fanart = [i['url'] for i in images if i['role'] == 'hbbtv-background'][0]
                    except IndexError:
                        fanart = [i['url'] for i in images if i['role'] == 'photo' and 'ertflix-background' in i['url']][0]
        codename = tile['codename']
        vid = tile['id']
        plot = tile['shortDescription']
        year = tile.get('year')
        if not year:
            year = 2021

        if tile.get('hasPlayableStream'):
            url = VOD_LINK.format('-'.join([vid, codename]))
        else:
            url = GET_SERIES_DETAILS.format(vid)

        data = {
            'title': title, 'image': image, 'fanart': fanart, 'url': url, 'plot': plot,
            'year': year
        }

        if tile.get('durationSeconds'):
            data.update({'duration': tile.get('durationSeconds')})

        if next_post:
            data.update(
                {
                    'next': next_post, 'nextaction': 'listing', 'nextlabel': 30500,
                    'nexticon': control.addonmedia('next.jpg')
                }
            )

        if tile.get('hasPlayableStream'):
            data.update({'action': 'play', 'isFolder': 'False'})
        else:
            data.update({'action': 'listing'})

        self_list.append(data)

    return self_list


@urldispatcher.register('listing', ['url'])
def listing(url):

    self_list = list_items(url)

    for i in self_list:
        bookmark = dict((k, v) for k, v in iteritems(i) if not k == 'next')
        bookmark['bookmark'] = i['url']
        i.update({'cm': [{'title': 30501, 'query': {'action': 'addBookmark', 'url': json.dumps(bookmark)}}]})

    directory.add(self_list, content='videos')


@cache_function(1800)
def category_list(url):

    if BASE_API_LINK in url:

        _json = client.request(url, output='json')
        list_of_lists = _json['sectionContents']
        codename = parse_qs(split(url)[1])['pageCodename'][0]
        page = _json['pagination']['page']
        total_pages = _json['pagination']['totalPages']

    else:

        html = client.request(url)
        script = client.parseDOM(html, 'script')[0].partition('</script>')[0].replace('var ___INITIAL_STATE__ = ', '')[:-1]
        _json = json.loads(script)
        pages = _json['pages']
        list_of_lists = [i for i in list(pages['sectionsByCodename'].values()) if 'adman' not in i['sectionContentCodename']]
        codename = list(pages.keys())[-1]
        page = 1
        total_pages = pages[codename]['totalPages']

    next_url = GET_PAGE_CONTENT.format(page + 1, codename)

    self_list = []

    for list_ in list_of_lists:
        title = list_['portalName']
        section_codename = list_['sectionContentCodename']
        if not list_['tilesIds']:
            continue
        url = LIST_OF_LISTS_LINK.format(
            title=quote(section_codename), pagecodename=codename, backurl=codename,
            sectioncodename=list_['sectionContentCodename']
        )
        data = {'title': title, 'url': url, 'nextaction': 'categories'}
        if page < total_pages:
            data.update({'nextlabel': 30500, 'nexticon': control.addonmedia('next.jpg'), 'next': next_url})
        self_list.append(data)

    return self_list


@urldispatcher.register('categories', ['url'])
def categories(url):

    self_list = category_list(url)

    for i in self_list:
        i.update({'action': 'listing'})

    directory.add(self_list)


# @urldispatcher.register('search')
# def search():
#
#     input_str = control.inputDialog()
#
#     _json = client.request(SEARCH, post=search_post(input_str), output='json')


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

    self_list.insert(
        4,
        {
            'title': 'Zeppelin Radio 106.1', 'action': 'play', 'isFolder': 'False',
            'url': ''.join([RADIO_STREAM, '/ert-zeppelin']), 'image': 'https://i.imgur.com/ep3LptZ.jpg',
            'fanart': control.addonmedia('zeppelin_bg.jpg')
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


@cache_function(259200)
def resolve(url):

    codename = split(url)[1].partition('-')[2]

    _json = client.request(ACQUIRE_CONTENT.format(DEVICE_KEY, codename), output='json')

    if len(_json['MediaFiles'][0]['Formats']) == 1:

        return _json['MediaFiles'][0]['Formats'][0]['Url']

    else:

        for result in _json['MediaFiles'][0]['Formats']:
            if '.mpd' in result['Url'] and control.setting('prefer_mpd') == 'true':
                return result['Url']
            elif '.m3u8' in result['Url']:
                return result['Url']


@urldispatcher.register('play', ['url'])
def play(url):

    if ('m3u8' not in url or 'mpd' not in url) and 'radiostreaming' not in url:
        url = resolve(url)

    dash = ('.m3u8' in url or '.mpd' in url) and control.kodi_version() >= 18.0

    directory.resolve(
        url, dash=dash,
        mimetype='application/vnd.apple.mpegurl' if 'm3u8' in url else None,
        manifest_type='hls' if 'm3u8' in url else None
    )


@urldispatcher.register('enter_yt_channel', ['url'])
def enter_yt_channel(url):

    control.execute('Container.Update({},return)'.format(url))
