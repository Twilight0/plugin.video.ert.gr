# -*- coding: utf-8 -*-

'''
    ERTflix Addon
    Author Twilight0

    SPDX-License-Identifier: GPL-3.0-only
    See LICENSES/GPL-3.0-only for more information.
'''

import json
import os

from . import api
from .constants import TEMPLATES, WIDEVINE_URL
from tulip import kodi, directory, bookmarks
from tulip.utils import iteritems
from urldispatcher import urldispatcher

try:
    from pickled import FunctionCache
    _cache = FunctionCache(kodi.cacheDirectory)
    cache_function = _cache.cache_function
except Exception:
    def cache_function(limit, limit_mode=60):
        def wrap(func):
            return func
        return wrap


def _i18n(num):
    try:
        return kodi.i18n(num)
    except Exception:
        return str(num)


def _is_greek():
    try:
        return 'Greek' in kodi.infoLabel('System.Language')
    except Exception:
        return True


def _bookmark_cm(item):
    bookmark = dict((k, v) for k, v in iteritems(item) if k != 'next')
    bookmark['bookmark'] = item.get('url')
    return [{'title': 30501, 'query': {'action': 'addBookmark', 'url': json.dumps(bookmark)}}]


@urldispatcher.register('root')
def root():
    menu = [
        {'title': _i18n(30001), 'action': 'live', 'image': kodi.addonmedia('channels.jpg'), 'isFolder': 'True'},
        {'title': _i18n(30049), 'action': 'categories', 'url': TEMPLATES['movies'], 'image': kodi.addonmedia('movies.jpg'), 'isFolder': 'True'},
        {'title': _i18n(30038), 'action': 'categories', 'url': TEMPLATES['series'], 'image': kodi.addonmedia('series.jpg'), 'isFolder': 'True'},
        {'title': _i18n(30020), 'action': 'categories', 'url': TEMPLATES['shows'], 'image': kodi.addonmedia('shows.jpg'), 'isFolder': 'True'},
        {'title': _i18n(30017), 'action': 'categories', 'url': TEMPLATES['documentaries'], 'image': kodi.addonmedia('documentaries.jpg'), 'isFolder': 'True'},
        {'title': _i18n(30003), 'action': 'categories', 'url': TEMPLATES['sports'], 'image': kodi.addonmedia('sports.jpg'), 'isFolder': 'True'},
        {'title': _i18n(30004), 'action': 'categories', 'url': TEMPLATES['news'], 'image': kodi.addonmedia('news.jpg'), 'isFolder': 'True'},
        {'title': _i18n(30060), 'action': 'categories', 'url': TEMPLATES['kids'], 'image': kodi.addonmedia('kids.jpg'), 'isFolder': 'True'},
        {'title': _i18n(30013), 'action': 'search', 'image': kodi.addonmedia('search.jpg'), 'isFolder': 'True'},
        {'title': _i18n(30012), 'action': 'bookmarks', 'image': kodi.addonmedia('bookmarks.jpg'), 'isFolder': 'True'},
    ]

    if kodi.setting('settings_boolean') == 'true':
        menu.append({'title': _i18n(30044), 'action': 'settings', 'image': kodi.addonmedia('settings.jpg'), 'isFolder': 'False', 'isPlayable': 'False'})

    if kodi.setting('show_exit') == 'true':
        menu.append({'title': _i18n(30048), 'action': 'exit_kodi', 'image': kodi.addonmedia('exit.jpg'), 'isFolder': 'False', 'isPlayable': 'False'})

    for item in menu:
        item.update({'cm': [{'title': 30036, 'query': {'action': 'clear_cache'}}, {'title': 30039, 'query': {'action': 'settings'}}]})

    directory.builder(menu, content='videos')


@urldispatcher.register('bookmarks')
def bookmarks_list():
    self_list = bookmarks.get() or []

    if not self_list:
        directory.builder([{'title': _i18n(30058), 'action': None}], content='videos')
        return

    for i in self_list:
        bookmark = dict((k, v) for k, v in iteritems(i) if k != 'next')
        bookmark['delbookmark'] = i['url']
        i.update({'cm': [{'title': 30502, 'query': {'action': 'deleteBookmark', 'url': json.dumps(bookmark)}}]})

    if kodi.setting('bookmarks_clear_boolean') == 'true':
        self_list.insert(
            0, {'title': _i18n(30059), 'action': 'clear_bookmarks', 'isFolder': 'False', 'isPlayable': 'False'}
        )

    directory.builder(self_list, content='videos')


@cache_function(30, 60)
def _live_channels():
    data = api.btv_services()
    channels = []
    for service in data.get('services', []):
        editorial = service.get('editorial', {}) or {}
        technical = service.get('technical', {}) or {}
        if 'SmartTV' not in (service.get('deviceType') or technical.get('deviceType') or []):
            continue
        if (editorial.get('isHidden') in ('true', True)):
            continue
        if (editorial.get('serviceType') or service.get('serviceType')) == 'radio':
            continue
        url = technical.get('NetworkLocation')
        if not url:
            continue
        cid = service.get('e') or editorial.get('id')
        try:
            stcu_template = (technical.get('shortTermCatchUpParameters') or {}).get('sourceId')
        except AttributeError:
            stcu_template = None
        channels.append(
            {
                'name': editorial.get('ShortName') or editorial.get('longName') or cid,
                'id': cid,
                'station': editorial.get('stationId'),
                'url': url,
                'drm': technical.get('drmId'),
                'plot': editorial.get('Description') or '',
                'stcu': stcu_template,
            }
        )
    # de-duplicate by station, prefer DASH entries
    seen = {}
    for ch in channels:
        key = ch['station'] or ch['id']
        if key not in seen or '.mpd' in (ch['url'] or ''):
            seen[key] = ch
    return list(seen.values())


@urldispatcher.register('live')
def live():
    self_list = []
    for ch in _live_channels():
        self_list.append(
            {
                'title': ch['name'],
                'url': json.dumps({'url': ch['url'], 'drm': ch['drm']}, separators=(',', ':')),
                'image': api.channel_logo(ch['id']),
                'fanart': api.channel_logo(ch['id'], width=1280),
                'plot': ch['plot'] or ch['name'],
                'action': 'play_live',
                'isFolder': 'False', 'isPlayable': 'True',
            }
        )
    for i in self_list:
        i.update({'cm': _bookmark_cm(i)})
    directory.builder(self_list)


@cache_function(60, 60)
def _template_rails(template_id, lang):
    data = api.template_summary(template_id)
    rails = []
    for rail in data.get('rails', []):
        props = rail.get('configurationProperties') or {}
        if props.get('instance') == 'ad-banner':
            continue
        title = rail.get('title') or rail.get('name') or rail.get('id')
        if not rail.get('title') and props.get('style') == 'promotion':
            title = _i18n(30067)
        rails.append({'title': title, 'template': template_id, 'rail': rail.get('id')})
    return rails


@urldispatcher.register('categories', ['url'])
def categories(url):
    rails = _template_rails(url, api.content_lang())
    self_list = [
        {
            'title': r['title'], 'url': json.dumps(r, separators=(',', ':')),
            'action': 'listing', 'isFolder': 'True',
        }
        for r in rails
    ]
    directory.builder(self_list, content='videos')


def _vod_image(item, width=400):
    cid = item.get('contentRef') or item.get('id') or ''
    kind = 'tvshow' if (item.get('seriesRef') or cid.endswith('_E0')) else 'movie'
    if not cid:
        return ''
    return api.image_url(kind, cid, 'HorizontalPoster', aspect='16x9', width=width)


@cache_function(30, 60)
def _rail_items(template_id, rail_id, lang):
    data = api.rail_contents(template_id, rail_id)
    items = []
    for section in data.get('sections', []):
        for content in section.get('contents', []):
            cid = content.get('contentRef') or content.get('id')
            if not cid:
                continue
            title = content.get('Title') or content.get('title') or cid
            kind, ref = api.rail_item_kind(content)
            plot = content.get('Description') or content.get('Synopsis') or ''
            year = content.get('Year')
            image = _vod_image(content)
            if kind == 'series':
                items.append(
                    {
                        'title': title, 'url': json.dumps({'series': ref}, separators=(',', ':')),
                        'image': image, 'fanart': image, 'plot': plot, 'year': year,
                        'action': 'seasons', 'isFolder': 'True',
                    }
                )
            else:
                items.append(
                    {
                        'title': title, 'url': json.dumps({'vod': cid}, separators=(',', ':')),
                        'image': image, 'fanart': image, 'plot': plot, 'year': year,
                        'action': 'play_vod',
                        'isFolder': 'False', 'isPlayable': 'True',
                    }
                )
    return items


@urldispatcher.register('listing', ['url'])
def listing(url):
    ref = json.loads(url)
    items = _rail_items(ref['template'], ref['rail'], api.content_lang())
    for i in items:
        i.update({'cm': _bookmark_cm(i)})
    directory.builder(items, content='videos')


@cache_function(60, 60)
def _seasons(series_ref, lang):
    data = api.series_seasons(series_ref, locale=lang)
    seasons = []
    for s in data.get('series', []):
        seasons.append(
            {
                'id': s.get('id'),
                'title': s.get('Title') or 'Season {0}'.format(s.get('SeasonNumber', '')),
                'plot': s.get('Description') or s.get('Synopsis') or '',
                'image': api.image_url('series', s.get('seriesRef') or series_ref, 'VerticalPoster', aspect='2x3', width=320),
            }
        )
    seasons.sort(key=lambda s: str(s['title']))
    return seasons


@urldispatcher.register('seasons', ['url'])
def seasons(url):
    series_ref = json.loads(url)['series']
    items = [
        {
            'title': s['title'], 'url': json.dumps({'season': s['id'], 'series': series_ref}, separators=(',', ':')),
            'image': s['image'], 'fanart': s['image'], 'plot': s['plot'],
            'action': 'episodes', 'isFolder': 'True',
        }
        for s in _seasons(series_ref, api.content_lang())
    ]
    if not items:
        items = [{'title': _i18n(30022), 'action': None}]
    directory.builder(items, content='videos')


@cache_function(30, 60)
def _episodes(season_ref, lang):
    data = api.season_episodes(season_ref, locale=lang)
    items = []
    for e in data.get('editorials', []):
        url, drm = api.episode_to_stream(e)
        if not url:
            continue
        num = e.get('EpisodeNumber') or e.get('episodeNumber')
        title = e.get('Title') or e.get('title') or e.get('id')
        label = 'E{0} - {1}'.format(num, title) if num else title
        items.append(
            {
                'title': label,
                'url': json.dumps({'url': url, 'drm': drm}, separators=(',', ':')),
                'image': api.image_url('tvshow', e.get('id'), 'HorizontalPoster', aspect='16x9', width=400),
                'plot': e.get('Description') or e.get('Synopsis') or '',
                'action': 'play_live',
                'isFolder': 'False', 'isPlayable': 'True',
            }
        )
    return items


@urldispatcher.register('episodes', ['url'])
def episodes(url):
    season_ref = json.loads(url)['season']
    items = _episodes(season_ref, api.content_lang())
    if not items:
        items = [{'title': _i18n(30022), 'action': None}]
    for i in items:
        i.update({'cm': _bookmark_cm(i)})
    directory.builder(items, content='videos')


@urldispatcher.register('search')
def search():
    import datetime

    term = kodi.inputDialog(heading=_i18n(30013))
    if not term:
        return
    data = api.search(term)
    rails = data.get('rails') or (data.get('data') or {}).get('rails') or []
    items = []
    for rail in rails:
        for section in rail.get('sections', []):
            for content in section.get('contents', []):
                item = _search_item(content, datetime)
                if item is not None:
                    items.append(item)
    if not items:
        items = [{'title': _i18n(30022), 'action': None}]
    for i in items:
        i.update({'cm': _bookmark_cm(i)})
    directory.builder(items, content='videos')


def _search_item(content, datetime):
    cid = content.get('contentRef') or content.get('id')
    if not cid:
        return None
    title = content.get('Title') or content.get('title') or cid
    plot = content.get('Description') or content.get('description') or content.get('Synopsis') or content.get('synopsis') or ''
    ctype = (content.get('contentType') or '').lower()
    itype = (content.get('type') or '').lower()

    if itype == 'stcu':
        channel = content.get('channel')
        start = content.get('start')
        end = content.get('end')
        try:
            when = datetime.datetime.fromtimestamp(int(start), datetime.timezone.utc).strftime('%d/%m %H:%M')
        except (TypeError, ValueError):
            when = ''
        label = '{0} ({1})'.format(title, when) if when else title
        return {
            'title': label,
            'url': json.dumps({'channel': channel, 'start': start, 'end': end}, separators=(',', ':')),
            'image': api.channel_logo(channel) if channel else '',
            'plot': plot, 'action': 'play_catchup',
            'isFolder': 'False', 'isPlayable': 'True',
        }

    if cid.endswith('_E0') or ctype in ('series', 'season'):
        ref = content.get('seriesRef') or (cid[:-3] if cid.endswith('_E0') else cid)
        return {
            'title': title, 'url': json.dumps({'series': ref}, separators=(',', ':')),
            'image': _vod_image(content), 'plot': plot, 'action': 'seasons',
            'isFolder': 'True',
        }

    return {
        'title': title, 'url': json.dumps({'vod': cid}, separators=(',', ':')),
        'image': _vod_image(content), 'plot': plot, 'action': 'play_vod',
        'isFolder': 'False', 'isPlayable': 'True',
    }


@urldispatcher.register('play_catchup', ['url'])
def play_catchup(url):
    import datetime

    ref = json.loads(url)
    stream_url, drm = _catchup_stream(ref.get('channel'), ref.get('start'), ref.get('end'), datetime)
    if not stream_url:
        kodi.infoDialog(_i18n(30022))
        return
    playback_url, content_token = _playout(stream_url, drm)
    _resolve(playback_url, content_token)


def _catchup_stream(channel_id, start, end, datetime):
    try:
        begin = datetime.datetime.fromtimestamp(int(start), datetime.timezone.utc).strftime('%Y%m%dT%H%M%S')
        finish = datetime.datetime.fromtimestamp(int(end), datetime.timezone.utc).strftime('%Y%m%dT%H%M%S')
    except (TypeError, ValueError):
        return None, None
    for ch in _live_channels():
        if ch['id'] == channel_id and ch.get('stcu'):
            url = ch['stcu'].replace('{startTime}', begin).replace('{endTime}', finish)
            return url, ch.get('drm')
    for ch in _live_channels():
        if ch['id'] == channel_id:
            return ch.get('url'), ch.get('drm')
    return None, None


@cache_function(24, 60 * 60)
def _playout(url, drm):
    return api.resolve_stream(url, drm)


@urldispatcher.register('play_live', ['url'])
def play_live(url):
    ref = json.loads(url)
    playback_url, content_token = _playout(ref['url'], ref.get('drm'))
    _resolve(playback_url, content_token)


@urldispatcher.register('play_vod', ['url'])
def play_vod(url):
    vod_id = json.loads(url)['vod']
    card = api.vod_mediacard(vod_id)
    if isinstance(card, dict) and 'data' in card and isinstance(card['data'], dict):
        card = card['data']
    stream_url, drm = None, None
    media = card.get('media')
    if isinstance(media, list) and media:
        stream_url, drm = media[0].get('uri'), media[0].get('drmId')
    if not stream_url or 'example.com' in stream_url:
        kodi.infoDialog(_i18n(30022))
        return
    playback_url, content_token = _playout(stream_url, drm)
    _resolve(playback_url, content_token)


def _widevine_available():
    try:
        cdm_dir = kodi.transPath('special://home/cdm')
        for name in os.listdir(cdm_dir):
            if 'widevine' in name.lower():
                return True
    except Exception:
        pass
    return False


def _ensure_widevine():
    if _widevine_available():
        return True
    try:
        import inputstreamhelper
        return bool(inputstreamhelper.Helper('mpd', drm='com.widevine.alpha').check_inputstream())
    except Exception:
        pass
    if kodi.yesnoDialog(_i18n(30066), heading=_i18n(30065)):
        kodi.execute('InstallAddon(script.module.inputstreamhelper)')
    return False


def _resolve(playback_url, content_token=None):
    dash = any(x in (playback_url or '') for x in ('.mpd', '.m3u8'))
    if content_token:
        if not _ensure_widevine():
            return
        licence_key = '{0}|nv-authorizations={1}&nv-tenant-id=nagra&Content-Type=application/octet-stream|R{{SSM}}|'.format(
            WIDEVINE_URL, content_token
        )
        directory.resolve(
            playback_url, dash=dash, licence_type='com.widevine.alpha', licence_key=licence_key,
        )
    else:
        directory.resolve(playback_url, dash=dash)
