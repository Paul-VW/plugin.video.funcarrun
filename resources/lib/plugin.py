import xbmcplugin
import xbmcgui
import xbmcvfs
import xbmc
import xbmcaddon
import os
import sys
import requests
import json

addonID = 'plugin.video.funcarrun'
addonVersion = '0.0.2'
addonDate = "24 Maart 2021"

__addon__ = xbmcaddon.Addon()
__addonname__ = __addon__.getAddonInfo('name')
__icon__ = __addon__.getAddonInfo('icon')


__quality__ = xbmcaddon.Addon(id=addonID).getSetting('quality')


def get_channel_content():
    url = "https://www.funcarrun.eu/apiv2.php?type=video"
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

    videoList = get_channel_content()
    listitem = xbmcgui.ListItem(label="Search")
    uri = "plugin://"
    xbmcplugin.addDirectoryItem(handle=addon_handle, url=uri, listitem=listitem, isFolder=False)
    for v in videoList:
        videoId = v['videoId']
        uri = "plugin://plugin.video.youtube/?action=play_video&videoid=" + videoId
        title = v['title']
        description = v['description']
        thumbnail = v['thumbUrl']
        description = description + "\n\nKijk voor inschrijven op https://www.funcarrun.eu"
        listitem = xbmcgui.ListItem(label=title)
        listitem.setInfo('video', {'plot': description })
        listitem.setInfo('video', {'plotoutline': description })
        listitem.setProperty('IsPlayable', 'true')
        listitem.setArt({'icon': thumbnail})

        xbmcplugin.addDirectoryItem(handle=addon_handle, url=uri, listitem=listitem, isFolder=False)

    xbmcplugin.addSortMethod(addon_handle, xbmcplugin.SORT_METHOD_LABEL)
    xbmcplugin.endOfDirectory(addon_handle)


def start():
    videoList = get_channel_content()
    print(videoList)


if __name__ == "__main__":
    run()
