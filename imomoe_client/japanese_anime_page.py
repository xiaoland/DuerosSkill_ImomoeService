# coding=utf-8
import requests
from bs4 import BeautifulSoup as bs


class ImomoeClientJapaneseAnimePage(object):

    def __init__(self):

        self.base_url = "http://www.imomoe.in"
        r = requests.get(self.base_url + "/list/2.html")
        self.jp_html = r.content
        self.soup = bs(self.jp_html, "lxml")

        self.all_div = self.soup.find_all("div")
        self.focus_div = self.all_div[13]
        self.classic_div = self.all_div[22]
        self.movie_div = self.all_div[24]
        self.ova_div = self.all_div[25]

    def get_focus_list(self):

        """
        获取热门日本番剧列表
        """
        focus = self.focus_div.select("li")
        focus_result = []
        for i in focus:
            result = {}
            result["title"] = i.p.a["title"]
            result["href"] = self.base_url + i.p.a["href"]
            result["img"] = i.img["src"]
            result["info"] = i.select("p")[1].string
            focus_result.append(result)

        return focus_result

    def get_classic_list(self):

        """
        获取经典日本番剧列表
        """
        classic = self.classic_div.select("li")
        classic_result = []
        for i in classic:
            result = {}
            result["title"] = i.p.a["title"]
            result["href"] = self.base_url + i.p.a["href"]
            result["img"] = i.img["src"]
            classic_result.append(result)

        return classic_result

    def get_movie_list(self):

        """
        获取日本剧场版动漫列表
        """
        movie = self.movie_div.select("li")
        movie_result = []
        for i in movie:
            result = {}
            result["title"] = i.p.a["title"]
            result["href"] = self.base_url + i.p.a["href"]
            result["img"] = i.img["src"]
            movie_result.append(result)

        return movie_result

    def get_ova_list(self):

        """
        获取日本OVA版动漫列表
        """
        ova = self.ova_div.select("li")
        ova_result = []
        for i in ova:
            result = {}
            result["title"] = i.p.a["title"]
            result["href"] = self.base_url + i.p.a["href"]
            result["img"] = i.img["src"]
            ova_result.append(result)

        return ova_result
