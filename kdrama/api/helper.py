from requests import get
from bs4 import BeautifulSoup
from urllib.parse import urlparse, parse_qs, urljoin
import aiohttp
import asyncio
from json import loads


class HttpRequest:

    def __init__(self, url, headers={}, params=""):
        self.url = url
        self.headers = headers
        self.params = params
        self.res = ""

    async def request(self, type):
        async with aiohttp.ClientSession() as session:
            async with session.get(self.url, headers=self.headers) as res:
                res = getattr(res, type)
                self.res = await self.response(res)
                return self.res

    async def response(self, res):
        if callable(res):
            return await res()
        return res

    async def HtmlParser(self, html):
        return BeautifulSoup(html, "html.parser")

    async def parse(self, type):
        response = await self.request(type)
        html = await self.HtmlParser(response)
        return html


class BaseDrama(HttpRequest):
    def __init__(self, url, headers={}, params=""):
        super().__init__(url, headers, params)

    def search(keyword):
        pass

    async def get_episodes(self):
        baseurl = "https://vidcloud9.com"
        episodes = []
        html = await super().parse("text")
        for li in html.find_all("ul", class_="listing items lists"):
            for a in li.find_all("a"):
                link = urljoin(baseurl, a.get('href'))
                episodes.append(link)
        return episodes

    async def get_episode(self, url):
        self.url = url
        response = await super().parse("text")
        for element in response.find_all("iframe"):
            parsed = urlparse(element.get("src"))
            id = parse_qs(parsed.query).get("id")
            title = parse_qs(parsed.query).get("title")
            return id[0], title[0]


class VideCloud(BaseDrama):

    async def get_video(self, id):
        self.url = f"https://vidnext.net/ajax.php?id={id}".format(id=id)
        return await super().request("json")


class GoPlay(BaseDrama):
    async def get_video(self, id):
        self.url = f"https://gogo-play.net/ajax.php?id={id}".format(id=id)
        return await super().request("json")


class DramaCool(BaseDrama):

    async def search(self, name):
        self.url = f"https://dramacool.vc/search?keyword={name}"
        dramas = await super().request("json")
        for drama in dramas:
            popKeys = ["alias", "cover", "status"]
            for key in popKeys:
                del drama[key]
        return dramas

    async def get_episodes(self):
        baseurl = "https://dramacool.vc"
        episodes = []
        html = await super().parse("text")
        for url in html.find_all("a", class_="img"):
            link = urljoin(baseurl, url.get('href'))
            if link.endswith(".html"):
                episodes.append(link)
        return episodes

    async def get_video(self, episode):
        id, title = episode
        self.url = f"https://embed.dramacool.vc/ajax.php?id={id}".format(id=id)
        return await super().request("text"), id, title


class Drama:
    def __init__(self, url, headers):
        self.url = url
        self.headers = headers

    def get_type(self):
        domain = urlparse(self.url).netloc
        if domain == "dramacool.ch":
            return "DramaCool"
        if domain == "gogo-stream.com":
            return "GoPlay"
        if domain == "vidcloud9.com":
            return "VideCloud"
        return None

    def create_obj(self, class_):
        obj = globals()[class_](self.url, headers=self.headers)
        return obj

    async def main(self):
        loop = asyncio.get_event_loop()
        class_ = self.get_type()
        drama = self.create_obj(class_)
        urls = await drama.get_episodes()
        tasks = [asyncio.ensure_future(
            drama.get_episode(url)) for url in urls]
        episode_id_list = await asyncio.gather(*tasks)
        episodes_detail = [asyncio.ensure_future(drama.get_video(episode))
                           for episode in episode_id_list]
        episodes_detail = await asyncio.gather(*episodes_detail)
        data = []
        link = {}
        for episode in episodes_detail:
            media, id, title = episode
            media = loads(media)
            video = media["source"][0]["file"]
            data.append((video, id, title))
        return data

    def run(self):
        return asyncio.run(self.main())
