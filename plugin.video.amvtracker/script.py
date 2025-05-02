import sys
import json
import os
from urllib.parse import urlencode, parse_qsl

import xbmcaddon
import xbmcgui
import xbmcplugin
import xbmc

from amvtrackerapi import Amv, AmvResultList, AmvTrackerDao
from locale import Locale

xbmc.log("AmvTracker scripts : url = " + str(sys.argv), xbmc.LOGINFO)
addon = xbmcaddon.Addon()
addonName = addon.getAddonInfo('name')

def getUserSelectedList(amvLists: list) -> str:
    selectList = list()
    for amvList in amvLists:
        selectList.append(amvList[0])
    select = xbmcgui.Dialog().select(Locale.getString("dialog.select_custom_list"), selectList)
    return "" if select == -1 else selectList[select]

def getUserSelectedRating() -> str:
    selectList = ("10", "9.5", "9", "8.5", "8", "7.5", "7", "6.5", "6", "5.5", "5", "4.5", "4", "3.5", "3", "2.5", "2", "1.5", "1", "0.5", "0")
    select = xbmcgui.Dialog().select(Locale.getString("contextmenu.set_rating"), selectList)
    return "" if select == -1 else selectList[select]

def processContextMenuActions():
    amvId = sys.argv[2]
    doRefresh = sys.argv[3] == "doRefresh"

    if "addToFavorite" == action:
        AmvTrackerDao.addAmvToFavorites(amvId)
        xbmcgui.Dialog().ok(addonName, Locale.getString("dialog.added_favorite_success"))
    elif "removeFromFavorite" == action:
        AmvTrackerDao.removeAmvFromFavorites(amvId)
        xbmcgui.Dialog().ok(addonName, Locale.getString("dialog.removed_favorite_success"))
    elif "addToCustomLists" == action:
        listname = getUserSelectedList(AmvTrackerDao.getCustomListsWithoutAmv(amvId))
        if listname != "":
            AmvTrackerDao.addToCustomList(amvId, listname)
            xbmcgui.Dialog().ok(addonName, Locale.getFormatedString("dialog.added_to_custom_list_success", listname))
    elif "removeFromCustomLists" == action:
        listname = getUserSelectedList(AmvTrackerDao.getCustomListsWithAmv(amvId))
        if listname != "":
            AmvTrackerDao.removeFromCustomList(amvId, listname)
            xbmcgui.Dialog().ok(addonName, Locale.getFormatedString("dialog.removed_from_custom_list_success", listname))
    elif "setRating" == action:
        rating = getUserSelectedRating()
        if rating != "":
            AmvTrackerDao.setRating(amvId, float(rating))
            xbmcgui.Dialog().ok(addonName, Locale.getString("dialog.rating_set_success"))
    
    if doRefresh:
        xbmc.executebuiltin("Container.Refresh")

if __name__ == '__main__':
    action = sys.argv[1]
    xbmc.log("AmvTracker scripts : dbpath = " + str(addon.getSetting('dbfilepath')), xbmc.LOGINFO)
    
    AmvTrackerDao.init(addon.getSetting('dbfilepath'))
    processContextMenuActions()