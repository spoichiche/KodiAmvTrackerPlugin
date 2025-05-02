import sys
import json
import os
from urllib.parse import urlencode, parse_qsl

import xbmcaddon
import xbmcgui
import xbmcplugin
import xbmc

from amvtrackerapi import Amv, AmvResultList, AmvTrackerDao

xbmc.log("AmvTracker scripts : url = " + str(sys.argv), xbmc.LOGINFO)
addon = xbmcaddon.Addon()
addonName = addon.getAddonInfo('name')

def getUserSelectedList() -> str:
    amvLists = AmvTrackerDao.getCustomLists()
    selectList = list()
    for amvList in amvLists:
        selectList.append(amvList[0])
    select = xbmcgui.Dialog().select("Custom lists", selectList)
    return "" if select == -1 else selectList[select]

if __name__ == '__main__':
    action = sys.argv[1]
    xbmc.log("AmvTracker scripts : dbpath = " + str(addon.getSetting('dbfilepath')), xbmc.LOGINFO)
    
    AmvTrackerDao.init(addon.getSetting('dbfilepath'))

    if "addToFavorite" == action:
        amvId = sys.argv[2]
        AmvTrackerDao.addAmvToFavorites(amvId)
        xbmcgui.Dialog().ok(addonName, "Amv succesfully added to AmvTracker's favorite")
        xbmc.executebuiltin("Container.Refresh")
    elif "removeFromFavorite" == action:
        amvId = sys.argv[2]
        AmvTrackerDao.removeAmvFromFavorites(amvId)
        xbmcgui.Dialog().ok(addonName, "Amv succesfully removed from AmvTracker's favorite")
        xbmc.executebuiltin("Container.Refresh")
    elif "addToCustomLists" == action:
        amvId = sys.argv[2]
        listname = getUserSelectedList()
        if listname != "":
            AmvTrackerDao.addToCustomList(amvId, listname)
            xbmcgui.Dialog().ok(addonName, f"Amv succesfully added to list : {listname}")
    elif "removeFromCustomLists" == action:
        amvId = sys.argv[2]
        listname = getUserSelectedList()
        if listname != "":
            AmvTrackerDao.removeFromCustomList(amvId, listname)
            xbmcgui.Dialog().ok(addonName, f"Amv succesfully removed from list : {listname}")