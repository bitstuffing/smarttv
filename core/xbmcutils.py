
import xbmcplugin
import xbmcaddon
import xbmc
import xbmcgui
import xbmcvfs
import os
import urllib
from core.logger import logger

class XBMCUtils():

    @staticmethod
    def getAddonInfo(property,idAddon='com.github.bitstuffing.smarttv'):
        return xbmcaddon.Addon(id=idAddon).getAddonInfo(property)

    @staticmethod
    def getSettingFromContext(context,setting):
        return xbmcplugin.getSetting(int(context), setting)

    @staticmethod
    def getSetting(property,idAddon="com.github.bitstuffing.smarttv"):
        xbmcaddon.Addon(id=idAddon).getSetting(property)

    @staticmethod
    def isWindowsPlatform():
        return xbmc.getCondVisibility("system.platform.windows")

    @staticmethod
    def isAndroidPlatform():
        return xbmc.getCondVisibility("System.Platform.Android")

    @staticmethod
    def isRaspberryPlatform():
        return xbmc.getCondVisibility("System.Platform.Linux.RaspberryPi")

    @staticmethod
    def isLinuxPlatform():
        return xbmc.getCondVisibility("System.Platform.Linux")

    @staticmethod
    def getAddonsDir():
        separatorChar = '/'
        if XBMCUtils.isWindowsPlatform():
            logger.debug("Detected Windows system...")
            separatorChar = "\\"
        #addons_dir = xbmc.("special://home"+separatorChar+"addons"+separatorChar)
        addons_dir = xbmcvfs.translatePath("special://home"+separatorChar+"addons"+separatorChar)
        return addons_dir

    @staticmethod
    def getSeparatorChar():
        separatorChar = "/"
        if XBMCUtils.isWindowsPlatform():
            separatorChar = "\\"
        return separatorChar

    @staticmethod
    def getPathFixedFrom(path):
        separatorChar = XBMCUtils.getSeparatorChar()
        #return xbmc.translatePath(path[path.rfind(separatorChar)+1:])
        return xbmcvfs.translatePath(path[path.rfind(separatorChar)+1:])

    @staticmethod
    def executeScript(path):
        xbmc.executebuiltin('RunScript('+path+')')

    @staticmethod
    def getAddon(idAddon="com.github.bitstuffing.smarttv"):
        return xbmcaddon.Addon(id=idAddon)

    @staticmethod
    def getString(id):
        return xbmc.getLocalizedString(id)

    @staticmethod
    def getDialog():
        return xbmcgui.Dialog()

    @staticmethod
    def getDialogProgress():
        return xbmcgui.DialogProgress()

    @staticmethod
    def getRightString(string):
        return xbmc.makeLegalFilename(string)

    @staticmethod
    def log(text):
        return xbmc.log(text)

    @staticmethod
    def getAddonFilePath(file='icon.png'):
        #return xbmc.translatePath(os.path.join( XBMCUtils.getAddonInfo('path'), file ))
        return xbmcvfs.translatePath(os.path.join( XBMCUtils.getAddonInfo('path'), file ))

    @staticmethod
    def getList(name, iconImage=None, thumbnailImage=None,fanArt=None, title = "title", category = "category", mediatype = "video"):
        #return xbmcgui.ListItem(name, iconImage=iconImage, thumbnailImage=thumbnailImage)
        li = xbmcgui.ListItem(label=name)
        li.setArt({"icon":iconImage, "thumb":thumbnailImage, "fanart": fanArt})
        li.setInfo('video', {'title': category, 'genre': category, 'mediatype': mediatype})
        return li

    @staticmethod
    def getSimpleList(name):
        return xbmcgui.ListItem(name)

    @staticmethod
    def addPlayableDirectory(handle,url,listitem):
        return xbmcplugin.addDirectoryItem(handle=int(handle),url=url,listitem=listitem,isFolder=False) #Playable

    @staticmethod
    def addDirectory(handle,url,listitem):
        return xbmcplugin.addDirectoryItem(handle=int(handle),url=url,listitem=listitem,isFolder=True) #Folder

    @staticmethod
    def getPlayer():
        return xbmc.Player(xbmc.PLAYER_CORE_AUTO)

    @staticmethod
    def play(url, listitem):
        player = XBMCUtils.getPlayer()
        if player.isPlaying() :
            player.stop()
        #xbmc.sleep(1000)
        player.showSubtitles(False)
        urlPlayer = urllib.unquote_plus(url.replace("+","@#@")).replace("@#@","+")
        urlPlayer = urllib.unquote_plus(url) ##THIS METHOD FAILS IN SOME CASES SHOWING A POPUP (server petition and ffmpeg internal problem)
        player.play(urlPlayer,listitem) ##THIS METHOD FAILS IN SOME CASES SHOWING A POPUP (server petition and ffmpeg internal problem)

    @staticmethod
    def resolveListItem(context,listitem):
        xbmcplugin.setResolvedUrl(int(context), True, listitem)

    @staticmethod
    def getDialogYesNo(title,text):
        return xbmcgui.Dialog().yesno(title,text, "", "", XBMCUtils.getString(11013), XBMCUtils.getString(11014) )

    @staticmethod
    def getOkDialog(title,text):
        return xbmcgui.Dialog().ok(title,text)

    @staticmethod
    def getNotification(title,text):
        xbmcgui.Dialog().notification(title,text)

    @staticmethod
    def setEndOfDirectory(context):
        xbmcplugin.endOfDirectory(int(context))

    @staticmethod
    def getKeyboard(text=''):
        return xbmc.Keyboard(text)
