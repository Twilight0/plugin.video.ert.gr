# -*- coding: utf-8 -*-

'''
    ERTflix Addon
    Author Twilight0

    SPDX-License-Identifier: GPL-3.0-only
    See LICENSES/GPL-3.0-only for more information.
'''

BASE_LINK = 'https://www.ertflix.gr'

# Nagra / OpenTV backend (reverse-engineered from Samsung Tizen app
# https://website.ertflix.opentv.com/samsung/index.html)
API_BASE = 'https://api.ertflix.opentv.com/'
IMAGE_BASE = 'https://imageservice.ertflix.opentv.com/images/v1/image/'
DRM_BASE = 'https://ertp8gz3.anycast.nagra.com/ERTP8GZ3'
WIDEVINE_URL = DRM_BASE + '/wvls/contentlicenseservice/v1/licenses'
PLAYREADY_URL = DRM_BASE + '/prls/contentlicenseservice/v1/licenses'

TENANT_HEADERS = {'nv-tenant-id': 'nagra', 'tenantId': 'nagra'}
DEVICE_HEADERS = {'Nagra-Device-Type': 'SmartTV', 'Nagra-Target': 'tv'}

# Guest templates from contentdelivery/v1/templateviews/hierarchy
TEMPLATES = {
    'home': 'c4cb773b-d7b2-40eb-bb28-a4ccd4ee88f8',
    'live': '19ae279d-ec0a-4331-9122-39c268bc626c',
    'series': '5e9e6155-5db5-43f2-ae97-d9aeb3e8ef39',
    'movies': '1d8f2437-ca79-4cf1-99df-f6f706756a43',
    'kids': 'a4a0f8d8-8acd-4235-81bd-a71b1d57e3f1',
    'documentaries': 'ccc72f99-34d0-46cc-a872-39c0772e5be7',
    'shows': '972b17e5-7ea9-48c2-acdd-37e65ca3dd70',
    'sports': 'dd232a0d-c6da-49e5-aff2-c756896ed273',
    'news': '93b8f97e-c4d4-46ba-ae4e-2ae59ac32628',
}
