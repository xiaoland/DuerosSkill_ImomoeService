# import wx
from tkinter import *
from PIL import ImageTk
from PIL import Image
from io import BytesIO
import threading
import requests
from main_page import ImomoeClientMainPage
from japanese_anime_page import ImomoeClientJapaneseAnimePage
from view_page import ImomoeClientViewPage
from search_page import ImomoeClientSearchEngine
from player import ImomoeClientPlayer


class ImomoeClient(Tk):

    def __init__(self):

        super().__init__()
        self.title("ImomoeClient")
        self.geometry("1024x600")
        self.resizable(width=True, height=True)
        self.parent = self
        self._now_displaying_page = ""
        self.main_page = ImomoeClientMainPage()
        self.jp_page = ImomoeClientJapaneseAnimePage()
        self.view_page = ImomoeClientViewPage()
        self.search_page = ImomoeClientSearchEngine()

        # self.scrollbar = Scrollbar(self.parent)
        # self.scrollbar.pack(side=RIGHT, fill=Y)

        self.player_frame = Frame(self.parent)
        self.player_control_bar_frame = Frame(self.parent)
        self.player_canvas = Frame(self.parent, bg="black", width=1024, height=600)

        self.sidebar_frame = Frame(self.parent)
        self.load_sidebar()

        self.content_frame = Frame(self.parent)
        self.content_frame.pack(side=LEFT, padx=0, fill=BOTH)
        self.load_main_page()

    def load_sidebar(self):

        """
        加载侧边栏
        :return:
        """
        print("load_sidear")
        # home_bitmap = Image.open("./bitmap/home.png")
        # tv_bitmap = Image.open("./bitmap/tv.png")
        # search_bitmap = Image.open("./bitmap/search.png")
        # reload_bitmap = Image.open("./bitmap/reload.png")
        Button(self.sidebar_frame, text="Home", command=self.load_main_page).pack(side=TOP)
        Button(self.sidebar_frame, text="JaPage", command=self.load_jp_page).pack(side=TOP, pady=0)
        Button(self.sidebar_frame, text="Search", command=self.load_search_page).pack(side=TOP, pady=0)
        Button(self.sidebar_frame, text="Reload", command=self.reload_page).pack(side=TOP, pady=0)

        self.sidebar_frame.pack(side=LEFT)

    def load_main_page(self):

        """
        加载主页
        :return:
        """
        print("load_main_page")
        if self._now_displaying_page != "":
            self.content_frame.forget()
        self._now_displaying_page = "main"

        focus_panel = Frame(self.content_frame)
        latest_panel = Frame(self.content_frame)
        ja_panel = Frame(self.content_frame)
        ch_panel = Frame(self.content_frame)
        self.load_content_list(focus_panel, "热门番剧", self.main_page.get_focus_list(), 5, "main_page")
        self.load_content_list(latest_panel, "最新番剧", self.main_page.get_latest_list(), 5, "main_page")
        self.load_content_list(ja_panel, "日本番剧", self.main_page.get_japan_anime_list(), 5, "main_page")
        self.load_content_list(ch_panel, "国创番剧", self.main_page.get_chinese_anime_list(), 5, "main_page")
        focus_panel.pack(side=TOP)
        latest_panel.pack(side=TOP, pady=5)
        ja_panel.pack(side=TOP, pady=5)
        ch_panel.pack(side=TOP, pady=5)

    def load_jp_page(self):

        """
        加载日本动漫页面
        :return:
        """
        print("load_jp_page")
        self.content_frame.forget()
        self._now_displaying_page = "jp"

        focus_panel = Frame(self.content_frame)
        classic_panel = Frame(self.content_frame)
        movie_panel = Frame(self.content_frame)
        ova_panel = Frame(self.content_frame)
        self.load_content_list(focus_panel, "热门番剧", self.jp_page.get_focus_list(), 5, "japanese_anime_page")
        self.load_content_list(classic_panel, "经典番剧", self.jp_page.get_classic_list(), 5, "japanese_anime_page")
        self.load_content_list(movie_panel, "剧场版", self.jp_page.get_movie_list(), 5, "japanese_anime_page")
        self.load_content_list(ova_panel, "OVA版番剧", self.jp_page.get_ova_list(), 5, "japanese_anime_page")
        focus_panel.pack(side=TOP)
        classic_panel.pack(side=TOP, pady=5)
        movie_panel.pack(side=TOP, pady=5)
        ova_panel.pack(side=TOP, pady=5)

    def load_search_page(self):

        """
        加载搜索页面
        :return:
        """
        print("load_search_page")
        self.content_frame.forget()
        self._now_displaying_page = "search"

        search_panel = Frame(self.content_frame)
        search_panel.pack(side=TOP)

        search_image = Image.open("./bitmap/search.png")
        keyword_input = Entry(search_panel, width=918)
        keyword_input.pack(side=LEFT)
        Button(search_panel, image=ImageTk.PhotoImage(search_image), command=lambda : self.search_button_handler(keyword_input.get())).pack(side=LEFT, padx=10)

    def reload_page(self):

        """
        重载页面
        :return:
        """
        if self._now_displaying_page == "main":
            self.load_main_page()
        elif self._now_displaying_page == "jp":
            self.load_jp_page()
        elif self._now_displaying_page == "search":
            self.load_search_page()

    def search_button_handler(self, keyword):

        """
        进行搜索
        :return:
        """
        print("start_search")
        search_result = self.search_page.search(keyword)
        result_panel = Frame(self.content_frame)
        result_panel.pack(side=TOP, pady=5)

        for i in search_result:
            block_panel = Frame(result_panel)
            block_panel.pack(side=TOP, pady=5)
            img_type = i["img"].split(".")[-1]
            path = './search_page/' + "img." + img_type
            file = Image.open(BytesIO(requests.get(i["img"]).content))
            file.save(path)
            file.close()
            show_image = Image.open(path)
            Label(block_panel, image=ImageTk.PhotoImage(show_image)).pack(side=LEFT)
            desc_panel = Frame(block_panel) # 126 196
            desc_panel.pack(side=LEFT, padx=8)
            Label(desc_panel, text=i["title"]).pack(side=TOP)
            Label(desc_panel, text=i["info"]).pack(side=TOP, pady=2)
            Label(desc_panel, text=i["desc"]).pack(side=TOP, pady=2)
            Button(desc_panel, text="open", command=lambda: self.load_view_page(i["href"])).pack(side=TOP, pady=2)

    def load_content_list(self, frame, title, content_list, max_block, page_dir):

        """
        加载番剧面板
        :return:
        """
        print("    load_content: " + title)
        for_count = 1
        Label(frame, text=title).pack(side=TOP)
        display_frame = Frame(frame)
        display_frame.pack(side=TOP, pady=5)
        for i in content_list:
            if for_count > max_block:
                break
            img_type = i["img"].split(".")[-1]
            path = "./" + page_dir + "/" + str(for_count) + "." + img_type
            file = Image.open(BytesIO(requests.get(i["img"]).content))
            file.save(path)
            file.close()
            block_frame = Frame(display_frame)
            block_frame.pack(side=LEFT, padx=2)
            image = Image.open(path)
            Label(block_frame, image=ImageTk.PhotoImage(image), width=126, height=196).pack(side=TOP)
            Label(block_frame, text=i["title"]).pack(side=TOP, pady=2)
            Label(block_frame, text=i["info"]).pack(side=TOP, pady=1)
            Button(block_frame, text="open", command=lambda: self.load_view_page(i["href"])).pack(side=TOP, pady=0)
            for_count += 1

    def load_view_page(self, view_url):

        """
        加载番剧详情页面
        :param view_url:
        :return:
        """
        print("load_view_page: " + view_url)
        player = PlayerFrame(self.player_frame, self.player_control_bar_frame)
        info_list, play_list = self.view_page.load_view_page(view_url)
        self.content_frame.forget()

        desc_frame = Frame(self.content_frame)
        play_list_frame = Frame(self.content_frame)
        desc_frame.pack(side=TOP)
        play_list_frame.pack(side=TOP, pady=15)

        # 加载图片
        img_type = info_list["img"].split(".")[-1]
        path = './main_page/' + "img." + img_type
        file = Image.open(BytesIO(requests.get(info_list["img"]).content))
        file.save(path)
        file.close()
        desc_image = Image.open(path)
        Label(self.content_frame, image=ImageTk.PhotoImage(desc_image)).pack(side=LEFT)

        # 加载描述
        desc_panel = Frame(desc_frame).pack(side=LEFT, padx=5)
        yatl_text = "年份：" + info_list["year"] + " 地区：" + info_list["area"] + " 类型：" + info_list["type"] + " 标签：" + \
                    info_list["label"]
        Label(desc_panel, text=info_list["title"]).pack(side=TOP)
        Label(desc_panel, text="别名：" + info_list["friendly_name"]).pack(side=TOP, pady=2)
        Label(desc_panel, text=info_list["desc"]).pack(side=LEFT)
        Label(desc_panel, text=yatl_text).pack(side=LEFT)

        # 加载播放列表
        count = 1
        row = 0
        column = 0
        for i in play_list:
            Label(play_list_frame, text="播放线路_" + str(count)).pack(side=TOP)
            play_line_frame = Frame(play_list_frame).pack(side=TOP, padx=0)
            for ep in i:
                if column >= 5:
                    column = 0
                    row += 1
                Button(play_line_frame, text=ep["title"], command=lambda : player.play(ep["href"], ep["title"])).pack(side=LEFT, padx=2)
                column += 1
            count += 1


class PlayerFrame(object):

    def __init__(self, parent, control_bar_frame):

        self.parent = parent

        self.player = ImomoeClientPlayer()
        self._play_list = []
        self._title_list = []
        self._play_title = ""
        self._play_ep_id = 0
        self._play_line = 0
        self._play_speed = 1.0
        self._play_line_chose = []

        self.control_bar_frame = control_bar_frame
        self.create_control_bar()

    def create_control_bar(self):

        """
        创建操控板
        :return:
        """
        last_image = Image.open("./bitmap/last.png")
        pp_image = Image.open("./bitmap/play.png")
        next_image = Image.open("./bitmap/next.png")
        Button(self.control_bar_frame, text="Stop", command=lambda: self.player.stop(True)).pack(side=LEFT)
        Button(self.control_bar_frame, image=ImageTk.PhotoImage(last_image), command=self.last_ep).pack(side=LEFT, padx=5)
        Button(self.control_bar_frame, image=ImageTk.PhotoImage(pp_image), command=self.play_pause).pack(side=LEFT, padx=5)
        Button(self.control_bar_frame, image=ImageTk.PhotoImage(next_image), command=self.next_ep).pack(side=LEFT, padx=5)
        Button(self.control_bar_frame, text="Go back", command=self.control_bar_frame.destroy).pack(side=LEFT, padx=5)

    def create_video_view(self):

        """
        创建播放窗口
        :return:
        """
        self._canvas = Canvas(self.parent, bg="black", width=1024, height=600)
        self._canvas.pack()
        self.player.set_window(self._canvas.winfo_id())

    def get_player_info(self):

        """
        获取播放器信息
        :return:
        """
        info = self.player.get_player_info()
        self._play_list = self.player.get_play_list()
        self._play_line_chose = range(0, len(self._play_list))
        self._play_ep_id = info["ep_id"]
        self._play_line = info["play_line"]
        self._play_title = info["title"]
        self._play_speed = info["play_speed"]

    def load_play_list(self, play_list):

        """
        加载播放列表
        :param play_list:
        :return:
        """
        self.player.load_play_list(play_list)

    def play(self, url=None, title=None):

        """
        开始播放
        :param url: 如果未指定url，则从播放列表中播放
        :param title: 视频标题，只有url指定时生效
        :return:
        """
        self.control_bar_frame.pack()
        self.create_video_view()
        self.get_player_info()
        if url is None:
            self.player.play()
        else:
            self._play_title = title
            self.player.play(url)

    def play_pause(self):

        """
        按钮响应-播放/暂停
        :return:
        """
        if self.player.get_playing_state() == 0:
            self.player.pause()
        elif self.player.get_playing_state() == 1:
            self.player.resume()
        else:
            self.play()

    def next_ep(self):

        """
        按钮响应-下一集
        :return:
        """
        self.player.next_ep()

    def last_ep(self):

        """
        按钮响应-上一集
        :return:
        """
        self.player.last_ep()


if __name__ == "__main__":

    app = ImomoeClient()
    app.mainloop()
