# coding=utf-8
import requests
from bs4 import BeautifulSoup as bs


class ImomoeClientMainPage(object):

    def __init__(self):

        self.base_url = "http://www.imomoe.in"
        r = requests.get(self.base_url)
        self.mp_html = r.content
        self.soup = bs(self.mp_html, "lxml")

        self.all_div = self.soup.find_all("div")
        self.focus_div = self.all_div[9]
        self.area_box_div = self.all_div[15]
        self.type_box_div = self.all_div[17]
        self.lang_box_div = self.all_div[18]
        self.latest_more_url = self.all_div[24].span.a["href"]
        self.latest_info_div = self.all_div[25]
        self.japan_more_url = self.all_div[27].span.a["href"]
        self.japan_info_div = self.all_div[28]
        self.chinese_more_url = self.all_div[30].span.a["href"]
        self.chinese_info_div = self.all_div[31]

    def get_focus_list(self):

        """
        获取热门番剧列表
        """
        focus = self.focus_div.select("li")
        focus_result = []
        for i in focus:
            result = {}
            result["title"] = i.a["title"]
            result["href"] = i.a["href"]
            result["img"] = i.img["src"]
            result["info"] = i.em.string
            focus_result.append(result)

        return focus_result

    def get_latest_list(self):

        """
        获取最新番剧列表
        """
        latest = self.latest_info_div.select("li")
        latest_result = []
        for i in latest:
            result = {}
            result["title"] = i.select("p")[0].a["title"]
            result["href"] = self.base_url + i.a["href"]
            result["img"] = i.img["src"]
            result["info"] = i.select("p")[1].string
            latest_result.append(result)

        return latest_result

    def get_japan_anime_list(self):

        """
        获取日本番剧列表
        """
        japan_anime = self.japan_info_div.select("li")
        japan_anime_result = []
        for i in japan_anime:
            result = {}
            result["title"] = i.select("p")[0].a["title"]
            result["href"] = self.base_url + i.a["href"]
            result["img"] = i.img["src"]
            result["info"] = i.select("p")[1].string
            japan_anime_result.append(result)

        return japan_anime_result

    def get_chinese_anime_list(self):

        """
        获取国产动漫列表
        """
        chinese_anime = self.chinese_info_div.select("li")
        chinese_anime_result = []
        for i in chinese_anime:
            result = {}
            result["title"] = i.select("p")[0].a["title"]
            result["href"] = self.base_url + i.a["href"]
            result["img"] = i.img["src"]
            result["info"] = i.select("p")[1].string
            chinese_anime_result.append(result)

        return chinese_anime_result

    def get_top_new_list(self):

        """
        获取最新更新的所有番剧
        """
        r = requests.get("http://www.imomoe.in/top/new.html")
        soup = bs(r.content, "lxml")
        topli_div = soup.find_all(attrs={"class": "topli"})[0]
        topli = topli_div.select("li")
        topli_result = []
        for i in topli:
            result = {}
            info = i.select("a")
            result["title"] = info[1]["title"]
            result["href"] = self.base_url + info[1]["href"]
            result["info"] = info[2].string
            result["time"] = i.em.string
            topli_result.append(result)

        return topli_result
