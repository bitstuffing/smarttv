import re

try:
    import json
except:
    import simplejson as json

import random
import string
import urllib
import shutil
import zipfile
import os

from core.xbmcutils import XBMCUtils
from core.logger import logger

class Decoder():

    #START STRING UTILS

    @staticmethod
    def extract(fromString, toString, data):
        newData = data[data.find(fromString) + len(fromString):]
        newData = newData[0:newData.find(toString)]
        return newData

    @staticmethod
    def rExtract(fromString, toString, data):
        newData = data[0:data.rfind(toString)]
        newData = newData[newData.rfind(fromString) + len(fromString):]
        return newData

    @staticmethod
    def extractWithRegex(fromString, toString, data):
        newData = data[data.find(fromString):]
        newData = newData[0:newData.find(toString) + len(toString)]
        return newData

    @staticmethod
    def rExtractWithRegex(fromString, toString, data):
        newData = data[0:data.rfind(toString) + len(toString)]
        newData = newData[newData.rfind(fromString):]
        return newData

    #END STRING UTILS

    @staticmethod
    def applyFix(fileFix,removeFix,replaced=''):
        logger.debug("Applying fix...")
        ROOT_DIR = XBMCUtils.getAddonInfo('path')
        # Read in the file
        pythonScript = ROOT_DIR + fileFix
        with open(pythonScript, 'r') as file:
            filedata = file.read()

        # Replace the target string
        filedata = filedata.replace(removeFix, replaced)

        # Write the file out again
        with open(pythonScript, 'w') as file:
            file.write(filedata)

    @staticmethod
    def removeHTML(body):
        finalText = ""
        while "<script" in body:
            replaceBy = Decoder.extractWithRegex("<script", "</script>", body)
            # logger.debug("removing: "+replaceBy)
            body = body.replace(replaceBy, "")
        # logger.debug("scripts removed, now body is: "+body)
        while "<" in body and ">" in body:
            index = body.find("<")
            if index > 0:
                targetLine = body[:index]
                # logger.debug("INDEX: "+str(index)+", appending target line to removed html: " + targetLine)
                finalText += targetLine.strip()
                body = body[body.find(">") + 1:]
                if len(targetLine.strip()) > 0:
                    finalText += " "
            else:
                body = body[body.find(">") + 1:]
                # logger.debug("removed until '>' \n"+body)
        # body = body.strip()
        return finalText

    @staticmethod
    def randomString(length=12):
        """Generate a random string of fixed length """
        letters = string.ascii_lowercase
        return ''.join(random.choice(letters) for i in range(length))
