# -*- coding: utf-8 -*-

'''
    ERTflix Addon
    Author Twilight0

    SPDX-License-Identifier: GPL-3.0-only
    See LICENSES/GPL-3.0-only for more information.
'''

import sys
from tulip.init import sysaddon, syshandle, params
from urldispatcher import urldispatcher
# noinspection PyUnresolvedReferences
from resources.lib import navigator, utils  # noqa: F401  (route registration)


def main(argv=None):

    if argv is None:
        argv = sys.argv

    queries = dict(params)
    action = queries.get('action', 'root')
    urldispatcher.dispatch(action, queries)


if __name__ == '__main__':

    sys.exit(main())
