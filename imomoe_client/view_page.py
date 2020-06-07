# coding=utf-8
import requests
from bs4 import BeautifulSoup as bs


class ImomoeClientViewPage(object):

    def __init__(self):

        self.base_url = "http://imomoe.in"

    def load_view_page(self, url):

        """
        加载番剧详情页面信息
        :param url: 网址
        """
        r = requests.get(url)
        soup = bs(r.content.decode("gbk"), "lxml")
        all_div = soup.find_all("div")
        info_div = all_div[14]
        alex_div = info_div.find_all(attrs={"class": "alex"})[0]
        spay_div = info_div.find_all(attrs={"class": "spay"})[0]
        tpicl_div = info_div.find_all(attrs={"class": "tpic l"})[0]
        info_a = alex_div.select("a")
        info_list = {
            "title": spay_div.a["title"],
            "friendly_name": alex_div.p.string,
            "img": tpicl_div.img["src"],
            "desc": info_div.find_all(attrs={"class": "info"})[0].string,
            "area": info_a[0].string,
            "type": info_a[1].string,
            "year": info_a[2].string,
            "label": info_a[3].string,
            "index": info_a[4].string
        }

        play_div = info_div.find_all(attrs={"class": "movurl"})
        play_list = []
        for play_info in play_div:
            play_id = play_info["id"].replace("play_", "播放路线")
            play_li = play_info.select("li")
            a_list = []
            for i in play_li:
                a_list.append({"title": i.a["title"],
                               "href": self.base_url + i.a["href"]})
            play_list.append(a_list)

        return info_list, play_list
