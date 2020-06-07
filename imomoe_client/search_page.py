# coding=utf-8
import json
import urllib
import requests
from bs4 import BeautifulSoup as bs


class ImomoeClientSearchEngine(object):

    def __init__(self):

        self.base_url = "http://www.imomoe.in"

    def search(self, keyword):

        """
        搜索
        :param keyword:
        :return:
        """
        r = requests.post(self.base_url + "/search.asp",
                          data=json.dumps({"searchword": keyword}))
        soup = bs(r.content, "lxml")
        keyword = urllib.urlencode(keyword.encode("gbk"))
        r = requests.get("http://www.imomoe.in/search.asp" + "?searchword=" + keyword)
        soup = bs(r.content.decode("gbk"), "lxml")
        all_div = soup.select("div")
        search_result_div = all_div[14]
        search_result = search_result_div.select("li")
        search_result_after = []
        for i in search_result:
            result = {}
            result["title"] = i.h2.a["title"]
            result["href"] = self.base_url + i.h2.a["href"]
            result["desc"] = i.p.string
            result["info"] = i.select("span")[1].string
            search_result_after.append(result)

        return search_result_after
