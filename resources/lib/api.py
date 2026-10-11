# -*- coding: utf-8 -*-

'''
    ERTflix Addon
    Author Twilight0

    SPDX-License-Identifier: GPL-3.0-only
    See LICENSES/GPL-3.0-only for more information.
'''

import json
import time
import os
from urllib.parse import urlencode, quote

from .constants import API_BASE, IMAGE_BASE, TENANT_HEADERS, DEVICE_HEADERS

try:
    from tulip import kodi

    def _profile_dir():
        return kodi.dataPath

    def _is_greek():
        try:
            return 'Greek' in kodi.infoLabel('System.Language')
        except Exception:
            return True
except Exception:
    kodi = None

    def _profile_dir():
        return '/tmp/opencode/ertflix'

    def _is_greek():
        return True


try:
    from netclient import Net
    _net = Net()
except Exception:
    _net = None


def _lang_code():
    try:
        choice = kodi.setting('content_lang')
    except Exception:
        choice = '0'
    if choice == '1':
        return 'el_GR'
    if choice == '2':
        return 'en_GB'
    return 'el_GR' if _is_greek() else 'en_GB'


def content_lang():
    return _lang_code()


def _base_headers(token=None):
    headers = dict(TENANT_HEADERS)
    headers['Accept-Language'] = _lang_code()
    if token:
        headers['Authorization'] = 'Bearer ' + token
    headers.update(DEVICE_HEADERS)
    return headers


def _get_json(url, headers, params=None, timeout=20):
    if params:
        url = url + ('&' if '?' in url else '?') + urlencode(params)
    if _net is not None:
        # netclient decodes text as ASCII when the response has no charset
        # (JSON API) which strips all non-ASCII content: take raw bytes.
        resp = _net.http_GET(url, headers=headers, timeout=timeout)
        raw = resp.nodecode(True).content
        return json.loads(raw.decode('utf-8'))
    import urllib.request
    req = urllib.request.Request(url, headers=headers)
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        return json.loads(resp.read().decode('utf-8'))


def _post_json(url, payload, headers, timeout=20):
    body = json.dumps(payload).encode('utf-8') if not isinstance(payload, bytes) else payload
    hdrs = dict(headers)
    hdrs['Content-Type'] = 'application/json'
    if _net is not None:
        resp = _net.http_POST(url, body.decode('utf-8'), headers=headers, jdata=False, timeout=timeout)
        raw = resp.nodecode(True).content
        return json.loads(raw.decode('utf-8'))
    import urllib.request
    req = urllib.request.Request(url, data=body, headers=hdrs, method='POST')
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        return json.loads(resp.read().decode('utf-8'))


# ---------------------------------------------------------------------------
# Anonymous auth (guest flow from loginService.getAnonymousToken)
# ---------------------------------------------------------------------------

_token_cache = {'token': None, 'expiry': 0}


def _token_path():
    try:
        d = _profile_dir()
        os.makedirs(d, exist_ok=True)
        return os.path.join(d, 'opentv_token.json')
    except Exception:
        return '/tmp/opencode/ertflix/opentv_token.json'


def session_token():
    now = time.time()
    if _token_cache['token'] and now < _token_cache['expiry'] - 600:
        return _token_cache['token']
    path = _token_path()
    try:
        with open(path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        if data.get('token') and now < data.get('expiry', 0) - 600:
            _token_cache['token'] = data['token']
            _token_cache['expiry'] = data['expiry']
            return data['token']
    except Exception:
        pass
    data = _post_json(
        API_BASE + 'ias/v2/anonymoustoken', {},
        {'Content-Type': 'application/json', 'Accept': '*/*', **TENANT_HEADERS},
    )
    token = data['access_token']
    expiry = now + int(data.get('expires_in', 3888000))
    _token_cache['token'] = token
    _token_cache['expiry'] = expiry
    try:
        with open(path, 'w', encoding='utf-8') as f:
            json.dump({'token': token, 'expiry': expiry}, f)
    except Exception:
        pass
    return token


def api_get(path, params=None):
    return _get_json(API_BASE + path, _base_headers(session_token()), params=params)


def image_url(kind, ref, role, aspect='16x9', width=400):
    return '{0}{1}/{2}/{3}?aspect={4}&width={5}&imageFormat=webp'.format(
        IMAGE_BASE, kind, ref, role, aspect, width
    )


def channel_logo(channel_id, width=400):
    return image_url('Channel', channel_id, 'Logo', aspect='1x1', width=width)


# ---------------------------------------------------------------------------
# Catalog
# ---------------------------------------------------------------------------

def hierarchy(parental=18):
    return api_get('contentdelivery/v1/templateviews/hierarchy', {'parental': parental})


def template_summary(template_id, parental=18):
    return api_get(
        'contentdelivery/v1/templatesummary/{0}'.format(template_id), {'parental': parental}
    )


def rail_contents(template_id, rail_id, parental=18):
    return api_get(
        'contentdelivery/v1/templateviews/{0}/rails/{1}'.format(template_id, rail_id),
        {'parental': parental},
    )


def btv_services():
    return api_get('metadata/delivery/ERT/btv/services')


def epg_now(channel_csv):
    return api_get('metadata/v1/epg/now', {'channel': channel_csv, 'next': True})


def vod_mediacard(vod_id):
    return api_get('metadata/v1/vod/{0}/mediacard'.format(vod_id), {'deviceType': 'SmartTV'})


def series_seasons(series_ref, locale=None):
    return api_get(
        'metadata/delivery/ERT/vod/series',
        {
            'filter': json.dumps(
                {'seriesRef': series_ref, 'locale': locale or _lang_code()}, separators=(',', ':')
            ),
            'sort': '[["SeasonNumberNumeric", 1]]',
            'offset': 0,
            'limit': 300,
        },
    )


def season_episodes(season_ref, locale=None, limit=300, offset=0):
    return api_get(
        'metadata/delivery/v2/ERT/vod/editorials',
        {
            'filter': json.dumps(
                {'editorial.seasonRef': season_ref, 'locale': locale or _lang_code()},
                separators=(',', ':'),
            ),
            'sort': '[["editorial.episodeNumber", 1]]',
            'offset': offset,
            'limit': limit,
        },
    )


def search(q, page=1, limit=18, parental=18):
    return api_get(
        'contentdelivery/v1/templateviews/Search',
        {'q': q, 'page': page, 'limit': limit, 'parental': parental},
    )


def playout_token(drm_id, stream_url):
    return api_get(
        'urlbuilder/v1/playout/content/token',
        {'content_id': drm_id, 'type': 'account', 'content_URL': stream_url},
    )


def resolve_stream(stream_url, drm_id=None):
    '''Returns (playback_url, content_token or None). Radios (no drm) play directly.'''
    if not drm_id:
        return stream_url, None
    data = playout_token(drm_id, stream_url)
    url = data.get('playbackUrl') or data.get('cdnAccessToken') or stream_url
    token = None
    try:
        token = data['contentAuthToken']['content_token']
    except (KeyError, TypeError):
        pass
    return url, token


# ---------------------------------------------------------------------------
# Mappers (mirror mapService logic from the Tizen app)
# ---------------------------------------------------------------------------

def _smarttv_tech(technicals):
    for t in technicals or []:
        if 'SmartTV' in (t.get('deviceType') or []):
            try:
                av = t['media']['AV_PlaylistName']
                if av.get('uri'):
                    return av['uri'], av.get('drmId')
            except (KeyError, TypeError):
                continue
    return None, None


def episode_to_stream(episode):
    url, drm = _smarttv_tech(episode.get('technicals'))
    if url:
        return url, drm
    media = episode.get('media')
    if isinstance(media, list) and media:
        return media[0].get('uri'), media[0].get('drmId')
    if isinstance(media, dict):
        return media.get('uri'), media.get('drmId')
    return None, None


def rail_item_kind(item):
    '''Classify a rail section content into (kind, ref) for navigation.'''
    cid = item.get('id') or item.get('contentRef') or ''
    if item.get('seriesRef') or (cid.endswith('_E0') and item.get('type') == 'editorial'):
        series = item.get('seriesRef') or (item.get('MasterSeries') if isinstance(item.get('MasterSeries'), str) else None)
        if not series and cid.endswith('_E0'):
            series = cid[:-3]
        return 'series', series or cid
    if item.get('type') == 'series' or item.get('MasterSeries'):
        ref = item.get('MasterSeries') if isinstance(item.get('MasterSeries'), str) else cid
        return 'series', ref
    return 'vod', cid


def episode_label(item, season_txt='S', episode_txt='E'):
    parts = []
    try:
        if item.get('SeasonNumber'):
            parts.append('{0}.{1}'.format(season_txt, item['SeasonNumber']))
        num = item.get('EpisodeNumber') or item.get('episodeNumber')
        if num:
            parts.append('{0}.{1}'.format(episode_txt, num))
    except Exception:
        pass
    return ' '.join(parts)
