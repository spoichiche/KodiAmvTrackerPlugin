import sys
import json
import os
from urllib.parse import urlencode, parse_qsl

import xbmcaddon
import xbmcgui
import xbmcplugin
import xbmc

from amvtrackerapi import Amv, AmvResultList, AmvTrackerDao

URL = sys.argv[0]
HANDLE = int(sys.argv[1])

def get_params(param_string):
    param_string = sys.argv[2][1:]
    if param_string:
        return dict(parse_qsl(param_string))
    return {}

def format_url(**kwargs):
    return '{}?{}'.format(URL, urlencode(kwargs))

def set_amv_sort_methods():
    xbmcplugin.setContent(HANDLE, 'musicvideos')
    xbmcplugin.addSortMethod(HANDLE, xbmcplugin.SORT_METHOD_FULLPATH)
    xbmcplugin.addSortMethod(HANDLE, xbmcplugin.SORT_METHOD_LABEL)
    xbmcplugin.addSortMethod(HANDLE, xbmcplugin.SORT_METHOD_TITLE)
    xbmcplugin.addSortMethod(HANDLE, xbmcplugin.SORT_METHOD_VIDEO_YEAR)
    xbmcplugin.addSortMethod(HANDLE, xbmcplugin.SORT_METHOD_DATEADDED)
    xbmcplugin.addSortMethod(HANDLE, xbmcplugin.SORT_METHOD_GENRE)
    xbmcplugin.addSortMethod(HANDLE, xbmcplugin.SORT_METHOD_STUDIO)
    xbmcplugin.addSortMethod(HANDLE, xbmcplugin.SORT_METHOD_VIDEO_RATING)
    xbmcplugin.addSortMethod(HANDLE, xbmcplugin.SORT_METHOD_LASTPLAYED)

def router(param_string):
    params = get_params(param_string)
    xbmc.log("AmvTracker plugin : url " + str(URL), xbmc.LOGINFO)

    AmvTrackerDao.init(xbmcplugin.getSetting(HANDLE, "dbfilepath"))

    if not params:
        list_root_dir()
    elif 'list_amvs' == params['action']:
        list_amv("All Amvs", AmvTrackerDao.getAllAmvs())
    elif 'list_favorites' == params['action']:
        list_amv("Favorite Amvs", AmvTrackerDao.getAllFavorites())
    elif 'list_lists' == params['action']:
        list_final_directories("Custom Lists", AmvTrackerDao.getCustomLists(), "list_list_amv", "")
    elif 'list_list_amv' == params['action']:
        list_amv(params['dirname'], AmvTrackerDao.getCustomListAmvs(params['dirname']))
    elif 'list_editors' == params['action']:
        list_final_directories("Editors", AmvTrackerDao.getAllEditors(), "list_editor_amv", "DefaultMusicRoles.png")
    elif 'list_editor_amv' == params['action']:
        list_amv(params['dirname']+"'s Amvs", AmvTrackerDao.getEditorAmvs(params['dirname']))
    elif 'list_studios' == params['action']:
        list_final_directories("Studios", AmvTrackerDao.getStudios(), "list_studio_amv", "DefaultStudios.png")
    elif 'list_studio_amv' == params['action']:
        list_amv(params['dirname']+"'s Amvs", AmvTrackerDao.getStudioAmvs(params['dirname']))
    elif 'list_genres' == params['action']:
        list_final_directories("Genres", AmvTrackerDao.getGenres(), "list_genre_amv", "DefaultGenre.png")
    elif 'list_genre_amv' == params['action']:
        list_amv(params['dirname']+" Amvs", AmvTrackerDao.getGenreAmvs(params['dirname']))
    elif 'list_years' == params['action']:
        list_final_directories("Years", AmvTrackerDao.getYears(), "list_year_amv", "DefaultYear.png")
    elif 'list_year_amv' == params['action']:
        list_amv(params['dirname']+"'s Amvs", AmvTrackerDao.getYearAmvs(params['dirname']))
    elif 'list_contests' == params['action']:
        list_final_directories("Contests", AmvTrackerDao.getContests(), "list_contest_amv", "DefaultMusicTop100.png")
    elif 'list_contest_amv' == params['action']:
        list_amv(params['dirname']+" Amvs", AmvTrackerDao.getContestAmvs(params['dirname']))
    elif 'list_animes' == params['action']:
        list_final_directories("Anime Sources", AmvTrackerDao.getAnimes(), "list_anime_amv", "DefaultTVShows.png")
    elif 'list_anime_amv' == params['action']:
        list_amv(params['dirname']+" Amvs", AmvTrackerDao.getAnimeAmvs(params['dirname']))
    elif 'list_artists' == params['action']:
        list_final_directories("Song Artists", AmvTrackerDao.getArtists(), "list_artist_amv", "DefaultArtist.png")
    elif 'list_artist_amv' == params['action']:
        list_amv(params['dirname']+" Amvs", AmvTrackerDao.getArtistAmvs(params['dirname']))
    elif 'list_song_genres' == params['action']:
        list_final_directories("Song Genres", AmvTrackerDao.getSongGenres(), "list_song_genre_amv", "DefaultMusicAlbums.png")
    elif 'list_song_genre_amv' == params['action']:
        list_amv(params['dirname']+" Amvs", AmvTrackerDao.getSongGenreAmvs(params['dirname']))

def icon_list_item(label, icon="", label2 = ""):
    liz = xbmcgui.ListItem(label=label)
    liz.setArt({'icon': icon})
    liz.setLabel2(label2)
    return liz

def list_root_dir():
    xbmcplugin.addDirectoryItem(HANDLE, format_url(action="list_amvs"), icon_list_item("All Amvs", "DefaultMusicVideoTitle.png"), True)
    xbmcplugin.addDirectoryItem(HANDLE, format_url(action="list_favorites"), icon_list_item("Favorites", "DefaultFavourites.png"), True)
    xbmcplugin.addDirectoryItem(HANDLE, format_url(action="list_lists"), icon_list_item("Custom Lists", ""), True)
    xbmcplugin.addDirectoryItem(HANDLE, format_url(action="list_editors"), icon_list_item("Editors", "DefaultDirector.png"), True)
    xbmcplugin.addDirectoryItem(HANDLE, format_url(action="list_studios"), icon_list_item("Studios", "DefaultStudios.png"), True)
    xbmcplugin.addDirectoryItem(HANDLE, format_url(action="list_genres"), icon_list_item("Genres", "DefaultGenre.png"), True)
    xbmcplugin.addDirectoryItem(HANDLE, format_url(action="list_years"), icon_list_item("Years", "DefaultYear.png"), True)
    xbmcplugin.addDirectoryItem(HANDLE, format_url(action="list_contests"), icon_list_item("Contests", "DefaultMusicTop100.png"), True)
    xbmcplugin.addDirectoryItem(HANDLE, format_url(action="list_animes"), icon_list_item("Anime Sources", "DefaultTVShows.png"), True)
    xbmcplugin.addDirectoryItem(HANDLE, format_url(action="list_artists"), icon_list_item("Song Artists", "DefaultArtist.png"), True)
    xbmcplugin.addDirectoryItem(HANDLE, format_url(action="list_song_genres"), icon_list_item("Song Genres", "DefaultMusicAlbums.png"), True)
    xbmcplugin.endOfDirectory(HANDLE)

def list_amv(category: str, amvList: AmvResultList):
    xbmcplugin.setPluginCategory(HANDLE, category)
    set_amv_sort_methods()

    for amv in amvList:
        list_item = build_list_item_from_amv(amv)
        xbmcplugin.addDirectoryItem(handle=HANDLE, url=list_item.getPath(), listitem=list_item)
    xbmcplugin.endOfDirectory(HANDLE)

def list_final_directories(category: str, dirList: list, urlAction: str, icon: str):
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

def list_contests():
    xbmcplugin.setPluginCategory(HANDLE, "Contests")
    xbmcplugin.addSortMethod(HANDLE, xbmcplugin.SORT_METHOD_LABEL)
    xbmcplugin.addSortMethod(HANDLE, xbmcplugin.SORT_METHOD_SIZE)

    for contest in AmvTrackerDao.getContests():
        list_item = icon_list_item(contest, "DefaultMusicTop100.png")
        xbmcplugin.addDirectoryItem(HANDLE, format_url(action="list_contest_amv", contest=contest), list_item, True)
    xbmcplugin.endOfDirectory(HANDLE)

def build_list_item_from_amv(amv: Amv):
    list_item = xbmcgui.ListItem(label=amv.getLabel(), offscreen=False)
    
    tags = list_item.getVideoInfoTag()
    tags.setUniqueIDs({'amvt2id': amv.getId()}, defaultuniqueid='amvt2id')
    tags.setMediaType('musicvideo')
    
    tags.setTitle(amv.getLabel()) #TODO add contitional title form
    tags.setDirectors(amv.getEditors())
    tags.setStudios([amv.getStudio()])
    tags.setPremiered(amv.getReleaseDate())
    tags.setArtists([amv.getSongArtist()])
    tags.setGenres(amv.getGenres())
    tags.setPlaycount(amv.get('play_count'))
    tags.setPlot(build_plot_info_string(amv))
    tags.addAvailableArtwork(get_thumbnail_path(amv.getThumbnailPath()), 'thumb')

    list_item.setArt({'thumb': get_thumbnail_path(amv.getThumbnailPath())})
    list_item.setProperty('IsPlayable', 'true')
    list_item.setPath(amv.get('local_file')) #TODO set playcount in a play action and xbmcplugin.setResolvedUrl

    list_item.addContextMenuItems(build_amv_context_menu(amv))

    return list_item

def build_plot_info_string(amv: Amv) -> str:
    amvGenres = " / ".join(amv.getGenres())
    animeList = "[CR] - ".join(amv.getAnimes())

    infoString = ("[B]Amv Genres : [/B]"+amvGenres+"[CR]" if amvGenres.strip() else "") \
        + ("[B]Song Artist : [/B]"+amv.getSongArtist()+"[CR]" if amv.getSongArtist().strip() else "") \
        + ("[B]Song Title : [/B]"+amv.getSongTitle()+"[CR]" if amv.getSongTitle().strip() else "") \
        + ("[B]Song Genre : [/B]"+amv.getSongGenre()+"[CR]" if amv.getSongGenre().strip() else "") \
        + ("[B]Date : [/B]"+amv.getReleaseDate()+"[CR]" if amv.getReleaseDate().strip() else "") \
        + ("[B]Studio : [/B]"+amv.getStudio()+"[CR]" if amv.getStudio().strip() else "") \
        + ("[B]Animes : [/B]"+animeList+"[CR]" if animeList.strip() else "") 
    return infoString
    
def get_thumbnail_path(vid_thumb_path):
    """
    process vid_thumb_path from database and return the correct filepath
    return str: the complete file path
    """
    if vid_thumb_path.startswith("\\") or vid_thumb_path.startswith("/"):
        return os.path.join( os.path.dirname(xbmcplugin.getSetting(HANDLE, "dbfilepath")), ".."+vid_thumb_path).replace("/", "\\")
    else:
        return vid_thumb_path

def build_amv_context_menu(amv: Amv):
    contextMenuList = list()

    if amv.isFavorite():
        contextMenuList.append(("Remove from AmvTracker Favorites", f"RunScript(plugin.video.amvtracker, removeFromFavorite, {amv.getId()})"))
    else:
        contextMenuList.append(("Add to AmvTracker Favorites", f"RunScript(plugin.video.amvtracker, addToFavorite, {amv.getId()})"))
    contextMenuList.append(("Add To List", f"RunScript(plugin.video.amvtracker, addToCustomLists, {amv.getId()})"))
    return contextMenuList

if __name__ == '__main__':
    if not xbmcplugin.getSetting(HANDLE, "dbfilepath"):
        xbmcaddon.Addon().openSettings()
    router(sys.argv[2][1:])
