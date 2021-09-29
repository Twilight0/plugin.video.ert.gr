# -*- coding: utf-8 -*-

'''
    ERTflix Addon
    Author Twilight0

    SPDX-License-Identifier: GPL-3.0-only
    See LICENSES/GPL-3.0-only for more information.
'''

from __future__ import absolute_import

import json, re
from os.path import exists as file_exists
from zlib import decompress
from base64 import b64decode
from tulip import bookmarks, directory, client, cache, control, cleantitle, user_agents, net
from tulip.compat import iteritems, range, quote, parse_qsl, urlencode, concurrent_futures
from tulip.parsers import itertags_wrapper, parseDOM
from youtube_resolver import resolve as yt_resolver
from youtube_registration import register_api_keys
from youtube_plugin.youtube.youtube_exceptions import YouTubeException


cache_method = cache.FunctionCache().cache_method
cache_function = cache.FunctionCache().cache_function


@cache_function(5760)
def _plot(url):

    load = client.request(url.partition('?')[0], post=url.partition('?')[2], timeout=20)

    description = parseDOM(load, 'div', {'class': 'video-description'})[-1]
    paragraphs = [client.stripTags(p) for p in parseDOM(description, 'p')]
    plot = client.replaceHTMLCodes('[CR]'.join(paragraphs))

    return plot


def meta_viewer(url):

    heading = control.infoLabel('Listitem.Label')

    control.dialog.textviewer(heading=heading, text=_plot(url))


class Indexer:

    def __init__(self, argv):

        self.list = []; self.data = []

        self.argv = argv
        self.base_link = 'https://www.ertflix.gr'
        self.old_base = 'https://webtv.ert.gr'
        self.search_link = ''.join([self.base_link, '/?s={}'])
        self.category_link = ''.join([self.base_link, '/category'])
        self.ajax_url = ''.join([self.base_link, '/wp-admin/admin-ajax.php'])
        self.load_more = 'action=loadmore_post_by_cat&query={query}&page={page}'
        self.load_search = 'action=load_search_post_info&item_id={data_id}'

        self.index_link = ''.join([self.base_link, '/ekpompes/'])
        self.recent_link = ''.join([self.base_link, '/feed/'])
        self.shows_link = ''.join([self.old_base, '/shows'])

        self.sports_link = ''.join([self.category_link, '/athlitika/'])

        self.news_link = ''.join([self.category_link, '/enimerosi-24/'])
        self.cartoons_link = ''.join([self.category_link, '/pedika/'])
        self.entertainment_link = ''.join([self.category_link, '/psichagogia/'])
        self.interviews_link = ''.join([self.category_link, '/synentefxeis/'])
        self.archive_link = ''.join([self.category_link, '/arxeio/'])

        self.ellinika_docs = ''.join([self.category_link, '/ellhnika-docs/'])
        self.ksena_docs = ''.join([self.category_link, '/ksena-docs/'])

        self.music_box_link = ''.join([self.category_link, '/moysiko-koyti/'])
        self.contemporary_music_link = ''.join([self.category_link, '/sygchroni-moysiki/'])
        self.classical_music_link = ''.join([self.category_link, '/klasiki-moysiki/'])

        self.movies_link = ''.join([self.category_link, '/tainies/'])
        self.series_link = ''.join([self.category_link, '/ksenes-seires/'])
        self.catchup_link = ''.join([self.category_link, '/ksenes-seires-catchup/'])
        self.greek_series_link = ''.join([self.category_link, '/ellinikes-seires/'])
        self.web_series_link = ''.join([self.category_link, '/web-series/'])

        # self.ert1_link = ''.join([self.base_link, '/ert1-live/'])
        # self.ert2_link = ''.join([self.base_link, '/ert2-live/'])
        # self.ert3_link = ''.join([self.base_link, '/ert3-live/'])
        # self.ertw_link = ''.join([self.base_link, '/ertworld-live/'])
        # self.erts_link = ''.join([self.base_link, '/ert-sports-live/'])

        self.radio_link = 'https://webradio.ert.gr'
        self.radio_stream = 'http://radiostreaming.ert.gr'
        self.district_link = ''.join([self.radio_link, '/liveradio/list.html'])
        self.channel_id = 'UC0jVU-mK53vDQZcSZB5mVHg'
        self.scramble = (
            'eJwVzM0OQzAAAOBXkZ43oRh2Y7KNZScmm4sUVc1K/bRNbNm7Lx7g+76ANuCoAcuF0LMN0/MdY484aislYS/9VpomplBROAytyzjroJh0NI'
            '6LTjgnDMsFzzUfBB6EXvMe7DSARlq+8bq1QfxB6XqCJItcZYXnqCCclGPcJahw7k3g5g91uL42teB6xmJDIRZRm7EiDtekeVY3O+Xd1OUX'
            '8PsDJ7A4qQ=='
        )

        self.keys_registration()

    def root(self):

        self.list = [
            {
                'title': control.lang(30001),
                'action': 'channels',
                'icon': 'channels.jpg'
            }
            ,
            {
                'title': control.lang(30002),
                'action': 'recent',
                'icon': 'recent.jpg'
            }
            ,
            {
                'title': control.lang(30015),
                'action': 'youtube',
                'icon': 'youtube.jpg',
                'url': ''.join(
                    ['plugin://plugin.video.youtube/channel/', self.channel_id, '/?addon_id=', control.addonInfo('id')]
                ),
                'isFolder': 'False', 'isPlayable': 'False'
            }
            ,
            {
                'title': control.lang(30011),
                'action': 'index',
                'icon': 'index.jpg'
            }
            ,
            {
                'title': control.lang(30004),
                'action': 'listing',
                'url': self.news_link,
                'icon': 'news.jpg'
            }
            ,
            {
                'title': control.lang(30049),
                'action': 'listing',
                'icon': 'movies.jpg',
                'url': self.movies_link
            }
            ,
            {
                'title': control.lang(30020),
                'action': 'shows',
                'icon': 'shows.jpg'
            }
            ,
            {
                'title': control.lang(30038),
                'action': 'series',
                'icon': 'series.jpg'
            }
            ,
            {
                'title': control.lang(30003),
                'action': 'listing',
                'url': self.sports_link,
                'icon': 'sports.jpg'
            }
            ,
            {
                'title': control.lang(30009),
                'action': 'music',
                'icon': 'music.jpg'
            }
            ,
            {
                'title': control.lang(30060),
                'action': 'kids',
                'icon': 'kids.jpg'
            }
            ,
            {
                'title': control.lang(30055),
                'action': 'listing',
                'url': self.archive_link,
                'icon': 'archive.jpg'
            }
            ,
            {
                'title': control.lang(30013),
                'action': 'search',
                'icon': 'search.jpg',
                'isFolder': 'False', 'isPlayable': 'False'
            }
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
            self.list.append(settings_menu)

        if control.setting('show_exit') == 'true':
            self.list.append(exit_button)

        for item in self.list:

            cache_clear = {'title': 30036, 'query': {'action': 'cache_clear'}}
            settings = {'title': 30039, 'query': {'action': 'settings'}}
            item.update({'cm': [cache_clear, settings]})

        directory.add(self.list, argv=self.argv, content='videos')

    @cache_method(86400)
    def get_live_links(self):

        html = client.request(self.base_link)

        list_items = client.parseDOM(html, 'li', attrs={'id': 'nav-menu-item-230432'})[0]

        pattern = r'<a href="(http.+)" class="menu-link  sub-menu-link">(.+) LIVE </a>'

        matches = re.findall(pattern, list_items)

        return matches

    def channels(self):

        try:
            get_items = self.get_live_links()
        except Exception:
            return

        for url, title in get_items:

            fanart = None
            icon = None

            if 'sports' in url:
                fanart = control.addonmedia('EPT_SPORTS_fanart.jpg')
                icon = 'EPT_SPORTS.png'
            elif 'ert1-live' in url:
                fanart = control.addonmedia('EPT1_fanart.jpg')
                icon = 'EPT1.png'
            elif 'ert2-live' in url:
                fanart = control.addonmedia('EPT2_fanart.jpg')
                icon = 'EPT2.png'
            elif 'ert3-live' in url:
                fanart = control.addonmedia('EPT3_fanart.jpg')
                icon = 'EPT3.png'
            elif 'ertworld' in url:
                fanart = control.addonmedia('EPT_WORLD_fanart.jpg')
                icon = 'EPT_WORLD.png'

            data = {'title': title, 'fanart': fanart, 'icon': icon, 'url': url, 'action': 'play', 'isFolder': 'False'}
            self.list.append(data)

        directory.add(self.list, argv=self.argv, content='videos')

    def bookmarks(self):

        self.list = bookmarks.get()

        if not self.list:
            na = [{'title': control.lang(30058), 'action': None}]
            directory.add(na, argv=self.argv)
            return

        for i in self.list:
            bookmark = dict((k, v) for k, v in iteritems(i) if not k == 'next')
            bookmark['delbookmark'] = i['url']
            i.update({'cm': [{'title': 30502, 'query': {'action': 'deleteBookmark', 'url': json.dumps(bookmark)}}]})

        if control.setting('bookmarks_clear_boolean') == 'true':

            clear_menu = {
                'title': control.lang(30059), 'action': 'clear_bookmarks', 'isFolder': 'False', 'isPlayable': 'False'
            }

            self.list.insert(0, clear_menu)

        control.sortmethods()
        control.sortmethods('title')

        directory.add(self.list, argv=self.argv, content='videos')

    @cache_method(2880)
    def index_listing(self):

        html = client.request(self.index_link)

        div = parseDOM(html, 'div', attrs={'class': 'wpb_wrapper'})[0]

        li = parseDOM(div, 'li')

        li.extend(parseDOM(div, 'li', attrs={'class': 'hideli'}))

        items = [i for i in li if 'category' in i and 'title' in i]

        for item in items:

            title = client.replaceHTMLCodes(parseDOM(item, 'a')[0])
            url = parseDOM(item, 'a', ret='href')[0]

            self.list.append({'title': title, 'url': url})

        self.list = sorted(self.list, key=lambda k: k['title'].lower())

        return self.list

    def index(self):

        try:
            self.list = self.index_listing()
        except Exception:
            return

        for i in self.list:
            i.update({'action': 'listing'})

        for i in self.list:
            bookmark = dict((k, v) for k, v in iteritems(i) if not k == 'next')
            bookmark['bookmark'] = i['url']
            i.update({'cm': [{'title': 30006, 'query': {'action': 'addBookmark', 'url': json.dumps(bookmark)}}]})

        directory.add(self.list, argv=self.argv, content='videos')

    def thread(self, url, post=None):

        result = client.request(url, post=post, timeout=20)
        self.data.append(result)

    def _loop(self, item, header, count, next_url=None):

        data_id = item.attributes['data-id']
        img = item.attributes['style']
        image = re.search(r'url\((.+)\)', img).group(1)
        url = [i for i in itertags_wrapper(item.text, 'a', ret='href') if 'https' in i][0]
        meta_url = '?'.join([self.ajax_url, self.load_search.format(data_id=data_id)])

        if 'inside-page-thumb-titles' in item.text and control.setting('metadata') == 'false':

            fanart = None
            plot = None
            title = parseDOM(item.text, 'div', attrs={'class': 'inside-page-thumb-titles'})[0]
            title = client.replaceHTMLCodes(parseDOM(title, 'a')[0])

        else:

            load = client.request(self.ajax_url, post=self.load_search.format(data_id=data_id), timeout=20)
            title = parseDOM(load, 'p', {'class': 'video-title'})[0].strip()
            title = client.replaceHTMLCodes(title)
            description = parseDOM(load, 'div', {'class': 'video-description'})[-1]
            paragraphs = [client.stripTags(p) for p in parseDOM(description, 'p')]
            plot = client.replaceHTMLCodes('[CR]'.join(paragraphs))
            f = parseDOM(load, 'div', attrs={'class': 'cover'}, ret='style')[0]
            fanart = re.search(r'url\((.+)\)', f).group(1)

        data = {'title': title, 'image': image, 'url': url, 'code': count, 'meta_url': meta_url}

        if next_url:

            data.update({'next': next_url})

        if header in [
            u'ΞΕΝΕΣ ΣΕΙΡΕΣ ΠΛΗΡΕΙΣ', u'ΨΥΧΑΓΩΓΙΑ', u'ΣΥΝΕΝΤΕΥΞΕΙΣ', u'ΕΛΛΗΝΙΚΑ ΝΤΟΚΙΜΑΝΤΕΡ', u'ΞΕΝΑ ΝΤΟΚΙΜΑΝΤΕΡ',
            u'ΠΑΙΔΙΚΗ ΔΙΑΣΚΕΔΑΣΗ', u'Η ΕΡΤ ΘΥΜΑΤΑΙ', u'ΑΘΛΗΤΙΚΑ', u'ΞΕΝΕΣ ΣΕΙΡΕΣ CATCH-UP', u'WEB ΣΕΙΡΕΣ',
            u'ΕΛΛΗΝΙΚΕΣ ΣΕΙΡΕΣ', u'ΞΕΝΕΣ ΣΕΙΡΕΣ ΠΛΗΡΕΙΣ', u'ΝΤΟΚΙΜΑΝΤΕΡ'
        ] and not 'archeio' in url and header is not None:
            data.update({'playable': 'false'})

        if fanart:
            data.update({'fanart': fanart})
        if plot:
            data.update({'plot': plot})

        return data

    def _exec(self, _items, header, _next_url=None):

        threads = []

        if control.setting('threading') == 'true':

            with concurrent_futures.ThreadPoolExecutor(5) as executor:

                for count, _item in list(enumerate(_items, start=1)):
                    threads.append(executor.submit(self._loop, _item, header, count, _next_url))

                for future in concurrent_futures.as_completed(threads):

                    item = future.result()

                    if not item:
                        continue

                    self.list.append(item)

        else:

            for count, _item in list(enumerate(_items, start=1)):
                self.list.append(self._loop(_item, header, count, _next_url))

    @cache_method(360)
    def _listing(self, url):

        if self.ajax_url in url:
            result = client.request(url.partition('?')[0], post=url.partition('?')[2])
        else:
            result = client.request(url)

        try:
            header = parseDOM(result, 'h2')[0]
        except IndexError:
            header = None

        next_url = None
        override = False

        if self.base_link + '/?s=' in url or control.setting('pagination') == 'true':
            override = True

        threads = []

        if 'enimerosi-24' not in url and self.ajax_url not in url:

            ajaxes = [i for i in parseDOM(result, 'script', attrs={'type': 'text/javascript'}) if 'ajaxurl' in i]

            ajax1 = json.loads(re.search(r'var loadmore_params = ({.+})', ajaxes[-1]).group(1))
            ajax2 = json.loads(re.search(r'var cactus = ({.+})', ajaxes[0]).group(1))

            ajax = self._ajax_merge(ajax1, ajax2)
            pages = int(ajax['max_page'])
            posts = ajax['posts']

            try:
                posts = posts.encode('utf-8')
            except Exception:
                pass

            if control.setting('threading') == 'true' and not override:

                with concurrent_futures.ThreadPoolExecutor(5) as executor:

                    for i in range(0, pages + 1):
                        threads.append(
                            executor.submit(
                                self.thread, self.ajax_url, post=self.load_more.format(query=quote(posts), page=str(i)))
                            )

                    for future in concurrent_futures.as_completed(threads):

                        item = future.result()

                        if not item:
                            continue

                        self.list.append(item)

            else:

                for i in range(0, pages + 1):

                    a = client.request(self.ajax_url, post=self.load_more.format(query=quote(posts), page=str(i)))
                    self.data.append(a)

                    if i == 0 and override:
                        next_url = '?'.join([self.ajax_url, self.load_more.format(query=quote(posts), page='1')])
                        break

            html = '\n'.join(self.data)

            items = itertags_wrapper(html, 'div', attrs={'class': 'item item-\d+'})

            if len(items) < 20:
                next_url = None

            self._exec(items, header, next_url)

        elif self.ajax_url in url:

            items = itertags_wrapper(result, 'div', attrs={'class': 'item item-\d+'})

            parsed = dict(parse_qsl(url.partition('?')[2]))

            next_page = int(parsed['page']) + 1

            parsed['page'] = next_page

            if len(items) >= 20:
                next_url = '?'.join([url.partition('?')[0], urlencode(parsed)])

            self._exec(items, header, next_url)

        else:

            items = itertags_wrapper(result, 'div', attrs={'class': 'item item-\d+'})

            for item in items:

                text = item.text

                img = item.attributes['style']
                image = re.search(r'url\((.+)\)', img).group(1)
                title = client.replaceHTMLCodes(parseDOM(text, 'a')[0].strip())
                url = parseDOM(text, 'a', ret='href')[0]

                self.list.append({'title': title, 'image': image, 'url': url})

        return self.list

    def listing(self, url):

        try:
            self.list = self._listing(url)
        except Exception:
            return

        for i in self.list:

            if 'paidikes-tainies' in i['url'] or 'archeio' in i['url'] or 'giannis-exarchos' in i['url']:
                i.update({'action': 'play', 'isFolder': 'False'})
            elif i.get('playable') == 'false' or 'pedika' in i['url']:
                i.update({'action': 'listing'})
            else:
                i.update({'action': 'play', 'isFolder': 'False'})

            try:
                del i['playable']
            except KeyError:
                pass

            bookmark = dict((k, v) for k, v in iteritems(i) if not k == 'next')
            bookmark['bookmark'] = i['url']
            bookmark_cm = {'title': 30501, 'query': {'action': 'addBookmark', 'url': json.dumps(bookmark)}}

            if 'enimerosi-24' in url or 'meta_url' not in i:
                i.update({'cm': [bookmark_cm]})
            else:
                info_cm = {'title': 30043, 'query': {'action': 'info', 'url': i['meta_url']}}
                i.update({'cm': [bookmark_cm, info_cm]})

        if control.setting('pagination') == 'true':

            for i in self.list:

                i.update({'nextaction': 'listing', 'nextlabel': 30500, 'nexticon': control.addonmedia('next.jpg')})

        if 'tainies' in url or 'seires' in url or 'docs' in url or 'pedika' in url:

            control.sortmethods()
            control.sortmethods('title')
            control.sortmethods('production_code')

        if 'tainies' in url:
            content = 'movies'
        elif 'category' in url or 'arxeio' in url and not 'enimerosi-24' in url:
            content = 'tvshows'
        else:
            content = 'videos'

        directory.add(self.list, argv=self.argv, content=content)

    @cache_method(360)
    def recent_list(self):

        result = client.request(self.recent_link)
        items = parseDOM(result, 'item')

        for item in items:

            title = client.replaceHTMLCodes(parseDOM(item, 'title')[0])

            url = parseDOM(item, 'link')[0]

            image = parseDOM(item, 'img', ret='src')[0]

            self.list.append({'title': title, 'url': url, 'image': image})

        return self.list

    def kids(self):

        pl_id = 'PLgeq7ezNgWe94VavlcE6HC0k8RVanZWPe'

        self.list = [
            {
                'title': control.lang(30062),
                'url': self.cartoons_link,
                'action': 'listing',
                'icon': 'kids.jpg'
            }
            ,
            {
                'title': control.lang(30061),
                'url': 'plugin://plugin.video.youtube/channel/UC0jVU-mK53vDQZcSZB5mVHg/playlist/{0}/'.format(pl_id),
                'action': 'youtube',
                'icon': 'interviews.jpg',
                'isFolder': 'False', 'isPlayable': 'False'
            }
        ]

        directory.add(self.list, argv=self.argv)

    def music(self):

        self.list = [
            {
                'title': control.lang(30052),
                'url': self.music_box_link,
                'action': 'listing',
                'icon': 'music.jpg'
            }
            ,
            {
                'title': control.lang(30046),
                'url': self.contemporary_music_link,
                'action': 'listing',
                'icon': 'music.jpg'
            }
            ,
            {
                'title': control.lang(30051),
                'url': self.classical_music_link,
                'action': 'listing',
                'icon': 'music.jpg'
            }
        ]

        directory.add(self.list, argv=self.argv)

    def recent(self):

        try:
            self.list = self.recent_list()
        except Exception:
            return

        for i in self.list:
            i.update({'action': 'play', 'isFolder': 'False'})

        directory.add(self.list, argv=self.argv, content='videos')

    def play(self, url):

        stream = self.resolve(url)

        m3u8_dash = 'm3u8' in stream and control.kodi_version() >= 18.0

        directory.resolve(
            stream, dash=any(['.mpd' in stream, m3u8_dash]),
            mimetype='application/vnd.apple.mpegurl' if m3u8_dash else None,
            manifest_type='hls' if m3u8_dash else None
        )

    def series(self):

        self.list = [
            {
                'title': control.lang(30047),
                'url': self.greek_series_link,
                'icon': 'series.jpg'
            }
            ,
            {
                'title': control.lang(30057),
                'url': self.series_link,
                'icon': 'series.jpg'
            }
            ,
            {
                'title': control.lang(30053),
                'url': self.catchup_link,
                'icon': 'series.jpg'
            }
            ,
            {
                'title': control.lang(30054),
                'url': self.web_series_link,
                'icon': 'series.jpg'
            }
        ]

        for i in self.list:
            i.update({'action': 'listing'})

        directory.add(self.list, argv=self.argv)

    def shows(self):

        self.list = [
            {
                'title': control.lang(30010),
                'url': self.entertainment_link,
                'icon': 'shows.jpg'
            }
            ,
            {
                'title': control.lang(30016),
                'url': self.interviews_link,
                'icon': 'interviews.jpg'
            }
            ,
            {
                'title': control.lang(30017),
                'url': self.ksena_docs,
                'icon': 'documentaries.jpg'
            }
            ,
            {
                'title': control.lang(30018),
                'url': self.ellinika_docs,
                'icon': 'documentaries.jpg'
            }
        ]

        for i in self.list:
            i.update({'action': 'listing'})

        directory.add(self.list, argv=self.argv)

    def search(self):

        input_str = control.inputDialog()

        try:
            input_str = cleantitle.strip_accents(input_str.decode('utf-8'))
        except (UnicodeEncodeError, UnicodeDecodeError, AttributeError):
            input_str = cleantitle.strip_accents(input_str)

        input_str = quote(input_str.encode('utf-8'))

        directory.run_builtin(action='listing', url=self.search_link.format(input_str))

    def radios(self):

        images = [
            ''.join([self.radio_link, i]) for i in [
                '/wp-content/uploads/2016/06/proto.jpg', '/wp-content/uploads/2016/06/deytero.jpg',
                '/wp-content/uploads/2016/06/trito.jpg', '/wp-content/uploads/2016/06/kosmos.jpg',
                '/wp-content/uploads/2016/06/VoiceOgGreece.png', '/wp-content/uploads/2016/06/eraSport.jpg',
                '/wp-content/uploads/2016/06/958fm.jpg', '/wp-content/uploads/2016/06/102fm.jpg'
            ]
        ]

        names = [control.lang(n) for n in list(range(30028, 30036))]

        urls = [
            ''.join([self.radio_stream, i]) for i in [
                '/ert-proto', '/ert-deftero', '/ert-trito', '/ert-kosmos', '/ert-voiceofgreece', '/ert-erasport',
                '/ert-958fm', '/ert-102fm'
            ]
        ]

        radios = map(lambda x, y, z: (x, y, z), names, images, urls)

        for title, image, link in radios:

            self.list.append(
                {
                    'title': title, 'url': link, 'image': image, 'action': 'play', 'isFolder': 'False',
                    'fanart': control.addonmedia('radio_fanart.jpg')
                }
            )

        district = {
            'title': control.lang(30027), 'action': 'district', 'icon': 'district.jpg',
            'fanart': control.addonmedia('radio_fanart.jpg')
        }

        self.list.append(district)

        directory.add(self.list, argv=self.argv)

    def _radio_loop(self, station):

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

    @cache_method(5760)
    def district_list(self):

        result = client.request(self.district_link, as_bytes=True)
        result = result.decode('windows-1253')
        radios = parseDOM(result, 'td')
        stations = [r for r in radios if r]

        with concurrent_futures.ThreadPoolExecutor(5) as executor:

            threads = [executor.submit(self._radio_loop, station) for station in stations]

            for future in concurrent_futures.as_completed(threads):

                item = future.result()

                if not item:
                    continue

                self.list.append(item)

        return self.list

    def district(self):

        self.list = self.district_list()

        for i in self.list:
            i.update({'action': 'play', 'isFolder': 'False', 'fanart': control.addonmedia('radio_fanart.jpg')})

        directory.add(self.list, argv=self.argv)

    @cache_method(5760)
    def resolve(self, url):

        _url = url

        if 'radiostreaming' in url:

            return url

        elif 'youtube' in url or len(url) == 11:

            if url.startswith('plugin://'):
                url = url[-11:]

            return self.yt_session(url)

        else:

            html = client.request(url)

            if 'iframe' in html:

                iframe = parseDOM(html, 'iframe', ret='src')[0]

            else:

                availability = parseDOM(html, 'strong')[-1]
                control.okDialog(control.name(), availability)

                return 'https://static.adman.gr/inpage/blank.mp4'

            if 'youtube' in iframe:

                return self.resolve(iframe)

            else:

                result = client.request(iframe.replace(' ', '%20'))

                urls = re.findall(r'(?:var )?(?:HLSLink|stream)(?:ww)?\s+=\s+[\'"](.+?)[\'"]', result)

                if urls:

                    geo = self._geo_detect()

                    if len(urls) >= 2:

                        if _url.endswith('-live/'):

                            if not geo:
                                return urls[-1] + user_agents.spoofer(age_str=user_agents.CHROME, referer=True, ref_str='https://www.ertflix.gr/')
                            else:
                                return urls[0] + user_agents.spoofer(age_str=user_agents.CHROME, referer=True, ref_str='https://www.ertflix.gr/')

                        else:

                            resolved_urls = [u for u in list(set(urls)) if 'copyright-alert.mp4' not in u]

                            for url in resolved_urls:

                                if not geo:
                                    if 'dvrorigingr' in url:
                                        continue

                                try:
                                    video_ok = net.Net().http_HEAD(url)
                                except Exception:
                                    video_ok = None

                                if video_ok:
                                    return url + user_agents.spoofer(age_str=user_agents.CHROME, referer=True, ref_str='https://www.ertflix.gr/')
                                else:
                                    continue

                    else:

                        if 'youtube' in urls[0]:
                            return self.resolve(urls[0])
                        else:
                            return urls[0] + user_agents.spoofer(age_str=user_agents.CHROME, referer=True, ref_str='https://www.ertflix.gr/')

                else:

                    iframes = parseDOM(result, 'iframe', ret='src')

                    try:
                        return self.resolve(iframes[-1])
                    except YouTubeException:
                        return self.resolve(iframes[0])

    def keys_registration(self):

        filepath = control.transPath(control.join(control.addon('plugin.video.youtube').getAddonInfo('profile'), 'api_keys.json'))

        setting = control.addon('plugin.video.youtube').getSetting('youtube.allow.dev.keys') == 'true'

        if file_exists(filepath):

            f = open(filepath)

            jsonstore = json.load(f)

            no_keys = control.addonInfo('id') not in jsonstore.get('keys', 'developer').get('developer')

            if setting and no_keys:

                keys = json.loads(decompress(b64decode(self.scramble)))
                register_api_keys(control.addonInfo('id'), keys['api_key'], keys['id'], keys['secret'])

            f.close()

    @staticmethod
    @cache_method(11520)
    def _geo_detect():

        _json = client.request('https://geoip.siliconweb.com/geo.json', output='json')

        if 'GR' in _json['country']:
            return True

    @staticmethod
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

    @staticmethod
    def yt(url):

        control.execute('Container.Update({},return)'.format(url))

    @staticmethod
    def _ajax_merge(d1, d2):

        d = d1.copy()
        d.update(d2)

        return d


def clear_bookmarks():

    bookmarks.clear('bookmark', withyes=True, file_=control.bookmarksFile, notify=False, label_yes_no=30025)
    control.sleep(200)
    control.refresh()
