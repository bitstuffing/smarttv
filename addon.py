import xbmcaddon
import xbmcgui
import urllib, urllib.parse

from core.utils import * #drawers
from providers.atresplayer import Atresplayer

addon       = xbmcaddon.Addon()
addonname   = addon.getAddonInfo('name')
ICON = XBMCUtils.getAddonFilePath('logo.jpg')


# Set a string variable to use
line1 = "Welcome!\nDev. rev."

# Launch a dialog box in kodi showing the string variable 'line1' as the contents
xbmcgui.Dialog().ok(addonname, line1)


def browse_channels(url,page): #BROWSES ALL PROVIDERS (it has been re-sorted)
    if "atresplayer" in url:
        drawAtresplayer(page)
    else: # main menu
        add_dir("Atresplayer.com", 'atresplayer', 4,"https://statics.atresmedia.com/atresplayer/assets/web/icon-192x192.png",'atresplayer', 0)

def browse_channel(url,page,provider): #MAIN TREE BROWSER IS HERE!
    if provider == 'atresplayer':
        drawAtresplayer(page)

    logger.info(provider)


def drawAtresplayer(url):
    logger.info("drawAtresplayer init...")
    channels = Atresplayer.getChannels(url)
    logger.debug("items obtained: " + str(len(channels)))
    for channel in channels:
        level = 4
        if "finalLink" in channel:
            level = 101  # stream
        img = ''
        if "thumbnail" in channel:
            img = channel["thumbnail"]
        add_dir(channel["title"], channel["link"], level, img, "atresplayer", channel["link"])

def openAtresplayer(url,page):
    logger.info("decoding atresplayer link... " + url)
    link = Atresplayer.getChannels(url)[0]["link"].strip()
    logger.info("decoded atresplayer link: " + link)
    play(link, page)

def init():
    params=get_params()

    url=""
    mode=None
    page=""
    provider = ""

    try:
        page=urllib.parse.unquote_plus(params["page"])
    except:
        pass
    try:
        url=urllib.parse.unquote_plus(params["url"])
    except:
        pass
    try:
        mode=int(params["mode"])
    except:
        pass
    try:
        provider=urllib.parse.unquote_plus(params["provider"])
    except:
        pass

    logger.debug("Mode: %s " % str(mode))
    logger.debug("URL: %s " % str(url))
    logger.debug("Page: %s " % str(page))
    logger.debug("Provider: %s " % str(provider))

    try:
        if mode==None: #init
            browse_channels(url,page)
        elif mode == 2: #open video in player
            play(url,page)
        elif mode == 3:
            browse_channels(url,page)
        elif mode == 4:
            browse_channel(url,page,provider)
        elif mode == 101:
            openAtresplayer(url,page)
        else:
            pass

    except Exception as e:
        logger.error(XBMCUtils.getString(10009)+", "+str(e))
        XBMCUtils.getNotification("Error",XBMCUtils.getString(10009))
        pass

    if not isAnException(url,page,provider,mode):
        logger.debug("End of main menu to be displayed. Params -> page: "+page+", url: "+url+", provider: "+provider+", mode: "+str(mode))
        XBMCUtils.setEndOfDirectory(int(sys.argv[1]))


init()
