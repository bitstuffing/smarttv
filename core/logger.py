import xbmcaddon
import logging as logger

IDADDON='com.github.bitstuffing.smarttv'
ROOT_DIR = xbmcaddon.Addon(id=IDADDON).getAddonInfo('path')

logger.basicConfig (
    format='%(asctime)s,%(msecs)d %(levelname)-s [%(filename)s:%(lineno)d] %(message)s - %(funcName)s()',
    datefmt='%Y-%m-%d:%H:%M:%S',
    filename=ROOT_DIR+"/debug.log",
    level=logger.DEBUG )
