# -*- encoding=utf-8 -*-


from dueros.Bot import Bot
from dueros.directive.Display.RenderTemplate import RenderTemplate
from dueros.directive.Display.template.ListTemplate import ListTemplateItem
from dueros.directive.Display.template.ListTemplate1 import ListTemplate1
from dueros.directive.Display.template.ListTemplate2 import ListTemplate2
from dueros.directive.Display.template.ListTemplate3 import ListTemplate3
from dueros.directive.VideoPlayer.VideoPlayer import VideoPlayer

from imomoe_client.main_page import ImomoeClientMainPage
from imomoe_client.japanese_anime_page import ImomoeClientJapaneseAnimePage
from imomoe_client.view_page import ImomoeClientViewPage
from imomoe_client.search_page import ImomoeClientSearchEngine


class ImomoeAnime(Bot):

    def __init__(self, request_data):

        super(ImomoeAnime, self).__init__(request_data)
        self.disable_verify_request_sign()

        self.add_launch_handler(self.launch_handler)
        self.add_intent_handler('search', self.search_intent_handler)

        self.add_intent_handler('previous', self.previous_intent_handlerr)
        self.add_intent_handler('next', self.next_intent_handler)
        self.add_intent_handler('choose_ep', self.choose_ep_intent_handler)

        self.add_intent_handler('play', self.play_intent_handler)
        self.add_intent_handler('stop', self.stop_intent_handler)
        self.add_intent_handler('pause', self.pause_intent_handler)
        self.add_intent_handler('resume', self.resume_intent_handler)

        self.add_intent_handler('fast_forward', self.fast_forward_intent_handler)
        self.add_intent_handler('rewind', self.rewind_intent_handler)
        self.add_intent_handler('jump_to', self.jump_to_intent_handler)

        self.add_intent_handler('list_choose', self.list_choose_intent_handler)

        self.add_intent_handler('back', self.back_intent_handler)

        self.search_engine = ImomoeClientSearchEngine()

    def load_main_page(self, template):

        """
        加载主页
        :param template: 被加载的模板
        :return:
        """
        token_count = 0

        main_page = ImomoeClientMainPage()

        # 加载热门番剧
        focus_list_template = ListTemplate3()
        focus_list_template.set_title("热门")

        focus_list = main_page.get_focus_list()
        for info in focus_list:
            Item = ListTemplateItem()
            Item.set_image(info["img"])
            Item.set_plain_primary_text(info["title"])
            Item.set_plain_secondary_text(info["info"])
            focus_list_template.add_item(Item)
        template.add_item(focus_list_template)

        # 加载最新番剧
        latest_list_template = ListTemplate3()
        latest_list_template.set_title("最新")

        latest_list = main_page.get_latest_list()
        for info in latest_list:
            Item = ListTemplateItem()
            Item.set_image(info["img"])
            Item.set_plain_primary_text(info["title"])
            Item.set_plain_secondary_text(info["info"])
            latest_list_template.add_item(Item)
        template.add_item(latest_list_template)

        # 加载日本番剧
        japanese_anime_list_template = ListTemplate3()
        japanese_anime_list_template.set_title("日漫")

        japanese_anime_list = main_page.get_japan_anime_list()
        for info in japanese_anime_list:
            Item = ListTemplateItem()
            Item.set_image(info["img"])
            Item.set_plain_primary_text(info["title"])
            Item.set_plain_secondary_text(info["info"])
            japanese_anime_list_template.add_item(Item)
        template.add_item(focus_list_template)

    def launch_handler(self):

        """
        处理-打开技能
        :return:
        """

        template = ListTemplate2()
        template.set_title('樱花动漫-首页')
        template.set_background_image("http://dbp-resource.cdn.bcebos.com/a3b2b130-c212-2241-294f-e13597c9dcc9/WeChat%20Image_20200508190042.jpg")

        self.load_main_page(template)

        directive = RenderTemplate(template)

        return {
            'directives': [directive],
            'outputSpeech': r'欢迎使用樱花动漫，在这里你可以找到各种你喜欢看的动漫哦~'
        }

    def search_intent_handler(self):

        """
        意图处理-搜索
        :return:
        """
        keyword = self.get_slots("keywords")
        if not keyword:
            self.ask("keywords")
            return {
                "outputSpeech": r"请问您要搜索什么？"
            }

        template = ListTemplate2()
        template.set_title("搜索-" + keyword)
        template.set_background_image("http://dbp-resource.cdn.bcebos.com/a3b2b130-c212-2241-294f-e13597c9dcc9/WeChat%20Image_20200508190042.jpg")

        search_result = self.search_engine.search(keyword)

        for info in search_result:
            item = ListTemplateItem()
            item.set_image(info["img"])
            item.set_plain_primary_text(info["title"])
            item.set_plain_secondary_text(info["info"])
            template.add_item(item)

        directive = RenderTemplate(template)

        return {
            "directives": [directive],
            "outputSpeech": r"为您找到如下结果"
        }

    def previous_intent_handlerr(self):
        
        """
        意图处理-上n集
        :return: 
        """
        
    def next_intent_handler(self):
        
        """
        意图处理-下n集
        :return: 
        """
        
    def choose_ep_intent_handler(self):
        
        """
        意图处理-选择集数
        :return: 
        """
        
    def play_intent_handler(self):

        """
        意图处理-播放
        :return:
        """

    def stop_intent_handler(self):

        """
        意图处理-退出播放
        :return:
        """

    def pause_intent_handler(self):

        """
        意图处理-暂停播放
        :return:
        """

    def resume_intent_handler(self):

        """
        意图处理-回复播放
        :return:
        """

    def fast_forward_intent_handler(self):

        """
        意图处理-快进
        :return:
        """

    def rewind_intent_handler(self):

        """
        意图处理-后退
        :return:
        """

    def jump_to_intent_handler(self):

        """
        意图处理-跳转到
        :return:
        """

    def list_choose_intent_handler(self):

        """
        意图处理-列表选择
        :return:
        """

    def back_intent_handler(self):

        """
        意图处理-返回
        :return:
        """
