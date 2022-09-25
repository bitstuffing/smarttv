import urllib
import urllib.parse
import sys,os
import platform

from core.xbmcutils import XBMCUtils
from core.logger import logger

def open(url,page,decode=True):
    logger.debug("launching playable url: "+url)
    play(url,page)

def play(url,page):
    listitem = XBMCUtils.getSimpleList(page)
    listitem.setProperty('IsPlayable','true')
    listitem.setPath(url)
    listitem.setInfo("video",page)
    try:
        #XBMCUtils.play(url,listitem)
        XBMCUtils.resolveListItem(sys.argv[1],listitem) ##FIX FOR PREVIEWS LINE##
        #xbmc.executebuiltin('Dialog.Close(all, true)') ## could be returned an empty element in a list, so player open the next and shows a invalid popup
    except:
        pass
        #print(traceback.format_exc())

def add_dir(name,url,mode,iconimage,provider,page="", thumbnailImage=''):
    type = "Video"
    u=sys.argv[0]+"?url="+urllib.parse.quote_plus(url)
    u+="&mode="+str(mode)+"&page="
    try:
        u+=urllib.parse.quote_plus(str(page))
    except:
        u+=page
        pass
    provider = str(provider)
    u+="&provider="+urllib.parse.quote_plus(provider)
    ok=True
    liz=XBMCUtils.getList(name, iconImage=iconimage, thumbnailImage=iconimage)
    liz.setInfo(type='Video', infoLabels={'Title': name+str(mode)})
    if mode == 2 or (mode >=100): #playable, not browser call, needs decoded to be playable or rtmp to be obtained
        liz.setProperty("IsPlayable", "true")
        liz.setPath(url)
        ok=XBMCUtils.addPlayableDirectory(handle=int(sys.argv[1]),url=u,listitem=liz) #Playable)
    else:
        liz.setProperty('Fanart_Image', thumbnailImage)
        ok=XBMCUtils.addDirectory(sys.argv[1],url=u,listitem=liz) #Folder

    return ok


def get_params():
    param={}
    paramstring=sys.argv[2]
    logger.info("paramString: %s " % paramstring)
    if len(paramstring)>=2:
        try:
            #now extract expected params, it has been changed because some params could be links
            #with other params and the previews method (split with '?' expr. doesn't work in some cases)
            logger.debug("filling params array with brute params... %s" % paramstring)

            params = paramstring[paramstring.find("?"):]
            for param in params.split("&"):
                par = param.split("=")
                if "mode" in par[0]:
                    mode = par[1]
                elif "url" in par[0]:
                    url = par[1]
                elif "page" in par[0]:
                    page = par[1]
                elif "provider" in par[0]:
                    provider = par[1]

            #finally put in param array
            logger.debug("done, filling params dic...")
            param={}
            param["mode"] = mode
            param["url"] = url
            param["page"] = page
            param["provider"] = provider
            logger.debug("done params built: %s " % str(param))
        except Exception as e:
            logger.error("ERROR: %s" % str(e))
            pass

    return param


def isAnException(url,page,provider,mode):
    state = False
    if mode == 4 and (provider=="bbccouk" and str(page) == '0' and ".xml" not in url) \
            or (str(page)=='1' and provider=='reuters')\
            or (str(page)!='0' and provider=='editioncnn'):
        logger.debug("Order don't reload page -> provider: "+provider)
        state = True
    if state:
        logger.debug("Dont reload view. Params -> page: "+page+", url: "+url+", provider: "+provider+", mode: "+str(mode))
    return state
