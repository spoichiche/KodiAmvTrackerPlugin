import re
import xbmc
import xbmcaddon

class Locale():
    def getString(strid: str) -> str:
        res = xbmcaddon.Addon().getLocalizedString(Locale.STRINGS[strid])
        xbmc.log("AmvTracker getString : " + str(xbmcaddon.Addon().getLocalizedString(32031)), xbmc.LOGINFO)
        return res

    def getFormatedString(strid: str, param: str) -> str:
        localeString = re.sub("{.*}", "{}", xbmcaddon.Addon().getLocalizedString(Locale.STRINGS[strid])) 
        return localeString.format(param)

    STRINGS = \
    {
        "settings.database_path"                    : 32001
        ,"mainmenu.all_amvs"                        : 32002
        ,"mainmenu.favorite_amvs"                   : 32032
        ,"mainmenu.custom_lists"                    : 32003
        ,"mainmenu.editors"                         : 32004
        ,"mainmenu.studios"                         : 32005
        ,"mainmenu.genres"                          : 32006
        ,"mainmenu.years"                           : 32007
        ,"mainmenu.contests"                        : 32008
        ,"mainmenu.anime_sources"                   : 32009
        ,"mainmenu.song_artists"                    : 32010
        ,"mainmenu.song_genres"                     : 32011
        ,"amvinfo.amv_genre"                        : 32012
        ,"amvinfo.song_artist"                      : 32013
        ,"amvinfo.song_title"                       : 32014
        ,"amvinfo.song_genre"                       : 32015
        ,"amvinfo.date"                             : 32016
        ,"amvinfo.studio"                           : 32017
        ,"amvinfo.animes"                           : 32018
        ,"amvinfo.user_rating"                      : 32019
        ,"contextmenu.add_to_favorites"             : 32020
        ,"contextmenu.remove_from_favorites"        : 32021
        ,"contextmenu.add_to_list"                  : 32022
        ,"contextmenu.remove_from_list"             : 32023
        ,"contextmenu.set_rating"                   : 32024
        ,"dialog.added_favorite_success"            : 32025
        ,"dialog.removed_favorite_success"          : 32026
        ,"dialog.select_custom_list"                : 32027
        ,"dialog.added_to_custom_list_success"      : 32028
        ,"dialog.removed_from_custom_list_success"  : 32029
        ,"dialog.setted_rating_success"             : 32030
        ,"menu.editors_amv"                         : 32031
    }