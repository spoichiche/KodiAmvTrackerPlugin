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

#plugin URL : plugin://plugin.video.amvtracker/
URL = sys.argv[0]
#plugin handle (plugin id)
HANDLE = int(sys.argv[1])
#global params being processed (will initialised later)
params = None

def get_params():
    param_string = sys.argv[2][1:]
    if param_string:
        return dict(parse_qsl(param_string))
    return {}

def format_url(**kwargs):
    return '{}?{}'.format(URL, urlencode(kwargs))

def set_amv_sort_methods():
    """
    Set all the sorting options for amv type content listings
    """
    xbmcplugin.setContent(HANDLE, 'musicvideos')
    xbmcplugin.addSortMethod(HANDLE, xbmcplugin.SORT_METHOD_LABEL)
    xbmcplugin.addSortMethod(HANDLE, xbmcplugin.SORT_METHOD_TITLE)
    xbmcplugin.addSortMethod(HANDLE, xbmcplugin.SORT_METHOD_VIDEO_YEAR)
    xbmcplugin.addSortMethod(HANDLE, xbmcplugin.SORT_METHOD_GENRE)
    xbmcplugin.addSortMethod(HANDLE, xbmcplugin.SORT_METHOD_STUDIO)
    xbmcplugin.addSortMethod(HANDLE, xbmcplugin.SORT_METHOD_VIDEO_RATING)
    xbmcplugin.addSortMethod(HANDLE, xbmcplugin.SORT_METHOD_PLAYCOUNT)
    xbmcplugin.addSortMethod(HANDLE, xbmcplugin.SORT_METHOD_FULLPATH)

def router():
    """
    Main entry point
    """
    global params
    params = get_params()
    xbmc.log("AmvTracker plugin : url " + str(URL), xbmc.LOGDEBUG)
    
    AmvTrackerDao.init(xbmcplugin.getSetting(HANDLE, "dbfilepath"))

    if not params:
        list_root_dir()
    elif 'play_amv' == params['action']:
        play_amv(params['amvid'])
    elif 'list_amvs' == params['action']:
        list_amv(Locale.getString("mainmenu.all_amvs"), AmvTrackerDao.getAllAmvs())
    elif 'list_favorites' == params['action']:
        list_amv(Locale.getString("mainmenu.favorite_amvs"), AmvTrackerDao.getAllFavorites())
    elif 'list_lists' == params['action']:
        list_final_directories(Locale.getString("mainmenu.custom_lists"), AmvTrackerDao.getAllCustomLists(), "list_list_amv", "")
    elif 'list_list_amv' == params['action']:
        list_amv(params['dirname'], AmvTrackerDao.getCustomListAmvs(params['dirname']))
    elif 'list_editors' == params['action']:
        list_final_directories(Locale.getString("mainmenu.editors"), AmvTrackerDao.getAllEditors(), "list_editor_amv", "DefaultMusicRoles.png")
    elif 'list_editor_amv' == params['action']:
        list_amv(params['dirname'], AmvTrackerDao.getEditorAmvs(params['dirname']))
    elif 'list_studios' == params['action']:
        list_final_directories(Locale.getString("mainmenu.studios"), AmvTrackerDao.getStudios(), "list_studio_amv", "DefaultStudios.png")
    elif 'list_studio_amv' == params['action']:
        list_amv(params['dirname'], AmvTrackerDao.getStudioAmvs(params['dirname']))
    elif 'list_genres' == params['action']:
        list_final_directories(Locale.getString("mainmenu.genres"), AmvTrackerDao.getGenres(), "list_genre_amv", "DefaultGenre.png")
    elif 'list_genre_amv' == params['action']:
        list_amv(params['dirname'], AmvTrackerDao.getGenreAmvs(params['dirname']))
    elif 'list_years' == params['action']:
        list_final_directories(Locale.getString("mainmenu.years"), AmvTrackerDao.getYears(), "list_year_amv", "DefaultYear.png")
    elif 'list_year_amv' == params['action']:
        list_amv(params['dirname'], AmvTrackerDao.getYearAmvs(params['dirname']))
    elif 'list_contests' == params['action']:
        list_final_directories(Locale.getString("mainmenu.contests"), AmvTrackerDao.getContests(), "list_contest_amv", "DefaultMusicTop100.png")
    elif 'list_contest_amv' == params['action']:
        list_amv(params['dirname'], AmvTrackerDao.getContestAmvs(params['dirname']))
    elif 'list_animes' == params['action']:
        list_final_directories(Locale.getString("mainmenu.anime_sources"), AmvTrackerDao.getAnimes(), "list_anime_amv", "DefaultTVShows.png")
    elif 'list_anime_amv' == params['action']:
        list_amv(params['dirname'], AmvTrackerDao.getAnimeAmvs(params['dirname']))
    elif 'list_artists' == params['action']:
        list_final_directories(Locale.getString("mainmenu.song_artists"), AmvTrackerDao.getArtists(), "list_artist_amv", "DefaultArtist.png")
    elif 'list_artist_amv' == params['action']:
        list_amv(params['dirname'], AmvTrackerDao.getArtistAmvs(params['dirname']))
    elif 'list_song_genres' == params['action']:
        list_final_directories(Locale.getString("mainmenu.song_genres"), AmvTrackerDao.getSongGenres(), "list_song_genre_amv", "DefaultMusicAlbums.png")
    elif 'list_song_genre_amv' == params['action']:
        list_amv(params['dirname'], AmvTrackerDao.getSongGenreAmvs(params['dirname']))
    elif 'list_tags' == params['action']:
        list_tag_directories(int(params['tagid']))
    elif 'list_tag_amvs' == params['action']:
        list_amv(params['tagname'], AmvTrackerDao.getTagAmvs(int(params['tagid']), params['tagname']))

def icon_list_item(label: str, icon="", label2 = "") -> xbmcgui.ListItem:
    """
    Shortcut to create a xbmcgui.ListItem object with label and icon

    @param: label
    @param: icon
    @param: label2
    @returns: the list item
    """
    liz = xbmcgui.ListItem(label=label)
    liz.setArt({'icon': icon})
    liz.setLabel2(label2)
    return liz

def list_root_dir():
    """
    Main menu listings
    """
    xbmcplugin.addDirectoryItem(HANDLE, format_url(action="list_amvs"), icon_list_item(Locale.getString("mainmenu.all_amvs"), "DefaultMusicVideoTitle.png"), True)
    xbmcplugin.addDirectoryItem(HANDLE, format_url(action="list_favorites"), icon_list_item(Locale.getString("mainmenu.favorite_amvs"), "DefaultFavourites.png"), True)
    xbmcplugin.addDirectoryItem(HANDLE, format_url(action="list_lists"), icon_list_item(Locale.getString("mainmenu.custom_lists"), ""), True)
    xbmcplugin.addDirectoryItem(HANDLE, format_url(action="list_editors"), icon_list_item(Locale.getString("mainmenu.editors"), "DefaultDirector.png"), True)
    xbmcplugin.addDirectoryItem(HANDLE, format_url(action="list_studios"), icon_list_item(Locale.getString("mainmenu.studios"), "DefaultStudios.png"), True)
    xbmcplugin.addDirectoryItem(HANDLE, format_url(action="list_genres"), icon_list_item(Locale.getString("mainmenu.genres"), "DefaultGenre.png"), True)
    xbmcplugin.addDirectoryItem(HANDLE, format_url(action="list_years"), icon_list_item(Locale.getString("mainmenu.years"), "DefaultYear.png"), True)
    xbmcplugin.addDirectoryItem(HANDLE, format_url(action="list_contests"), icon_list_item(Locale.getString("mainmenu.contests"), "DefaultMusicTop100.png"), True)
    xbmcplugin.addDirectoryItem(HANDLE, format_url(action="list_animes"), icon_list_item(Locale.getString("mainmenu.anime_sources"), "DefaultTVShows.png"), True)
    xbmcplugin.addDirectoryItem(HANDLE, format_url(action="list_artists"), icon_list_item(Locale.getString("mainmenu.song_artists"), "DefaultArtist.png"), True)
    xbmcplugin.addDirectoryItem(HANDLE, format_url(action="list_song_genres"), icon_list_item(Locale.getString("mainmenu.song_genres"), "DefaultMusicAlbums.png"), True)
    add_tag_dir_listing(2)
    add_tag_dir_listing(3)
    add_tag_dir_listing(4)
    add_tag_dir_listing(5)
    add_tag_dir_listing(6)
    xbmcplugin.endOfDirectory(HANDLE)

def add_tag_dir_listing(tagId: int):
    if xbmcplugin.getSetting(HANDLE, "showTag"+str(tagId)+"Filter") == "true":
        tagName = AmvTrackerDao.getTagName(tagId)
        if tagName != "":
            xbmcplugin.addDirectoryItem(HANDLE, format_url(action="list_tags", tagid=tagId), icon_list_item(tagName, ""), True)

def list_amv(category: str, amvList: AmvResultList):
    """
    Generic listing of a list of amv

    @param category: the name of the page listing
    @param amvList
    """
    xbmcplugin.setPluginCategory(HANDLE, category)
    set_amv_sort_methods()

    for amv in amvList:
        list_item = build_list_item_from_amv(amv)
        xbmcplugin.addDirectoryItem(handle=HANDLE, url=list_item.getPath(), listitem=list_item)
    xbmcplugin.endOfDirectory(HANDLE)

def list_final_directories(category: str, dirList: list, urlAction: str, icon: str):
    """
    Generic listing for a list of amv directories

    @param category: the name of the page listing
    @param dirList: a list of tuples like ({directoryName}, {nb of amv in the directory})
    @param urlAction: the action to trigger on entering a directory
    @param icon: the icon to display for the directories
    """
    xbmcplugin.setPluginCategory(HANDLE, category)
    xbmcplugin.addSortMethod(HANDLE, xbmcplugin.SORT_METHOD_LABEL)
    xbmcplugin.addSortMethod(HANDLE, xbmcplugin.SORT_METHOD_SIZE)

    for row in dirList:
        if row[0].strip():
            list_item = icon_list_item(row[0], icon)
            if len(row) > 1:
                list_item.setLabel(row[0] + "  [LIGHT]("+str(row[1])+")[/LIGHT]")
                list_item.setInfo("video", {"size": row[1]})
            xbmcplugin.addDirectoryItem(HANDLE, format_url(action=urlAction, dirname=row[0]), list_item, True)
    xbmcplugin.endOfDirectory(HANDLE)

def list_tag_directories(tagId: int):
    xbmcplugin.setPluginCategory(HANDLE, AmvTrackerDao.getTagName(tagId))
    xbmcplugin.addSortMethod(HANDLE, xbmcplugin.SORT_METHOD_LABEL)
    xbmcplugin.addSortMethod(HANDLE, xbmcplugin.SORT_METHOD_SIZE)
    dirList = AmvTrackerDao.getTagList(tagId)
    for row in dirList:
        if row[0].strip():
            list_item = icon_list_item(row[0])
            if len(row) > 1:
                list_item.setLabel(row[0] + "  [LIGHT]("+str(row[1])+")[/LIGHT]")
                list_item.setInfo("video", {"size": row[1]})
            xbmcplugin.addDirectoryItem(HANDLE, format_url(action="list_tag_amvs", tagid=tagId, tagname=row[0]), list_item, True)
    xbmcplugin.endOfDirectory(HANDLE)

def build_list_item_from_amv(amv: Amv) -> xbmcgui.ListItem:
    """
    Builds a xbmcgui.ListItem object from an Amv

    @param amv
    @return: xbmcgui.ListItem representing an amv
    """
    amvLabel = build_amv_label(amv)
    list_item = xbmcgui.ListItem(label=amvLabel, offscreen=False)
    
    tags = list_item.getVideoInfoTag()
    tags.setUniqueIDs({'amvt2id': amv.getId()}, defaultuniqueid='amvt2id')
    tags.setMediaType('musicvideo')
    
    tags.setTitle(amvLabel if xbmcplugin.getSetting(HANDLE, "setAmvLabelAsTitle") == "true" else amv.getTitle())
    tags.setDirectors(amv.getEditors())
    tags.setStudios([amv.getStudio()])
    tags.setPremiered(amv.getReleaseDate())
    tags.setArtists([amv.getSongArtist()])
    tags.setGenres(amv.getGenres())
    tags.setPlaycount(amv.getPlaycount())
    tags.setPlot(build_plot_info_string(amv))
    tags.setFilenameAndPath(get_amv_filepath(amv.getFilepath()))
    
    if amv.getUserRating() is not None and amv.getUserRating() != '':
        tags.setRating(amv.getUserRating(), 1, "AmvTrackerRating", True)

    tags.addAvailableArtwork(get_thumbnail_path(amv.getThumbnailPath()), 'thumb')

    list_item.setArt({'thumb': get_thumbnail_path(amv.getThumbnailPath())})
    list_item.setIsFolder(False)
    list_item.setProperty('IsPlayable', 'true')
    list_item.setPath(format_url(action='play_amv', amvid=amv.getId()))

    list_item.addContextMenuItems(build_amv_context_menu(amv))

    return list_item

def build_amv_label(amv: Amv) -> str:
        editors = amv.getEditors()
        if len(editors) == 1:
            return editors[0] + " - " + amv.getTitle()
        elif len(editors) == 2:
            return editors[0] + " / " + editors[1] + " - " + amv.getTitle()
        elif len(editors) > 2:
            return editors[0] + " " + Locale.getString("amvinfo.andMore") + " - " + amv.getTitle()
        else:
            return amv.getTitle()

def build_plot_info_string(amv: Amv) -> str:
    """
    Build and format a string containing all the data that should be contained in the amv plot field

    @param amv: the amv
    @return: the plot as a string
    """
    infoString = ""

    if xbmcplugin.getSetting(HANDLE, "setPlaycountInPlot") == "true":
        infoString += ("[B]"+Locale.getString("amvinfo.playcount")+" : [/B]"+str(amv.getPlaycount())+"[CR]" if str(amv.getPlaycount()).strip() else "")
    if xbmcplugin.getSetting(HANDLE, "setGenreInPlot") == "true":
        amvGenres = " / ".join(amv.getGenres())
        infoString += ("[B]"+Locale.getString("amvinfo.amv_genre")+" : [/B]"+amvGenres+"[CR]" if amvGenres.strip() else "")
    if xbmcplugin.getSetting(HANDLE, "setArtistInPlot") == "true":
        infoString += ("[B]"+Locale.getString("amvinfo.song_artist")+" : [/B]"+amv.getSongArtist()+"[CR]" if amv.getSongArtist().strip() else "")
    if xbmcplugin.getSetting(HANDLE, "setSongTitleInPlot") == "true":
        infoString += ("[B]"+Locale.getString("amvinfo.song_title")+" : [/B]"+amv.getSongTitle()+"[CR]" if amv.getSongTitle().strip() else "")
    if xbmcplugin.getSetting(HANDLE, "setSongGenreInPlot") == "true":
        infoString += ("[B]"+Locale.getString("amvinfo.song_genre")+" : [/B]"+amv.getSongGenre()+"[CR]" if amv.getSongGenre().strip() else "")
    if xbmcplugin.getSetting(HANDLE, "setDateInPlot") == "true":
        infoString += ("[B]"+Locale.getString("amvinfo.date")+" : [/B]"+amv.getReleaseDate()+"[CR]" if amv.getReleaseDate().strip() else "")
    if xbmcplugin.getSetting(HANDLE, "setStudioInPlot") == "true":
        infoString += ("[B]"+Locale.getString("amvinfo.studio")+" : [/B]"+amv.getStudio()+"[CR]" if amv.getStudio().strip() else "")
    if xbmcplugin.getSetting(HANDLE, "setRatingInPlot") == "true":
        infoString += ("[B]"+Locale.getString("amvinfo.user_rating")+" : [/B]"+str(amv.getUserRating())+" / 10[CR]" if str(amv.getUserRating()).strip() else "")
    if xbmcplugin.getSetting(HANDLE, "setAnimesInPlot") == "true":
        animeList = "[CR] - ".join(amv.getAnimes())
        infoString += ("[B]"+Locale.getString("amvinfo.animes")+" : [/B]"+animeList+"[CR]" if animeList.strip() else "")
    if xbmcplugin.getSetting(HANDLE, "setContestsInPlot") == "true":
        contestsList = "[CR] - ".join(amv.getContests())
        infoString += ("[B]"+Locale.getString("amvinfo.contests")+" : [/B]"+contestsList+"[CR]" if contestsList.strip() else "")

    return infoString

def get_amv_filepath(amvFilepath:str) -> str:
    """
    Process amv file path from database and return the correct filepath for Kodi playback
    @param amvFilepath: the amv file path present in the database
    @return: the complete file path
    """
    if xbmcplugin.getSetting(HANDLE, "doFilepathSubstitution") == "true":
        amvFilepath = amvFilepath.replace(xbmcplugin.getSetting(HANDLE, "filepathSubstitutionReplace"), xbmcplugin.getSetting(HANDLE, "filepathSubstitutionWith"))
    return amvFilepath

    
def get_thumbnail_path(vid_thumb_path:str) -> str:
    """
    Process vid_thumb_path from database and return the correct filepath
    @param vid_thumb_path: the thumbpath present in the database
    @return: the complete file path
    """
    if vid_thumb_path.startswith("\\") or vid_thumb_path.startswith("/"):
        return os.path.join( os.path.dirname(xbmcplugin.getSetting(HANDLE, "dbfilepath")), ".."+vid_thumb_path)
    else:
        return vid_thumb_path

def build_amv_context_menu(amv: Amv):
    contextMenuList = list()

    ### Add / Remove from favorite actions
    doRefresh = "doRefresh" if params['action'] == "list_favorites" else "noRefresh"
    if amv.isFavorite():
        contextMenuList.append((Locale.getString("contextmenu.remove_from_favorites"), f"RunScript(plugin.video.amvtracker, removeFromFavorite, {amv.getId()}, {doRefresh})"))
    else:
        contextMenuList.append((Locale.getString("contextmenu.add_to_favorites"), f"RunScript(plugin.video.amvtracker, addToFavorite, {amv.getId()}, {doRefresh})"))
    
    ### Add / Remove from custom list action
    contextMenuList.append((Locale.getString("contextmenu.add_to_list"), f"RunScript(plugin.video.amvtracker, addToCustomLists, {amv.getId()}, noRefresh)"))
    doRefresh = "doRefresh" if "list_list_amv" == params['action'] else "noRefresh"
    contextMenuList.append((Locale.getString("contextmenu.remove_from_list"), f"RunScript(plugin.video.amvtracker, removeFromCustomLists, {amv.getId()}, {doRefresh})"))

    ### Set rating action
    contextMenuList.append((Locale.getString("contextmenu.set_rating"), f"RunScript(plugin.video.amvtracker, setRating, {amv.getId()}, doRefresh)"))

    return contextMenuList

def play_amv(amvid: str):
    """
    Play action : set playcount++ then setResolvedUrl the item to play for Kodi
    @param amvid:
    """
    xbmc.log("AmvTracker plugin : play amv " + amvid, xbmc.LOGDEBUG)
    
    amv = AmvTrackerDao.getAmv(amvid)
    list_item = build_list_item_from_amv(amv)
    list_item.setPath(get_amv_filepath(amv.getFilepath()))
    xbmcplugin.setResolvedUrl(HANDLE, True, list_item)

    AmvTrackerDao.incrementPlaycount(amv.getId())

if __name__ == '__main__':
    if not xbmcplugin.getSetting(HANDLE, "dbfilepath"):
        xbmcaddon.Addon().openSettings()
    router()
