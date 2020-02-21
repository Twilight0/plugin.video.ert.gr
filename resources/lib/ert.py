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
    along with this program.  If not, see <https://www.gnu.org/licenses/>.
'''
from __future__ import absolute_import

import json, re
from tulip import bookmarks, directory, client, cache, control
from tulip.compat import iteritems, urlparse, range
from youtube_resolver import resolve as yt_resolver
from youtube_plugin.youtube.youtube_exceptions import YouTubeException


class Indexer:

    def __init__(self):

        self.list = []

        self.base_link = 'https://webtv.ert.gr'
        self.series_link = self.base_link.replace('webtv', 'series')

        self.categories_link = ''.join([self.base_link, '/ekpompes/'])
        self.recent_link = ''.join([self.base_link, '/feed/'])
        self.shows_link = ''.join([self.base_link, '/shows'])

        self.category_link = ''.join([self.base_link, '/category'])
        self.news_link = ''.join([self.category_link, '/eidiseis/'])
        self.weather_link = ''.join([self.category_link, '/kairos/'])
        self.cartoons_link = ''.join([self.category_link, '/paidika/'])

        self.tag_link = ''.join([self.base_link, '/tag'])
        self.culture_link = ''.join([self.tag_link, '/politismos/'])
        self.doc_link = ''.join([self.tag_link, '/ntokimanter/'])

        self.sports_link = ''.join([self.shows_link, '/athlitika/'])
        self.movies_link = ''.join([self.category_link, '/movies/xenes-tainies/'])

        self.ert1_link = ''.join([self.base_link, '/ert1-live/'])
        self.ert2_link = ''.join([self.base_link, '/ert2-live/'])
        self.ert3_link = ''.join([self.base_link, '/ert3-live/'])
        self.ertw_link = ''.join([self.base_link, '/ertworld-live/'])
        self.ertp1_link = ''.join([self.base_link, '/ert-play-live/'])
        self.ertp2_link = ''.join([self.base_link, '/ert-play-2-live/'])
        self.ertp3_link = ''.join([self.base_link, '/ertplay-3-live/'])
        self.ertp4_link = ''.join([self.base_link, '/ertplay-4-live/'])
        self.ertp5_link = ''.join([self.base_link, '/ertplay-5-live/'])
        self.ertsports_link = ''.join([self.base_link, '/ert-sports-live/'])

        self.radio_link = 'https://webradio.ert.gr/'
        self.radio_stream = 'http://radiostreaming.ert.gr'
        self.district_link = ''.join([self.radio_link, 'liveradio/list.html'])

    def root(self):

        self.list = [
            {
                'title': control.lang(32001),
                'action': 'channels',
                'icon': 'channels.png'
            }
            ,
            {
                'title': control.lang(32002),
                'action': 'recent',
                'icon': 'recent.png'
            }
            ,
            {
                'title': control.lang(32011),
                'action': 'index',
                'icon': 'index.png'
            }
            ,
            {
                'title': control.lang(32004),
                'action': 'episodes',
                'url': self.news_link,
                'icon': 'news.png'
            }
            ,
            {
                'title': control.lang(32003),
                'action': 'sports',
                'url': self.sports_link,
                'icon': 'sports.png'
            }
            ,
            {
                'title': control.lang(32006),
                'action': 'episodes',
                'url': self.weather_link,
                'icon': 'weather.png'
            }
            ,
            {
                'title': control.lang(32007),
                'action': 'episodes',
                'url': self.doc_link,
                'icon': 'documentary.png'
            }
            ,
            {
                'title': control.lang(32009),
                'action': 'episodes',
                'url': self.cartoons_link,
                'icon': 'cartoons.png'
            }
            ,
            {
                'title': control.lang(32049),
                'action': 'episodes',
                'icon': 'movies.png',
                'url': self.movies_link
            }
            ,
            {
                'title': control.lang(32038),
                'action': 'series',
                'icon': 'series.png'
            }
            ,
            {
                'title': control.lang(32026),
                'action': 'radios',
                'icon': 'radio.png'
            }
            ,
            {
                'title': control.lang(32012),
                'action': 'bookmarks',
                'icon': 'bookmarks.png'
            }
        ]

        for item in self.list:

            cache_clear = {'title': 32036, 'query': {'action': 'cache_clear'}}
            item.update({'cm': [cache_clear]})

        directory.add(self.list, content='videos')

    def channels(self):

        self.list = [
            {
                'title': 32021,
                'action': 'play',
                'url': self.ert1_link,
                'isFolder': 'False',
                'icon': 'live1.png'
            },

            {
                'title': 32022,
                'action': 'play',
                'url': self.ert2_link,
                'isFolder': 'False',
                'icon': 'live2.png'
            },

            {
                'title': 32023,
                'action': 'play',
                'url': self.ert3_link,
                'isFolder': 'False',
                'icon': 'live3.png'
            },

            {
                'title': 32024,
                'action': 'play',
                'url': self.ertw_link,
                'isFolder': 'False',
                'icon': 'livew.png'
            }
            ,
            {
                'title': 32025,
                'action': 'play',
                'url': self.ertp1_link,
                'isFolder': 'False',
                'icon': 'livep.png'
            }
            ,
            {
                'title': 32037,
                'action': 'play',
                'url': self.ertp2_link,
                'isFolder': 'False',
                'icon': 'livep.png'
            }
            ,
            {
                'title': 32039,
                'action': 'play',
                'url': self.ertp3_link,
                'isFolder': 'False',
                'icon': 'livep.png'
            }
            ,
            {
                'title': 32040,
                'action': 'play',
                'url': self.ertp4_link,
                'isFolder': 'False',
                'icon': 'livep.png'
            }
            ,
            {
                'title': 32042,
                'action': 'play',
                'url': self.ertp5_link,
                'isFolder': 'False',
                'icon': 'livep.png'
            }
            ,
            {
                'title': 32041,
                'action': 'play',
                'url': self.ertsports_link,
                'isFolder': 'False',
                'icon': 'lives.png'
            }
        ]

        for i in self.list:

            i.update({'fanart': control.addonmedia('webtv_fanart.jpg')})

        directory.add(self.list, content='videos')

    def bookmarks(self):

        self.list = bookmarks.get()

        if not self.list:
            na = [{'title': 'N/A', 'action': None}]
            directory.add(na)
            return

        for i in self.list:
            bookmark = dict((k, v) for k, v in iteritems(i) if not k == 'next')
            bookmark['delbookmark'] = i['url']
            i.update({'cm': [{'title': 32502, 'query': {'action': 'deleteBookmark', 'url': json.dumps(bookmark)}}]})

        control.sortmethods('title')

        directory.add(self.list, content='videos')

    def index_listing(self):

        html = client.request(self.categories_link)

        div = client.parseDOM(html, 'div', attrs={'class': 'wpb_wrapper'})[0]

        li = client.parseDOM(div, 'li')

        li.extend(client.parseDOM(div, 'li', attrs={'class': 'hideli'}))

        items = [i for i in li if 'category' in i and 'title' in i]

        for item in items:

            title = client.replaceHTMLCodes(client.parseDOM(item, 'a')[0])
            url = client.parseDOM(item, 'a', ret='href')[0]

            self.list.append({'title': title, 'url': url})

        return self.list

    def index(self):

        self.list = cache.get(self.index_listing, 24)

        if self.list is None:
            return

        for i in self.list:
            i.update({'action': 'episodes'})

        for i in self.list:
            bookmark = dict((k, v) for k, v in iteritems(i) if not k == 'next')
            bookmark['bookmark'] = i['url']
            i.update({'cm': [{'title': 32501, 'query': {'action': 'addBookmark', 'url': json.dumps(bookmark)}}]})

        self.list = sorted(self.list, key=lambda k: k['title'].lower())

        directory.add(self.list, content='videos')

    def episodes(self, url):

        self.list = cache.get(self.episodes_list, 2, url)

        if self.list is None:
            return

        for i in self.list:
            i.update({'action': 'play', 'isFolder': 'False', 'nextlabel': 32500, 'nextaction': 'episodes'})

        directory.add(self.list, content='videos')

    def recent(self):

        self.list = cache.get(self.recent_list, 1, self.recent_link)

        if self.list is None:
            return

        for i in self.list:
            i.update({'action': 'play', 'isFolder': 'False'})

        directory.add(self.list, content='videos')

    def play(self, url):

        title = None

        if url == self.ert1_link:
            title = control.lang(32021)
        elif url == self.ert2_link:
            title = control.lang(32022)
        elif url == self.ert3_link:
            title = control.lang(32023)
        elif url == self.ertw_link:
            title = control.lang(32024)
        elif url == self.ertp1_link:
            title = control.lang(32025)
        elif url == self.ertp2_link:
            title = control.lang(32037)
        elif url == self.ertp3_link:
            title = control.lang(32039)
        elif url == self.ertp4_link:
            title = control.lang(32040)
        elif url == self.ertsports_link:
            title = control.lang(32041)

        stream = self.resolve(url)

        dash = '.mpd' in stream or 'dash' in stream

        directory.resolve(stream, meta={'title': title}, dash=dash)

    def episodes_list(self, url):

        if client.request(url, redirect=False, output='response')[0] == u'301':
            url = re.sub(r'category/[\w-]+', 'tag', url)

        result = client.request(url)

        items = client.parseDOM(result, 'div', attrs={'class': 'blog-listing-con.+?'})[0]
        items = client.parseDOM(items, 'div', attrs={'class': 'item-thumbnail'})

        try:
            nexturl = client.parseDOM(result, 'a', ret='href', attrs={'rel': 'next'})[0]
        except Exception:
            nexturl = ''

        for item in items:

            try:
                plot = client.parseDOM(item, 'p')[0]
            except Exception:
                plot = ''

            title = client.parseDOM(item, 'a', ret='title')[0]
            title = client.replaceHTMLCodes(title)

            url = client.parseDOM(item, 'a', ret='href')[0]

            image = client.parseDOM(item, 'img', ret='src')[0]

            self.list.append({'title': title, 'url': url, 'image': image, 'next': nexturl, 'plot': plot})

        return self.list

    def recent_list(self, url):
        try:

            result = client.request(url)
            items = client.parseDOM(result, 'item')

        except Exception:

            return

        for item in items:

            title = client.replaceHTMLCodes(client.parseDOM(item, 'title')[0])

            url = client.parseDOM(item, 'link')[0]

            image = client.parseDOM(item, 'img', ret='src')[0]

            self.list.append({'title': title, 'url': url, 'image': image})

        return self.list

    def sports(self):

        self.list = [
            {
                'title': 32005,
                'url': ''.join([self.category_link, '/athlitika/athlitikoi-agwnes/football/']),
                'image': ''.join([self.base_link, '/wp-content/uploads/2017/10/football.jpg'])
            }
            ,
            {
                'title': 32008,
                'url': ''.join([self.category_link, '/athlitika/athlitikoi-agwnes/basketball/']),
                'image': ''.join([self.base_link, '/wp-content/uploads/2017/10/basket-1.jpg'])
            }
            ,
            {
                'title': 32043,
                'url': ''.join([self.category_link, '/athlitika/athlitikoi-agwnes/volley/']),
                'image': ''.join([self.base_link, '/wp-content/uploads/2017/10/volei.jpg'])
            }
            ,
            {
                'title': 32044,
                'url': ''.join([self.tag_link, '/tennis/']),
                'image': ''.join([self.base_link, '/wp-content/uploads/2018/09/tennis.png'])
            }
            ,
            {
                'title': 32045,
                'url': ''.join([self.tag_link, '/polo/']),
                'image': ''.join([self.base_link, '/wp-content/uploads/2018/09/POlo.png'])
            }
            ,
            {
                'title': 32046,
                'url': ''.join([self.category_link, '/athlitika/athlitikoi-agwnes/ygros-stivos/']),
                'image': ''.join([self.base_link, '/wp-content/uploads/2018/09/YgrosStivos.png'])
            }
            ,
            {
                'title': 32047,
                'url': ''.join([self.category_link, '/athlitika/athlitikoi-agwnes/stivos/']),
                'image': ''.join([self.base_link, '/wp-content/uploads/2018/09/Stivos.png'])
            }
            ,
            {
                'title': 32048,
                'url': ''.join([self.tag_link, '/chantmpol/']),
                'image': ''.join([self.base_link, '/wp-content/uploads/2018/09/Handball.png'])
            },
            {
                'title': 32053,
                'url': ''.join([self.category_link, '/ert2/auto-moto-ert/']),
                'image': ''.join([self.base_link, '/wp-content/uploads/2018/09/AutoMoto.png'])
            }
            ,
            {
                'title': 32050,
                'url': ''.join([self.tag_link, '/marathonios/']),
                'image': ''.join([self.base_link, '/wp-content/uploads/2018/09/Marathonios.png'])
            }
            ,
            {
                'title': 32051,
                'url': ''.join([self.tag_link, '/pagkosmio-protathlima-patinaz/']),
                'image': ''.join([self.base_link, '/wp-content/uploads/2018/09/KallitexnikoPatinaz.png'])
            }
            ,
            {
                'title': 32052,
                'url': ''.join([self.category_link, '/athlitika/athlitikoi-agwnes/alla-spor/']),
                'image': ''.join([self.base_link, '/wp-content/uploads/2017/10/alla-spor.jpg'])
            }
        ]

        for i in self.list:
            i.update({'action': 'episodes'})

        directory.add(self.list)

    def series_listing(self):

        html = client.request(self.series_link)

        items = client.parseDOM(html, 'figure', attrs={'class': 'wpb_wrapper vc_figure'})

        for item in items:

            url = client.parseDOM(item, 'a', ret='href')[0]
            title = urlparse(url).path.strip('/').replace('-', ' ').capitalize()
            image = client.parseDOM(item, 'img', ret='src')[0]

            self.list.append({'title': title, 'image': image, 'url': url})

        return self.list

    def series(self):

        self.list = cache.get(self.series_listing, 6)

        if self.list is None:
            return

        for i in self.list:
            i.update({'action': 'series_episodes'})
            bookmark = dict((k, v) for k, v in iteritems(i) if not k == 'next')
            bookmark['bookmark'] = i['url']
            i.update({'cm': [{'title': 32501, 'query': {'action': 'addBookmark', 'url': json.dumps(bookmark)}}]})

        directory.add(self.list, content='videos')

    def series_episodes_listing(self, url):

        def appender(html_):

            _list = []

            items = client.parseDOM(html_, 'div', attrs={'class': 'pt-cv-ifield'})

            for _item in items:

                title = client.parseDOM(_item, 'h4')[0]
                label = client.replaceHTMLCodes(client.parseDOM(title, 'a')[0])
                image = client.parseDOM(_item, 'img', ret='src')[0]
                plot = client.parseDOM(_item, 'div', attrs={'class': 'pt-cv-content'})[0].partition('<br>')[0]
                _url = client.parseDOM(title, 'a', ret='href')[0]

                _list.append({'title': label, 'url': _url, 'plot': plot, 'image': image})

            return _list

        html = client.request(url)

        if 'vc_btn3-container vc_btn3-center' in html:

            inner = client.parseDOM(html, 'div', attrs={'class': 'vc_btn3-container vc_btn3-center'})

            for i in inner:

                inner_url = client.parseDOM(i, 'a', ret='href')[0]

                inner_html = client.request(inner_url)

                self.list = appender(inner_html)

        else:

            self.list = appender(html)

        return self.list

    def series_episodes(self, url):

        self.list = cache.get(self.series_episodes_listing, 6, url)

        if self.list is None:
            return

        for i in self.list:
            i.update({'action': 'play', 'isFolder': 'False'})

        directory.add(self.list, content='videos')

    def radios(self):

        images = [
            ''.join([self.radio_link, i]) for i in [
                'wp-content/uploads/2016/06/proto.jpg', 'wp-content/uploads/2016/06/deytero.jpg',
                '/wp-content/uploads/2016/06/trito.jpg', 'wp-content/uploads/2016/06/kosmos.jpg',
                'wp-content/uploads/2016/06/VoiceOgGreece.png', 'wp-content/uploads/2016/06/eraSport.jpg',
                'wp-content/uploads/2016/06/958fm.jpg', 'wp-content/uploads/2016/06/102fm.jpg'
            ]
        ]

        names = [control.lang(n) for n in list(range(32028, 32036))]

        urls = [
            ''.join([self.radio_stream, i]) for i in [
                '/ert-proto', '/ert-deftero', '/ert-trito', '/ert-kosmos', '/ert-voiceofgreece', '/ert-erasport',
                '/ert-958fm', '/ert-102fm'
            ]
        ]

        radios = map(lambda x, y, z: (x, y, z), names, images, urls)

        for title, image, link in radios:

            self.list.append({'title': title, 'url': link, 'image': image, 'action': 'play', 'isFolder': 'False'})

        district = {'title': control.lang(32027), 'action': 'district', 'icon': 'district.png'}

        self.list.append(district)

        directory.add(self.list)

    def district_list(self):

        try:
            try:
                result = client.request(self.district_link).decode('windows-1253')
            except AttributeError:
                result = client.request(self.district_link)
            radios = client.parseDOM(result, 'td')
            radios = [r for r in radios if r]

        except Exception:

            return

        for radio in radios:

            title = client.parseDOM(radio, 'a')[0]
            href = client.parseDOM(radio, 'a', ret='href')[0]
            html = client.request(href)
            link = client.parseDOM(html, 'iframe', ret='src')[0]
            embed = client.request(link)
            url = re.search(r'mp3: [\'"](.+?)[\'"]', embed).group(1).replace('https', 'http')
            image = client.parseDOM(html, 'img', ret='src')[0]

            self.list.append({'title': title, 'image': image, 'url': url})

        return self.list

    def district(self):

        self.list = cache.get(self.district_list, 96)

        if self.list is None:
            return

        for i in self.list:
            i.update({'action': 'play', 'isFolder': 'False'})

        directory.add(self.list)

    def resolve(self, url):

        if 'radiostreaming' in url:
            return url
        elif 'youtube' in url or len(url) == 11:
            return self.yt_session(url)
        else:
            html = client.request(url)
            if 'live' in url:
                html = client.parseDOM(html, 'div', attrs={'class': 'wpb_column vc_column_container vc_col-sm-12'})[0]
            if 'iframe' in html:
                iframe = client.parseDOM(html, 'iframe', ret='src')[0]
            else:
                availability = client.parseDOM(html, 'strong')[-1]
                control.okDialog(control.name(), availability)
                return 'https://static.adman.gr/inpage/blank.mp4'
            if 'youtube' in iframe:
                return self.resolve(iframe)
            else:
                result = client.request(iframe)
                url = re.search(r'var (?:HLSLink|stream) = [\'"](.+?)[\'"]', result)
                if url:
                    url = url.group(1)
                    return url
                else:
                    iframes = client.parseDOM(result, 'iframe', ret='src')
                    try:
                        return self.resolve(iframes[1])
                    except YouTubeException:
                        return self.resolve(iframes[0])

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
