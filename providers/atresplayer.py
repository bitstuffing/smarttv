from core.logger import logger
from core.downloader import Downloader
from core.decoder import Decoder
import json
import random
import string

class Atresplayer(Downloader):

    API = "https://api.atresplayer.com/client/v1/"

    URL = "%sinfo/channels" % API
    CHANNELS = "%sinfo/categories/5a6b32667ed1a834493ec03b" % API
    DIRECTOS = "%srow/live" % API
    SCHEDULE = "https://www.atresplayer.com/programacion/"

    CHANNEL = "%srow/search?entityType=ATPFormat&sectionCategory=true&mainChannelId=%s&categoryId=%s&sortType=AZ&size=100&page=%s"
    EPISODE = "%sepisode/%s?NODRM=true"

    REGISTER = "https://account.atresplayer.com/user/v1/signup"

    HEADERS = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:104.0) Gecko/20100101 Firefox/104.0',
        'Origin':'https://www.atresplayer.com'
    }

    @staticmethod
    def register():

        output_string = ''.join(random.SystemRandom().choice(string.ascii_letters + string.digits) for _ in range(10))

        logger.debug(output_string)

        form = {
          "firstName": "%s" % output_string,
          "gender": "desconocido",
          "birthday": "1973",
          "email": "%s@gmail.com" % output_string,
          "password": "%s1" % output_string,
          "marketing": {
            "thirdParty": False,
            "shareData": False
          },
          "statusInfo": {
            "status": "ALTA"
          }
        }

        jsonContent = Atresplayer.getContentFromUrl(url=Atresplayer.REGISTER,data=bytes(json.dumps(form),'utf-8'),headers=Atresplayer.HEADERS,referer=Atresplayer.SCHEDULE)
        logger.debug(Atresplayer.cookie)
        logger.debug(jsonContent)


    @staticmethod
    def decoder(page):
        x = []
        logger.debug("decoding link %s"%page)

        newHeaders = Atresplayer.HEADERS

        try:
            jsonContent = Atresplayer.getContentFromUrl(url=page,headers=Atresplayer.HEADERS,referer=Atresplayer.SCHEDULE)
        except:
            logger.info('try 2... {"error":"required_registered","error_description":"Required registered uer)')
            #TODO: login if there are credentials
            Atresplayer.register()
            logger.debug("registered, trying cookies: %s..." % Atresplayer.cookie)
            jsonContent = Atresplayer.getContentFromUrl(url=page,headers=Atresplayer.HEADERS, cookie=Atresplayer.cookie,referer=Atresplayer.SCHEDULE)
            logger.debug(str(jsonContent))
            logger.info("endding try 2...")
            pass

        parsed = json.loads(jsonContent)
        logger.debug(str(parsed))
        if "sources" not in parsed:
            url = parsed["urlVideo"]
            logger.debug("decoding 1... %s" % url)
            try:
                jsonContent = Atresplayer.getContentFromUrl(url=url, headers=Atresplayer.HEADERS, referer=Atresplayer.SCHEDULE)
            except:
                logger.info('try 2.2... {"error":"required_registered","error_description":"Required registered uer)')
                #TODO: login if there are credentials
                Atresplayer.register()
                logger.debug("registered, trying cookies %s..." % Atresplayer.cookie)
                newHeaders = {
                    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:104.0) Gecko/20100101 Firefox/104.0',
                    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
                    'Accept-Language': 'en-US,en;q=0.5',
                    'Accept-Encoding': 'deflate, br',
                    'Alt-Used': 'api.atresplayer.com',
                    'Connection': 'keep-alive',
                    'Upgrade-Insecure-Requests': '1',
                    'Sec-Fetch-Dest': 'document',
                    'Sec-Fetch-Mode': 'navigate',
                    'Sec-Fetch-Site': 'none',
                    'Sec-Fetch-User': '?1',
                    'TE': 'trailers',
                    'Cookie' : Atresplayer.cookie
                }
                jsonContent = Atresplayer.getContentFromUrl(url=url, headers=newHeaders)
                logger.info("endding try 2.2...")
                pass
            parsed = json.loads(jsonContent)
        logger.debug("decoding 2... %s" % page)
        link = parsed["sources"][0]["src"]
        title = parsed["omniture"]["channel"]
        logger.debug("found link %s" % link)
        element = {}
        element["title"] = title
        element["link"] = link + "|Referer="+page+("&User-Agent=Mozilla/5.0 (X11; Linux x86_64; rv:45.0) Gecko/20100101 Firefox/104.0".replace(" ","+"))
        x.append(element)
        return x

    @staticmethod
    def getChannels(page):
        x = []
        if str(page) == '0':

            element = {}
            element["title"] = "Directo"
            element["link"] = "directo"
            x.append(element)

            jsonContent = Atresplayer.getContentFromUrl(url=Atresplayer.CHANNELS, headers=Atresplayer.HEADERS, referer=Atresplayer.SCHEDULE)
            parsed = json.loads(jsonContent)
            logger.info(parsed)
            for line in parsed:
                if "title" in line and "link" in line:
                    element = {}
                    element["title"] = line["title"]
                    element["link"] = line["link"]["href"]
                    x.append(element)

        elif 'directo' in str(page):
            jsonContent = Atresplayer.getContentFromUrl(url=Atresplayer.DIRECTOS, headers=Atresplayer.HEADERS, referer=Atresplayer.SCHEDULE)
            parsed = json.loads(jsonContent)
            for line in parsed["itemRows"]:
                element = {}
                element["title"] = line["link"]["url"]+" - "+line["title"]
                element["link"] = line["link"]["href"]
                element["finalLink"] = True
                x.append(element)
        else:
            x = []
            if 'ATPEpisode' not in page and '/format/' not in page and '?categoryId=' not in page:
                logger.debug("decoding...")
                x = Atresplayer.decoder(page)
            elif 'ATPEpisode' in page:
                #TODO -> more web browser for sub-sections
                jsonContent = Atresplayer.getContentFromUrl(url=page,headers=Atresplayer.HEADERS,referer=Atresplayer.SCHEDULE)
                parsed = json.loads(jsonContent)

                logger.debug(str(parsed))

                for item in parsed["itemRows"]:
                    element = {}
                    element["title"] = item["title"]
                    element["link"] = item["link"]["href"].replace("/client/","/player/").replace("/page/","/")
                    logger.debug(element["link"])
                    x.append(element)
            elif "/channel/" in page and "?categoryId=" in page:
                    logger.debug("not decoding...")
                    id = Decoder.extract('/channel/','?categoryId=',page)
                    category = page[page.find('?categoryId=')+len('?categoryId='):]
                    url = Atresplayer.CHANNEL % (Atresplayer.API, id, category, "0") #TODO, change page, now it's '0'
                    jsonContent = Atresplayer.getContentFromUrl(url=url,headers=Atresplayer.HEADERS,referer=Atresplayer.SCHEDULE)
                    parsed = json.loads(jsonContent)

                    logger.debug(str(parsed))

                    for item in parsed["itemRows"]:
                        element = {}
                        element["title"] = item["title"]
                        element["link"] = item["link"]["href"]
                        x.append(element)

                    #TODO -> put next with 'page=X+1'
            elif "/page/format/" in page:
                id = page[page.rfind("/")+1:]
                url = "%srow/search?entityType=ATPEpisode&formatId=%s&progress=true" % (Atresplayer.API, id)
                jsonContent = Atresplayer.getContentFromUrl(url=url,headers=Atresplayer.HEADERS,referer=Atresplayer.SCHEDULE)
                parsed = json.loads(jsonContent)

                logger.debug(str(parsed))
                if "itemRows" in parsed:
                    for item in parsed["itemRows"]:
                        element = {}
                        element["title"] = item["title"]
                        element["link"] = item["link"]["href"]
                        element["finalLink"] = True
                        x.append(element)
                else: #probably unique element
                    element = {}
                    element["title"] = item["title"]
                    element["link"] = item["href"]
                    element["finalLink"] = True
                    x.append(element)

            else:
                logger.debug("not decoding ELSE...")

        return x
