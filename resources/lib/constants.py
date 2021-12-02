# -*- coding: utf-8 -*-

'''
    ERTflix Addon
    Author Twilight0

    SPDX-License-Identifier: GPL-3.0-only
    See LICENSES/GPL-3.0-only for more information.
'''

BASE_LINK = 'https://www.ertflix.gr'
OLD_LINK = 'https://webtv.ert.gr'
DEVICE_KEY = '5ac9136c63fb4e682c94e13128540e43'
BASE_API_LINK = 'https://api.app.ertflix.gr/'

# to get codenames and ids for channels - GET METHOD
FILTER_NOW_ON_TV_TILES = ''.join(
    [
        BASE_API_LINK,
        'v1/EpgTile/FilterNowOnTvTiles?platformCodename=www'
    ]
)

# to get channel metadata - POST METHOD
# sample post data: {"platformCodename":"www","requestedTiles":[{"id":"prg.170440"}]}
GET_TILES = ''.join(
    [
        BASE_API_LINK,
        'v2/Tile/GetTiles?$headers=%7B%22Content-Type%22:%22application%2Fjson%3Bcharset%3Dutf-8%22,%22X-Api-Date-Format%22:%22iso%22,%22X-Api-Camel-Case%22:true%7D'
    ]
)


# to get codenames for regions and respect geolocked content - GET METHOD
GET_REGIONS = ''.join(
    [
        BASE_API_LINK,
        'v1/IpRegion/GetRegionsForIpAddress?platformCodename=www&$headers=%7B%22X-Api-Date-Format%22:%22iso%22,%22X-Api-Camel-Case%22:true%7D'
    ]
)

# probably helps on pagination - GET METHOD
GET_CONTENT = ''.join(
    [
        BASE_LINK,
        'v1/InsysGoCms/GetContents?platformCodename=www&categoryCodenames=footer-cms-top&page=1&limit=99&contentFlags=Image&$headers=%7B%22X-Api-Date-Format%22:%22iso%22,%22X-Api-Camel-Case%22:true%7D'
    ]
)

# requires codename to get stream links (eg. ept1-live) - GET METHOD
ACQUIRE_CONTENT = ''.join(
    [
        BASE_API_LINK,
        'v1/Player/AcquireContent?platformCodename=www&deviceKey={0}&codename={1}&t=1638218692856'
    ]
)

SEARCH_LINK = ''.join([BASE_LINK, '/?s={}'])
CATEGORY_LINK = ''.join([BASE_LINK, '/category'])
AJAX_URL = ''.join([BASE_LINK, '/wp-admin/admin-ajax.php'])

INDEX_LINK = ''.join([BASE_LINK, '/ekpompes/'])
RECENT_LINK = ''.join([BASE_LINK, '/vods'])
SHOWS_LINK = ''.join([OLD_LINK, '/shows'])

SPORTS_LINK = ''.join([CATEGORY_LINK, '/athlitika/'])

NEWS_LINK = ''.join([CATEGORY_LINK, '/enimerosi-24/'])
CARTOONS_LINK = ''.join([CATEGORY_LINK, '/pedika/'])
ENTERTAINMENT_LINK = ''.join([CATEGORY_LINK, '/psichagogia/'])
INTERVIEWS_LINK = ''.join([CATEGORY_LINK, '/synentefxeis/'])
ARCHIVE_LINK = ''.join([CATEGORY_LINK, '/arxeio/'])

ELLINIKA_DOCS = ''.join([CATEGORY_LINK, '/ellhnika-docs/'])
KSENA_DOCS = ''.join([CATEGORY_LINK, '/ksena-docs/'])

MUSIC_BOX_LINK = ''.join([CATEGORY_LINK, '/moysiko-koyti/'])
CONTEMPORARY_MUSIC_LINK = ''.join([CATEGORY_LINK, '/sygchroni-moysiki/'])
CLASSICAL_MUSIC_LINK = ''.join([CATEGORY_LINK, '/klasiki-moysiki/'])

MOVIES_LINK = ''.join([CATEGORY_LINK, '/tainies/'])
SERIES_LINK = ''.join([CATEGORY_LINK, '/ksenes-seires/'])
CATCHUP_LINK = ''.join([CATEGORY_LINK, '/ksenes-seires-catchup/'])
GREEK_SERIES_LINK = ''.join([CATEGORY_LINK, '/ellinikes-seires/'])
WEB_SERIES_LINK = ''.join([CATEGORY_LINK, '/web-series/'])

# ert1_link = ''.join([BASE_LINK, '/ert1-live/'])
# ert2_link = ''.join([BASE_LINK, '/ert2-live/'])
# ert3_link = ''.join([BASE_LINK, '/ert3-live/'])
# ertw_link = ''.join([BASE_LINK, '/ertworld-live/'])
# erts_link = ''.join([BASE_LINK, '/ert-sports-live/'])

RADIO_LINK = 'https://webradio.ert.gr'
RADIO_STREAM = 'http://radiostreaming.ert.gr'
DISTRICT_LINK = ''.join([RADIO_LINK, '/liveradio/list.html'])
CHANNEL_ID = 'UC0jVU-mK53vDQZcSZB5mVHg'
SCRAMBLE = (
    'eJwVzMEOgiAYAOBXaZzTBZZWN+1QzS3brGknh0JaGqD8LKz17s0H+L4vejC0naF14C99L1gGGBOH4rbfAIiV2oBnyqf/KkWjGRWkb2Xga5cqpd1ayr'
    'rjRvOhkgK4ALeSLzSfIaoeRcvHqQ2PH5qO0a0Zw+wQR7XF5spUCOdYZD1rib3k46lbTErzauAwoX2yS8+506XJ+z5keZHFF48sVpBY65QM6shY9PsD'
    '2wk9GA=='
)