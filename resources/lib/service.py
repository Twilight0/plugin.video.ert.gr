# -*- coding: utf-8 -*-

'''
    ERTflix Addon
    Author Twilight0

    SPDX-License-Identifier: GPL-3.0-only
    See LICENSES/GPL-3.0-only for more information.
'''

try:
    from sqlite3 import dbapi2 as database
except ImportError:
    from pysqlite2 import dbapi2 as database

import xbmc
import xbmcaddon


__addon__ = xbmcaddon.Addon('plugin.video.ert.gr')


class Daemon:

    def __init__(self):

        self._service_setup()

        while not self.Monitor.abortRequested():

            if self.Monitor.waitForAbort(2):

                break

    def _service_setup( self ):

        self.Monitor = WatchChanges()
        self._get_settings()

    def _get_settings(self):

        self.metadata = __addon__.getSetting('metadata')
        self.pagination = __addon__.getSetting('pagination')
        self.threading = __addon__.getSetting('threading')


class WatchChanges(xbmc.Monitor):

    def __init__( self):

        xbmc.Monitor.__init__( self )

    def action(self):

        table = ['rel_list', 'rel_lib']

        filename = xbmc.translatePath('special://profile/addon_data/plugin.video.ert.gr/cache.db')

        dbcon = database.connect(filename)
        dbcur = dbcon.cursor()

        for t in table:

            try:

                dbcur.execute("DROP TABLE IF EXISTS {0}".format(t))
                dbcur.execute("VACUUM")
                dbcon.commit()

            except BaseException:

                pass

    def onSettingsChanged(self):

        self.action()


if __name__ == '__main__':

    Daemon()
