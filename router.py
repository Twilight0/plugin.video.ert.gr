# -*- coding: utf-8 -*-

'''
    ERTflix Addon
    Author Twilight0

    SPDX-License-Identifier: GPL-3.0-only
    See LICENSES/GPL-3.0-only for more information.
'''

from __future__ import absolute_import

import sys
from tulip.compat import parse_qsl
from tulip.control import infoLabel
from tulip.url_dispatcher import urldispatcher
# noinspection PyProtectedMember, PyUnresolvedReferences
from resources.lib import navigator, utils


def main(argv=None):

    if sys.argv: argv = sys.argv

    params = dict(parse_qsl(argv[2][1:]))
    action = params.get('action', 'root')
    if 'audio' in infoLabel('Container.FolderPath') and action in [None, 'root']:
        action = 'radios'
    urldispatcher.dispatch(action, params)


if __name__ == '__main__':

    utils.keys_registration()
    sys.exit(main())
