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
BASE_API_LINK = 'https://api.app.ertflix.gr'
VOD_LINK = '/'.join([BASE_LINK, 'vod/{0}'])
LIST_OF_LISTS_LINK = '/'.join([BASE_LINK, 'list?imageRole=photo&title={title}&pageCodename={pagecodename}&backUrl=/show/{backurl}&sectionCodename={sectioncodename}'])
NEWS_LINK = '/'.join([BASE_LINK, 'list?imageRole=photo&title=%CE%95%CE%B9%CE%B4%CE%AE%CF%83%CE%B5%CE%B9%CF%82&pageCodename=news&backUrl=/show/news&sectionCodename=eideseis'])
ENTERTAINMENT_LINK = '/'.join([BASE_LINK, 'list?imageRole=poster&title=%CE%A8%CF%85%CF%87%CE%B1%CE%B3%CF%89%CE%B3%CE%AF%CE%B1&backUrl=/show/&sectionCodename=psukhagogia-2'])
INFO_LINK = '/'.join([BASE_LINK, 'show/news'])
MOVIES_LINK = '/'.join([BASE_LINK, 'show/movies'])
SERIES_LINK = '/'.join([BASE_LINK, 'show/series'])
SHOWS_LINK = '/'.join([BASE_LINK, 'show/ekpompes'])
SPORTS_LINK = '/'.join([BASE_LINK, 'show/sport'])
ARCHIVE_LINK = '/'.join([BASE_LINK, 'show/archives'])
KIDS_LINK = '/'.join([BASE_LINK, 'show/children'])
INDEX_LINK = 'https://www.ert.gr/index/'

# to get codenames and ids for channels - GET METHOD
FILTER_NOW_ON_TV_TILES = '/'.join(
    [
        BASE_API_LINK,
        'v1/EpgTile/FilterNowOnTvTiles?platformCodename=www'
    ]
)

# to get video tiles - POST METHOD
FILTER_TILES = '/'.join(
    [
        BASE_API_LINK,
        'v2/Tile/FilterTiles?$headers=%7B%22Content-Type%22:%22application%2Fjson%3Bcharset%3Dutf-8%22,%22X-Api-Date-Format%22:%22iso%22,%22X-Api-Camel-Case%22:true%7D'
    ]
)

# to get channel metadata - POST METHOD
GET_TILES = '/'.join(
    [
        BASE_API_LINK,
        'v2/Tile/GetTiles?$headers=%7B%22Content-Type%22:%22application%2Fjson%3Bcharset%3Dutf-8%22,%22X-Api-Date-Format%22:%22iso%22,%22X-Api-Camel-Case%22:true%7D'
    ]
)


# to get codenames for regions and respect geolocked content - GET METHOD
GET_REGIONS = '/'.join(
    [
        BASE_API_LINK,
        'v1/IpRegion/GetRegionsForIpAddress?platformCodename=www&$headers=%7B%22X-Api-Date-Format%22:%22iso%22,%22X-Api-Camel-Case%22:true%7D'
    ]
)

# to get additional content - GET METHOD
GET_PAGE_CONTENT = '/'.join(
    [
        BASE_API_LINK,
        'v1/InsysGoPage/GetPageContent?platformCodename=www&page={0}&limit=5&pageCodename={1}&$headers=%7B%22X-Api-Date-Format%22:%22iso%22,%22X-Api-Camel-Case%22:true%7D'
    ]
)

# to get selected content from a category - GET METHOD
GET_SECTION = '/'.join(
    [
        BASE_API_LINK,
        'v1/InsysGoPage/GetSectionContent?platformCodename=www&page={0}&limit=50&sectionCodename={1}&$headers=%7B%22X-Api-Date-Format%22:%22iso%22,%22X-Api-Camel-Case%22:true%7D'
    ]
)

# to get details from a tv series - GET METHOD
GET_SERIES_DETAILS = '/'.join(
    [
        BASE_API_LINK,
        'v1/Tile/GetSeriesDetails?platformCodename=www&id={0}&$headers=%7B%22X-Api-Date-Format%22:%22iso%22,%22X-Api-Camel-Case%22:true%7D'
    ]
)

# requires codename to get stream links (eg. ept1-live) - GET METHOD
ACQUIRE_CONTENT = '/'.join(
    [
        BASE_API_LINK,
        'v1/Player/AcquireContent?platformCodename=www&deviceKey={0}&codename={1}'
    ]
)

SEARCH = '/'.join(
    [
        BASE_API_LINK,
        'v1/Tile/Search?$headers=%7B%22Content-Type%22:%22application%2Fjson%3Bcharset%3Dutf-8%22,%22X-Api-Date-Format%22:%22iso%22,%22X-Api-Camel-Case%22:true%7D'
    ]
)

RADIO_LINK = 'https://webradio.ert.gr'
RADIO_STREAM = 'http://radiostreaming.ert.gr'
DISTRICT_LINK = '/'.join([RADIO_LINK, 'liveradio/list.html'])
CHANNEL_ID = 'UC0jVU-mK53vDQZcSZB5mVHg'
SCRAMBLE = (
    'eJwVzMEOgiAYAOBXaZzTBZZWN+1QzS3brGknh0JaGqD8LKz17s0H+L4vejC0naF14C99L1gGGBOH4rbfAIiV2oBnyqf/KkWjGRWkb2Xga5cqpd1ayr'
    'rjRvOhkgK4ALeSLzSfIaoeRcvHqQ2PH5qO0a0Zw+wQR7XF5spUCOdYZD1rib3k46lbTErzauAwoX2yS8+506XJ+z5keZHFF48sVpBY65QM6shY9PsD'
    '2wk9GA=='
)
