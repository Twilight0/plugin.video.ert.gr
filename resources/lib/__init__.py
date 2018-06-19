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
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
'''

from __future__ import absolute_import

from sys import argv
from tulip.compat import parse_qsl
from tulip.control import infoLabel
from resources.lib import ert

syshandle = int(argv[1])
sysaddon = argv[0]
params = dict(parse_qsl(argv[2].replace('?','')))

########################################################################################################################

action = params.get('action')
url = params.get('url')

########################################################################################################################

if 'audio' in infoLabel('Container.FolderPath') and action is None:
    action = 'radios'

__all__ = ["action", "url", "ert", "sysaddon", "syshandle", "params"]
