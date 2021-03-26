import xbmcplugin
import xbmcgui
import xbmcvfs
import xbmc
import xbmcaddon
import os
import sys
import requests
import json

addonID = 'script.domoticz.scenes'
addonVersion = '0.0.8'
addonDate = "24 Maart 2021"

__addon__ = xbmcaddon.Addon()
__addonname__ = __addon__.getAddonInfo('name')
__icon__ = __addon__.getAddonInfo('icon')


__quality__ = xbmcaddon.Addon(id=addonID).getSetting('quality')


def get_channel_content():
    url = "https://www.funcarrun.eu/api.php?&type=all_youtube_videos"
    r = requests.get(url)
    result = r.text
    data = json.loads(result)
    return data


def get_data():
    video_list = get_channel_content()

    data = video_list['items']
    video_list = []
    for v in data:
        if v['id']['kind'] == 'youtube#video':
            video_list.append(v)
    return video_list


def show_notification(msg):
    xbmc.executebuiltin('Notification(' + __addonname__ + ',' + msg + ',5000,' + __icon__ + ')')


def get_editions():
    url = 'https://www.funcarrun.eu/api.php?type=editions'
    r = requests.get(url)
    result = r.text
    data = json.loads(result)
    return data


def add_editions(addon_handle):
    editions = get_editions()
    for e in editions['editions']:
        title = e['title']
        thumbnail = e['thumbnail']

        listitem = xbmcgui.ListItem(label=title)
        listitem.setArt({'icon': thumbnail})
        listitem.setIsFolder(isFolder=True)

        # Example: plugin://plugin.video.example/?action=listing&category=Animals
        url = 'plugin://' + addonID + '?action=listing&category=' + title
        xbmcplugin.addDirectoryItem(handle=addon_handle, url=url, listitem=listitem, isFolder=True)


def run():
    addon_handle = int(sys.argv[1])
    xbmcplugin.setContent(addon_handle, 'videos')
    addonID = 'plugin.video.funcarrun'
    addonVersion = '0.0.2'
    addonDate = "25 Maart 2021"

    __addon__ = xbmcaddon.Addon()
    __addonname__ = __addon__.getAddonInfo('name')
    __icon__ = __addon__.getAddonInfo('icon')

    LIB_DIR = xbmcvfs.translatePath(os.path.join(xbmcaddon.Addon(id=addonID).getAddonInfo('path'), 'resources', 'lib'))
    sys.path.append(LIB_DIR)

    # Get plugin settings
    DEBUG = xbmcaddon.Addon(id=addonID).getSetting('debug')

    if (DEBUG) == 'true':
        xbmc.log("[ADDON] %s v%s (%s) is starting, ARGV = %s" % (addonID, addonVersion, addonDate, repr(sys.argv)),
                 xbmc.LOGINFO)

    videoList = get_data()

    #add_editions(addon_handle=addon_handle)

    for v in videoList:
        videoId = v['id']['videoId']
        uri = "plugin://plugin.video.youtube/?action=play_video&videoid=" + videoId
        title = v['snippet']['title']
        description = v['snippet']['description']
        thumbnail = v['snippet']['thumbnails']['high']['url']

        description = description + "\n\nKijk voor inschrijven op https://www.funcarrun.eu"
        listitem = xbmcgui.ListItem(label=v['snippet']['title'])
        listitem.setProperty('IsPlayable', 'true')
        listitem.setArt({'icon': thumbnail})

        xbmcplugin.addDirectoryItem(handle=addon_handle, url=uri, listitem=listitem, isFolder=False)

    xbmcplugin.addSortMethod(addon_handle, xbmcplugin.SORT_METHOD_LABEL)
    xbmcplugin.endOfDirectory(addon_handle)


def start():
    videoList = get_data()
    print(videoList)


if __name__ == "__main__":
    run()
