#!/usr/bin/env python2
# -*- encoding=utf-8 -*-

import random
import threading
from dueros.Bot import Bot
from dueros.directive.Display.RenderTemplate import RenderTemplate
from dueros.directive.Display.template.ListTemplate1 import ListTemplate1
from dueros.directive.Display.template.ListTemplateItem import ListTemplateItem
from dueros.directive.Display.template.BodyTemplate3 import BodyTemplate3
from dueros.directive.Display.Hint import Hint
from dueros.samples.jisuan.MemberBiz import MemberBiz

class JiSuanBot(Bot):

    def __init__(self, request_data):
        super(JiSuanBot, self).__init__(request_data)
        self.add_launch_handler(self.launch_request)
        self.add_intent_handler('com.jack.dbp.calculate.type', self.selectRangeAndType)
        self.add_intent_handler('com.jack.dbp.calculate.result', self.result)

    def get_member_biz(self):
        return MemberBiz()

    def launch_request(self):
        self.wait_answer()
        device_id = self.request.get_device_id()
        self.get_member_biz().add_member(device_id)
        self.set_session_attribute('right', 0, 0)
        template = self.__get_home_card()
        speech = '欢迎使用趣味计算,您可以对我说:"帮助" 来获取帮助信息,对我说"退出" 关闭技能,请告诉我要做多少以内的加法或减法'
        reprompt = '趣味计算没有听懂，可以直接对我说帮助'
        hint1 = Hint('做10以内的加法')
        return {
            'outputSpeech': speech,
            'reprompt': reprompt,
            'directives': [hint1, template]
        }

    def __get_home_card(self):

        token = {'page': 'home'}
        body_template = BodyTemplate3()
        body_template.set_title('趣味计算')
        body_template.set_image(
            'http://dbp-resource.gz.bcebos.com/d78d043c-89d1-dfbb-fb48-482829cad05d/quweijisuan.png?authorization=bce-auth-v1%2Fa4d81bbd930c41e6857b989362415714%2F2018-06-23T07%3A18%3A48Z%2F-1%2F%2F77ebff2dd618080c880d6dfe15ebb0154a116a1e3ff83947e22b27e468540a46')
        body_template.set_token(self.get_token(token))
        body_template.set_background_image(BG2)
        body_template.set_plain_content('欢迎使用趣味计算,您可以对我说:"帮助",获取帮助信息,对我说"退出",关闭技能')
        directive = RenderTemplate(body_template)
        return directive

    def selectRangeAndType(self):
        self.wait_answer()
        _range = self.get_slots('range')
        ctype = self.get_slots('type')
        if not _range:
            self.ask('range')
            return {
                'outputSpeech': '请您告诉我要做什么范围的呢',
                'reprompt': '趣味计算没有听懂，可以直接对我说帮助'
            }

        if not ctype:
            self.ask('type')
            return {
                'outputSpeech': '请您告诉我要做加法还是减法呢',
                'reprompt': '趣味计算没有听懂，可以直接对我说帮助'
            }

        if _range and ctype:
            self.set_session_attribute('range', _range, 10)
            self.set_session_attribute('type', ctype, '加法')
            return self.__generateSubject(int(_range), ctype)

    def result(self):
        self.wait_answer()
        result = self.get_slots('result')
        if result:
            rightResult = self.get_session_attribute('result', 0)
            rightIndex = self.get_session_attribute('index', 0)
            if int(result) == int(rightResult):
                right = int(self.get_session_attribute('right', 0))
                self.set_session_attribute('right', (right + 1), 0)
                self.increase_score_by_thread()
                return self.__nexted('恭喜你，答对了。请听下一题。')
            else:
                return {
                    'outputSpeech': '答错了,再想想哦，或者对我说：跳过, 继续回答下一题',
                    'reprompt': '答错了,再想想哦'
                }

    def increase_score_by_thread(self):
        thread = threading.Thread(target=self.__increase_score_device_id)
        thread.start()

    def __increase_score_device_id(self):
        device_id = self.request.get_device_id()
        biz = self.get_member_biz()
        biz.incr_member_score(device_id)

    def nexted(self, notify=''):
        self.wait_answer()
        _range = self.get_slots('range')
        type = self.get_slots('type')
        return self.__generateSubject(int(_range), type, notify)

    def __nexted(self, notify=''):
        self.wait_answer()
        _range = self.get_session_attribute('range', 10)
        type = self.get_session_attribute('type', '加法')
        return self.__generateSubject(int(_range), type, notify)


    def __generateSubject(self, _range, ctype, notify=''):

        if ctype == '加法':
            one = int(random.random() * _range + 1)
            two = int(random.random() * (_range - one))
            result = one + two
            return self.__common(one, two, result, ctype, _range, notify)

        elif ctype == '减法':
            one = int(random.random() * _range + 1)
            two = int(random.random() * _range + 1)
            func = lambda one, two: one - two if one > two else two - one
            result = func(one, two)
            return self.__common(one, two, result, ctype, _range, notify)

    def __common(self, one, two, result, cType, cRange, notify=''):

        listTemplate2 = ListTemplate1()
        listTemplate2.set_background_image(BG2)
        resultIndex = random.randint(1, 3)
        random1 = int(random.random() * cRange)
        while random1 == result:
            random1 = int(random.random() * cRange)

        random2 = int(random.random() * cRange)
        while random2 == random1 or random2 == result:
            random2 = int(random.random() * cRange)

        return self.__baseCommon(one, two, result, resultIndex, random1, random2, cType, cRange, listTemplate2, notify)

    def __baseCommon(self, one, two, result, resultIndex, random1, random2, cType, cRange, listTemplate2, notify=''):

        item1 = ListTemplateItem()
        item1.set_plain_primary_text('等于%s吗' % random1)
        item1.set_image(nums[random1])

        item2 = ListTemplateItem()
        item2.set_plain_primary_text('等于%s吗' % random2)
        item2.set_image(nums[random2])

        item3 = ListTemplateItem()
        item3.set_plain_primary_text('等于%s吗' % result)
        item3.set_image(nums[result])

        self.set_session_attribute('one', one, 0)
        self.set_session_attribute('two', two, 0)
        self.set_session_attribute('result', result, result)
        self.set_session_attribute('index', resultIndex, resultIndex)
        self.set_session_attribute('random1', random1, 0)
        self.set_session_attribute('random2', random2, 0)
        self.set_session_attribute('type', cType, '加法')
        self.set_session_attribute('range', cRange, 10)

        if resultIndex == 1:
            item3.set_token('1')
            item1.set_token('2')
            item2.set_token('3')
            listTemplate2.add_item(item3)
            listTemplate2.add_item(item1)
            listTemplate2.add_item(item2)
        elif resultIndex == 2:
            item1.set_token('1')
            item3.set_token('2')
            item2.set_token('3')
            listTemplate2.add_item(item1)
            listTemplate2.add_item(item3)
            listTemplate2.add_item(item2)
        elif resultIndex == 3:
            item1.set_token('1')
            item2.set_token('2')
            item3.set_token('3')
            listTemplate2.add_item(item1)
            listTemplate2.add_item(item2)
            listTemplate2.add_item(item3)

        if cType == '加法':
            listTemplate2.set_title('%s + %s = ?' % (one, two))
            self.set_session_attribute('speech',
                                     '<speak><say-as type="number:ordinal">%s</say-as> 加 <say-as type="number:ordinal">%s</say-as> 等于多少呢</speak>' % (
                                         one, two), '')

            if notify:
                speech = '<speak>%s<say-as type="number:ordinal">%s</say-as> 加 <say-as type="number:ordinal">%s</say-as> 等于多少呢</speak>' % (
                    notify, one, two)
            else:
                speech = '<speak><say-as type="number:ordinal">%s</say-as> 加 <say-as type="number:ordinal">%s</say-as> 等于多少呢</speak>' % (
                    one, two)
        elif cType == '减法':
            if one >= two:
                tuples = (one, two)
            else:
                tuples = (two, one)

            listTemplate2.set_title('%s - %s = ?' % tuples)
            if notify:
                speech = '<speak>%s<say-as type="number:ordinal">%s</say-as> 减 <say-as type="number:ordinal">%s</say-as> 等于多少呢</speak>' % (
                    notify, tuples[0], tuples[1])
            else:
                speech = '<speak><say-as type="number:ordinal">%s</say-as> 减 <say-as type="number:ordinal">%s</say-as> 等于多少呢</speak>' % tuples
            self.set_session_attribute('speech', speech, '')
        template = RenderTemplate(listTemplate2)
        reprompt = '趣味计算没有听懂，可以直接对我说帮助'
        hint = Hint(['第x个或我说等于x', '做10以内的减法'])
        return {
            'outputSpeech': speech,
            'reprompt': reprompt,
            'directives': [hint, template]
        }


BG2 = 'http://dbp-resource.gz.bcebos.com/51952f2a-c778-7440-cf78-8146b2001f81/bg.png?authorization=bce-auth-v1%2Fa4d81bbd930c41e6857b989362415714%2F2018-06-15T02%3A06%3A20Z%2F-1%2F%2F78a349b765569d51de037bf890108f854736c45ab90301e2072918b77fdfa6cd'
nums=[
        'http://dbp-resource.gz.bcebos.com/51952f2a-c778-7440-cf78-8146b2001f81/0.png?authorization=bce-auth-v1%2Fa4d81bbd930c41e6857b989362415714%2F2018-06-15T02%3A03%3A54Z%2F-1%2F%2F1105bb8fe1d043f710c2e67940c9d75ad3dee7be25f2441ca6f4554cef68d5f8',
        'http://dbp-resource.gz.bcebos.com/51952f2a-c778-7440-cf78-8146b2001f81/1.png?authorization=bce-auth-v1%2Fa4d81bbd930c41e6857b989362415714%2F2018-06-15T02%3A04%3A00Z%2F-1%2F%2F346a6edc4c57fcb1a074bbec69acae08e4c175dd278a3b418128a84b14b0ac27',
        'http://dbp-resource.gz.bcebos.com/51952f2a-c778-7440-cf78-8146b2001f81/2.png?authorization=bce-auth-v1%2Fa4d81bbd930c41e6857b989362415714%2F2018-06-15T02%3A04%3A07Z%2F-1%2F%2F361f8d8bf94dcae81c6a0822797c8488c1c86ee08803210937249773d8e69962',
        'http://dbp-resource.gz.bcebos.com/51952f2a-c778-7440-cf78-8146b2001f81/3.png?authorization=bce-auth-v1%2Fa4d81bbd930c41e6857b989362415714%2F2018-06-15T02%3A04%3A27Z%2F-1%2F%2F0ff598a6bd85612b6100f7ba3c127e15f41dc9c2a4d0ca1220da3cf51d02d654',
        'http://dbp-resource.gz.bcebos.com/51952f2a-c778-7440-cf78-8146b2001f81/4.png?authorization=bce-auth-v1%2Fa4d81bbd930c41e6857b989362415714%2F2018-06-15T02%3A04%3A27Z%2F-1%2F%2Fa2d3fede51e02ed7ead0f765cac61fd96355a882b797e65f3db8af0c2a8b2069',
        'http://dbp-resource.gz.bcebos.com/51952f2a-c778-7440-cf78-8146b2001f81/5.png?authorization=bce-auth-v1%2Fa4d81bbd930c41e6857b989362415714%2F2018-06-15T02%3A04%3A27Z%2F-1%2F%2Fd634fb287b471d0090c84afee495acca3c495f5302dadd95a071ea8bd4fc020d',
        'http://dbp-resource.gz.bcebos.com/51952f2a-c778-7440-cf78-8146b2001f81/6.png?authorization=bce-auth-v1%2Fa4d81bbd930c41e6857b989362415714%2F2018-06-15T02%3A04%3A28Z%2F-1%2F%2Fffdd150a4384dfb00350f5c4444ee166df5f8314cffe547dbcf91f82a3aa69be',
        'http://dbp-resource.gz.bcebos.com/51952f2a-c778-7440-cf78-8146b2001f81/7.png?authorization=bce-auth-v1%2Fa4d81bbd930c41e6857b989362415714%2F2018-06-15T02%3A04%3A28Z%2F-1%2F%2Fafe10e21050472700bffc6b0466200d87ab254b902c6e219ec0c419b2cfb2d24',
        'http://dbp-resource.gz.bcebos.com/51952f2a-c778-7440-cf78-8146b2001f81/8.png?authorization=bce-auth-v1%2Fa4d81bbd930c41e6857b989362415714%2F2018-06-15T02%3A04%3A28Z%2F-1%2F%2F3c98784c2c5cbdf75c7e0d0af973cb6b57780fa6345bc9e2828b3416c4486227',
        'http://dbp-resource.gz.bcebos.com/51952f2a-c778-7440-cf78-8146b2001f81/9.png?authorization=bce-auth-v1%2Fa4d81bbd930c41e6857b989362415714%2F2018-06-15T02%3A04%3A28Z%2F-1%2F%2Fdfbdb4eb211d9e2642df80166ed13468a32e35531c0aa97c8bfcc43231519cec',
        'http://dbp-resource.gz.bcebos.com/51952f2a-c778-7440-cf78-8146b2001f81/10.png?authorization=bce-auth-v1%2Fa4d81bbd930c41e6857b989362415714%2F2018-06-15T02%3A04%3A28Z%2F-1%2F%2Fc80ee5bca524986b307d7b6c082f0c016c2cef3566262ca03df0a1ccefa48284',
        'http://dbp-resource.gz.bcebos.com/51952f2a-c778-7440-cf78-8146b2001f81/11.png?authorization=bce-auth-v1%2Fa4d81bbd930c41e6857b989362415714%2F2018-06-15T02%3A04%3A28Z%2F-1%2F%2F4927e061742ced2dc2c15a8b1fb7f83414a9c3a126197b1dadb4aa604a744d7c',
        'http://dbp-resource.gz.bcebos.com/51952f2a-c778-7440-cf78-8146b2001f81/12.png?authorization=bce-auth-v1%2Fa4d81bbd930c41e6857b989362415714%2F2018-06-15T02%3A04%3A29Z%2F-1%2F%2Fe926d87d3de467ac25bec3b3b376e790d349c2bd3b0742ef9593d99d267bc0e7',
        'http://dbp-resource.gz.bcebos.com/51952f2a-c778-7440-cf78-8146b2001f81/13.png?authorization=bce-auth-v1%2Fa4d81bbd930c41e6857b989362415714%2F2018-06-15T02%3A04%3A29Z%2F-1%2F%2F9f779b1cc209fa651e1c65602b2b475d8e8c75d6f55e369898514506d0fc0740',
        'http://dbp-resource.gz.bcebos.com/51952f2a-c778-7440-cf78-8146b2001f81/14.png?authorization=bce-auth-v1%2Fa4d81bbd930c41e6857b989362415714%2F2018-06-15T02%3A04%3A29Z%2F-1%2F%2F9cf84432da7459169ae27b929702c0d7a0cca9fac096e5e6a196e3038f195970',
        'http://dbp-resource.gz.bcebos.com/51952f2a-c778-7440-cf78-8146b2001f81/15.png?authorization=bce-auth-v1%2Fa4d81bbd930c41e6857b989362415714%2F2018-06-15T02%3A04%3A29Z%2F-1%2F%2F8e3dbd96cb03612abf521ba24ac2505f3cc5ea7ab9349e22d4c228da5a3388bd',
        'http://dbp-resource.gz.bcebos.com/51952f2a-c778-7440-cf78-8146b2001f81/16.png?authorization=bce-auth-v1%2Fa4d81bbd930c41e6857b989362415714%2F2018-06-15T02%3A04%3A29Z%2F-1%2F%2Fb6f0d8d25d35dda7b956cfb4db5a67cabc20cd3ab308e57a4052c7c4764c5718',
        'http://dbp-resource.gz.bcebos.com/51952f2a-c778-7440-cf78-8146b2001f81/17.png?authorization=bce-auth-v1%2Fa4d81bbd930c41e6857b989362415714%2F2018-06-15T02%3A04%3A30Z%2F-1%2F%2F3fd55be052d3db044bfe5715f0e3e3f5212f7876d6df531b9492fcb2194cbada',
        'http://dbp-resource.gz.bcebos.com/51952f2a-c778-7440-cf78-8146b2001f81/18.png?authorization=bce-auth-v1%2Fa4d81bbd930c41e6857b989362415714%2F2018-06-15T02%3A04%3A30Z%2F-1%2F%2Fc8d50f9832b6c39306afeb181c6bc8a3cedbc4e71fba946e27e8cd496480a446',
        'http://dbp-resource.gz.bcebos.com/51952f2a-c778-7440-cf78-8146b2001f81/19.png?authorization=bce-auth-v1%2Fa4d81bbd930c41e6857b989362415714%2F2018-06-15T02%3A04%3A30Z%2F-1%2F%2Fc9ce2617a0940023e3f4327c82a3a99244b84e620ecc5112bae8aca7696ec332',
        'http://dbp-resource.gz.bcebos.com/51952f2a-c778-7440-cf78-8146b2001f81/20.png?authorization=bce-auth-v1%2Fa4d81bbd930c41e6857b989362415714%2F2018-06-15T02%3A04%3A30Z%2F-1%2F%2F2c4c5b5cb0d584c5b2a3df6cbaa8e931b0e6b0ab80caa9ebf0e6e658dde3861b',
        'http://dbp-resource.gz.bcebos.com/51952f2a-c778-7440-cf78-8146b2001f81/21.png?authorization=bce-auth-v1%2Fa4d81bbd930c41e6857b989362415714%2F2018-06-15T02%3A04%3A30Z%2F-1%2F%2Fc82b03659d58dfc9fafb83dd59e7cc4c8579ccfb7df1f810cc11b410c47ae2f0',
        'http://dbp-resource.gz.bcebos.com/51952f2a-c778-7440-cf78-8146b2001f81/22.png?authorization=bce-auth-v1%2Fa4d81bbd930c41e6857b989362415714%2F2018-06-15T02%3A04%3A30Z%2F-1%2F%2F35384bcee33fe55de35ad7bc95aa21bbfeeb9aa3833d4bda07306af906a0f5a1',
        'http://dbp-resource.gz.bcebos.com/51952f2a-c778-7440-cf78-8146b2001f81/23.png?authorization=bce-auth-v1%2Fa4d81bbd930c41e6857b989362415714%2F2018-06-15T02%3A04%3A31Z%2F-1%2F%2F292ee52922326ba93786dcfba66a73fedc3e2da74fc2dda6d91c292a4f2e4e84',
        'http://dbp-resource.gz.bcebos.com/51952f2a-c778-7440-cf78-8146b2001f81/24.png?authorization=bce-auth-v1%2Fa4d81bbd930c41e6857b989362415714%2F2018-06-15T02%3A04%3A31Z%2F-1%2F%2F8e63158eeece40ce327bd9e36b92a346a798caeb39ab0c8853d3e0512baacfe7',
        'http://dbp-resource.gz.bcebos.com/51952f2a-c778-7440-cf78-8146b2001f81/25.png?authorization=bce-auth-v1%2Fa4d81bbd930c41e6857b989362415714%2F2018-06-15T02%3A04%3A31Z%2F-1%2F%2F87317f3e136693abd315e7f00282c0e68c2c1fd282e5a6c7715ce9cc36f7e46f',
        'http://dbp-resource.gz.bcebos.com/51952f2a-c778-7440-cf78-8146b2001f81/26.png?authorization=bce-auth-v1%2Fa4d81bbd930c41e6857b989362415714%2F2018-06-15T02%3A04%3A31Z%2F-1%2F%2Ffc5fe02d380256ced90b7db04b9bd351667420c28a2d308c21f883df5ec130ed',
        'http://dbp-resource.gz.bcebos.com/51952f2a-c778-7440-cf78-8146b2001f81/27.png?authorization=bce-auth-v1%2Fa4d81bbd930c41e6857b989362415714%2F2018-06-15T02%3A04%3A31Z%2F-1%2F%2Fd7123dcdbb7beb8474d2cf0c35d3c05a0034f8c2b046acaaa833d1417dd88979',
        'http://dbp-resource.gz.bcebos.com/51952f2a-c778-7440-cf78-8146b2001f81/28.png?authorization=bce-auth-v1%2Fa4d81bbd930c41e6857b989362415714%2F2018-06-15T02%3A04%3A31Z%2F-1%2F%2Fbb337bd0380414ffbc0aeefe6204b722afad664810c300f97bb280fcc5fc6590',
        'http://dbp-resource.gz.bcebos.com/51952f2a-c778-7440-cf78-8146b2001f81/29.png?authorization=bce-auth-v1%2Fa4d81bbd930c41e6857b989362415714%2F2018-06-15T02%3A04%3A32Z%2F-1%2F%2F66652147cc150ab58238f0ad241983c82747e8da4435e0c9f98ade86d7637d70',
        'http://dbp-resource.gz.bcebos.com/51952f2a-c778-7440-cf78-8146b2001f81/30.png?authorization=bce-auth-v1%2Fa4d81bbd930c41e6857b989362415714%2F2018-06-15T02%3A04%3A32Z%2F-1%2F%2F71b793f028a84853ddd0b958e34535e27f41410d4b7f1415e8e0515db6ad0bf5',
        'http://dbp-resource.gz.bcebos.com/51952f2a-c778-7440-cf78-8146b2001f81/31.png?authorization=bce-auth-v1%2Fa4d81bbd930c41e6857b989362415714%2F2018-06-15T02%3A04%3A32Z%2F-1%2F%2F17e476ad4bda9405a56cb85f2e04d8bc6057f629c78780e2545e39e3ffe7aea2',
        'http://dbp-resource.gz.bcebos.com/51952f2a-c778-7440-cf78-8146b2001f81/32.png?authorization=bce-auth-v1%2Fa4d81bbd930c41e6857b989362415714%2F2018-06-15T02%3A04%3A32Z%2F-1%2F%2Faf33398d79d24c97ed7e8990ad1d5e6808114713114f97de8cebb1eff1eed0e0',
        'http://dbp-resource.gz.bcebos.com/51952f2a-c778-7440-cf78-8146b2001f81/33.png?authorization=bce-auth-v1%2Fa4d81bbd930c41e6857b989362415714%2F2018-06-15T02%3A04%3A32Z%2F-1%2F%2F8f5f35c5a6945946ae96e6758d532edd0cc34360b12a17fea6018925d9df405a',
        'http://dbp-resource.gz.bcebos.com/51952f2a-c778-7440-cf78-8146b2001f81/34.png?authorization=bce-auth-v1%2Fa4d81bbd930c41e6857b989362415714%2F2018-06-15T02%3A04%3A32Z%2F-1%2F%2F3346da552ab7ed0e38aecb2134287720f5ce0e6ae61d92a092ed64499b0785b0',
        'http://dbp-resource.gz.bcebos.com/51952f2a-c778-7440-cf78-8146b2001f81/35.png?authorization=bce-auth-v1%2Fa4d81bbd930c41e6857b989362415714%2F2018-06-15T02%3A04%3A33Z%2F-1%2F%2Ff62465fd2cf26b5ad2447372bbd97256e2d725c9e86665f7e00a930bd4c73963',
        'http://dbp-resource.gz.bcebos.com/51952f2a-c778-7440-cf78-8146b2001f81/36.png?authorization=bce-auth-v1%2Fa4d81bbd930c41e6857b989362415714%2F2018-06-15T02%3A04%3A33Z%2F-1%2F%2F98007f27c489c6f60b771b1e2b996b150b6fcf0c680df6b8c0e9e8ec82195de9',
        'http://dbp-resource.gz.bcebos.com/51952f2a-c778-7440-cf78-8146b2001f81/37.png?authorization=bce-auth-v1%2Fa4d81bbd930c41e6857b989362415714%2F2018-06-15T02%3A04%3A33Z%2F-1%2F%2F2839a525ed8687f405a073f9c65170d881e0d0aa2a71c9e43f64498f6672070c',
        'http://dbp-resource.gz.bcebos.com/51952f2a-c778-7440-cf78-8146b2001f81/38.png?authorization=bce-auth-v1%2Fa4d81bbd930c41e6857b989362415714%2F2018-06-15T02%3A04%3A33Z%2F-1%2F%2F07c6118af02b3c29d1bc123b8b5e68ffcb90f320182af98c77d40d63a12e3146',
        'http://dbp-resource.gz.bcebos.com/51952f2a-c778-7440-cf78-8146b2001f81/39.png?authorization=bce-auth-v1%2Fa4d81bbd930c41e6857b989362415714%2F2018-06-15T02%3A04%3A33Z%2F-1%2F%2F2762071811d6cedd2957040122e83694fb4edc26a34735f4601e78f764013e7a',
        'http://dbp-resource.gz.bcebos.com/51952f2a-c778-7440-cf78-8146b2001f81/40.png?authorization=bce-auth-v1%2Fa4d81bbd930c41e6857b989362415714%2F2018-06-15T02%3A04%3A33Z%2F-1%2F%2Fb16a18afb3afa3fc71aa38b59404a171c633588d882c531ccc2386ba9ce164ad',
        'http://dbp-resource.gz.bcebos.com/51952f2a-c778-7440-cf78-8146b2001f81/41.png?authorization=bce-auth-v1%2Fa4d81bbd930c41e6857b989362415714%2F2018-06-15T02%3A04%3A34Z%2F-1%2F%2Fcc2144763de0de1a99a380bb4efe9ec130a12279e627190c8279b59c7c05b992',
        'http://dbp-resource.gz.bcebos.com/51952f2a-c778-7440-cf78-8146b2001f81/42.png?authorization=bce-auth-v1%2Fa4d81bbd930c41e6857b989362415714%2F2018-06-15T02%3A04%3A34Z%2F-1%2F%2F3bafa095f04bf0a699be8ec34e206d6d7d63180b6ec50405087fdb66b3c9d4d3',
        'http://dbp-resource.gz.bcebos.com/51952f2a-c778-7440-cf78-8146b2001f81/43.png?authorization=bce-auth-v1%2Fa4d81bbd930c41e6857b989362415714%2F2018-06-15T02%3A04%3A34Z%2F-1%2F%2Fa439638ce1752885914d6c444d0b2223bce01917f5a6b89cefc774fad3ec25a8',
        'http://dbp-resource.gz.bcebos.com/51952f2a-c778-7440-cf78-8146b2001f81/44.png?authorization=bce-auth-v1%2Fa4d81bbd930c41e6857b989362415714%2F2018-06-15T02%3A04%3A34Z%2F-1%2F%2F3169056f7a481015d0babd335af6a788661ae0a631ee5cc81e04067e75872085',
        'http://dbp-resource.gz.bcebos.com/51952f2a-c778-7440-cf78-8146b2001f81/45.png?authorization=bce-auth-v1%2Fa4d81bbd930c41e6857b989362415714%2F2018-06-15T02%3A04%3A34Z%2F-1%2F%2F3cdf4587eea87f316423037d470156853758ff7c9fd13ae204a566f357cf15d9',
        'http://dbp-resource.gz.bcebos.com/51952f2a-c778-7440-cf78-8146b2001f81/46.png?authorization=bce-auth-v1%2Fa4d81bbd930c41e6857b989362415714%2F2018-06-15T02%3A04%3A34Z%2F-1%2F%2Fc49ce953473753ad34472814a5097397e40b5796904f366954231d8729fde7da',
        'http://dbp-resource.gz.bcebos.com/51952f2a-c778-7440-cf78-8146b2001f81/47.png?authorization=bce-auth-v1%2Fa4d81bbd930c41e6857b989362415714%2F2018-06-15T02%3A04%3A35Z%2F-1%2F%2F9f265c033f80f1955b7acccad1d218f937e86bf464710285f4e1530a8e74de0e',
        'http://dbp-resource.gz.bcebos.com/51952f2a-c778-7440-cf78-8146b2001f81/48.png?authorization=bce-auth-v1%2Fa4d81bbd930c41e6857b989362415714%2F2018-06-15T02%3A04%3A35Z%2F-1%2F%2F86ee7ebe48ac9f18368a91b925191e61e6de6f4796afb24f3b4b8da0efd51005',
        'http://dbp-resource.gz.bcebos.com/51952f2a-c778-7440-cf78-8146b2001f81/49.png?authorization=bce-auth-v1%2Fa4d81bbd930c41e6857b989362415714%2F2018-06-15T02%3A04%3A35Z%2F-1%2F%2F5615b7f4b58c7f176cc34bb69c2717bab7d118f2b7c3e9e33c8573a7e28328e5',
        'http://dbp-resource.gz.bcebos.com/51952f2a-c778-7440-cf78-8146b2001f81/50.png?authorization=bce-auth-v1%2Fa4d81bbd930c41e6857b989362415714%2F2018-06-15T02%3A05%3A17Z%2F-1%2F%2Faf918a689c8b2c4a793349cff4ac8dd8dbe35e54a9c613d344c3312060a00991',
        'http://dbp-resource.gz.bcebos.com/51952f2a-c778-7440-cf78-8146b2001f81/51.png?authorization=bce-auth-v1%2Fa4d81bbd930c41e6857b989362415714%2F2018-06-15T02%3A05%3A28Z%2F-1%2F%2F2e508951f357322115221711a156dd360a840fafd39cc8c249fd4a0c20d902e1',
        'http://dbp-resource.gz.bcebos.com/51952f2a-c778-7440-cf78-8146b2001f81/52.png?authorization=bce-auth-v1%2Fa4d81bbd930c41e6857b989362415714%2F2018-06-15T02%3A05%3A47Z%2F-1%2F%2Fd8e2aca31d7a17ee400ae61d46576825f7bcaa717e26d64ff41629a9185cf345',
        'http://dbp-resource.gz.bcebos.com/51952f2a-c778-7440-cf78-8146b2001f81/53.png?authorization=bce-auth-v1%2Fa4d81bbd930c41e6857b989362415714%2F2018-06-15T02%3A05%3A47Z%2F-1%2F%2Fca83db0985a21bda30f87270d8df6b5d11412575d92e0291aa6c9bd8e9aea202',
        'http://dbp-resource.gz.bcebos.com/51952f2a-c778-7440-cf78-8146b2001f81/54.png?authorization=bce-auth-v1%2Fa4d81bbd930c41e6857b989362415714%2F2018-06-15T02%3A05%3A47Z%2F-1%2F%2F8723ed35bb2ced48b4ae41e3ba1b4c0c6ab521ad7cf68d217bffda888aa3cd16',
        'http://dbp-resource.gz.bcebos.com/51952f2a-c778-7440-cf78-8146b2001f81/55.png?authorization=bce-auth-v1%2Fa4d81bbd930c41e6857b989362415714%2F2018-06-15T02%3A05%3A48Z%2F-1%2F%2F7053a7a50ffb17303d921f5a2b912595b1c868feee9a64726249ecba6b9182ca',
        'http://dbp-resource.gz.bcebos.com/51952f2a-c778-7440-cf78-8146b2001f81/56.png?authorization=bce-auth-v1%2Fa4d81bbd930c41e6857b989362415714%2F2018-06-15T02%3A05%3A48Z%2F-1%2F%2F0ffb56f5cd0baa92540c58640569b8370ecb682fe38f39cd3b1740870505558a',
        'http://dbp-resource.gz.bcebos.com/51952f2a-c778-7440-cf78-8146b2001f81/57.png?authorization=bce-auth-v1%2Fa4d81bbd930c41e6857b989362415714%2F2018-06-15T02%3A05%3A48Z%2F-1%2F%2F30118269a3142e8c498d2db8c1a42e63ab5748b9a0c57007212b7d89239ed17b',
        'http://dbp-resource.gz.bcebos.com/51952f2a-c778-7440-cf78-8146b2001f81/58.png?authorization=bce-auth-v1%2Fa4d81bbd930c41e6857b989362415714%2F2018-06-15T02%3A05%3A48Z%2F-1%2F%2F40e8b2e093287f4a9a81cb1ed6e3a8bdbfa8b2c77bd98d00668d64a991e7b1bc',
        'http://dbp-resource.gz.bcebos.com/51952f2a-c778-7440-cf78-8146b2001f81/59.png?authorization=bce-auth-v1%2Fa4d81bbd930c41e6857b989362415714%2F2018-06-15T02%3A05%3A48Z%2F-1%2F%2Fa83ac7995f5c373abc5f99b4210e732b97b6c7d82d7c476867ed2a5585be7802',
        'http://dbp-resource.gz.bcebos.com/51952f2a-c778-7440-cf78-8146b2001f81/60.png?authorization=bce-auth-v1%2Fa4d81bbd930c41e6857b989362415714%2F2018-06-15T02%3A05%3A48Z%2F-1%2F%2F9f3d760fe0387fe8c059046cf3434768e6721924dc788132cfabf3076e38bcf4',
        'http://dbp-resource.gz.bcebos.com/51952f2a-c778-7440-cf78-8146b2001f81/61.png?authorization=bce-auth-v1%2Fa4d81bbd930c41e6857b989362415714%2F2018-06-15T02%3A05%3A49Z%2F-1%2F%2Fa75156b38bb167c7274efdef400ce32a9a978c552579e01ccee7ef9555e8dfb7',
        'http://dbp-resource.gz.bcebos.com/51952f2a-c778-7440-cf78-8146b2001f81/62.png?authorization=bce-auth-v1%2Fa4d81bbd930c41e6857b989362415714%2F2018-06-15T02%3A05%3A49Z%2F-1%2F%2F5f1fd15503efa69928f42c4b6146c06e635790e0e6057adc727cdd1a9dcbe068',
        'http://dbp-resource.gz.bcebos.com/51952f2a-c778-7440-cf78-8146b2001f81/63.png?authorization=bce-auth-v1%2Fa4d81bbd930c41e6857b989362415714%2F2018-06-15T02%3A05%3A49Z%2F-1%2F%2Fe18253138e6f6887f9c4d33ff592c240d4f9e50f45a89c4f1e7459fd4c533a6f',
        'http://dbp-resource.gz.bcebos.com/51952f2a-c778-7440-cf78-8146b2001f81/64.png?authorization=bce-auth-v1%2Fa4d81bbd930c41e6857b989362415714%2F2018-06-15T02%3A05%3A50Z%2F-1%2F%2F7ec720a734b53dcf48d0695019420625d987a9fdbbac4fa2526436812a6f4a9c',
        'http://dbp-resource.gz.bcebos.com/51952f2a-c778-7440-cf78-8146b2001f81/65.png?authorization=bce-auth-v1%2Fa4d81bbd930c41e6857b989362415714%2F2018-06-15T02%3A05%3A50Z%2F-1%2F%2F3164cd8608ee56687be3c466afa2291e6b5966539010daa46bc4402652116669',
        'http://dbp-resource.gz.bcebos.com/51952f2a-c778-7440-cf78-8146b2001f81/66.png?authorization=bce-auth-v1%2Fa4d81bbd930c41e6857b989362415714%2F2018-06-15T02%3A05%3A50Z%2F-1%2F%2F985fd4acbf412baa1829e95f7f18cd64413d14098bf0aa9151a475311f069893',
        'http://dbp-resource.gz.bcebos.com/51952f2a-c778-7440-cf78-8146b2001f81/67.png?authorization=bce-auth-v1%2Fa4d81bbd930c41e6857b989362415714%2F2018-06-15T02%3A05%3A50Z%2F-1%2F%2F530ec82669fa8a075bf9a5be8c6be1e865a29035cd96ea31be8e60ef1e05fd6b',
        'http://dbp-resource.gz.bcebos.com/51952f2a-c778-7440-cf78-8146b2001f81/68.png?authorization=bce-auth-v1%2Fa4d81bbd930c41e6857b989362415714%2F2018-06-15T02%3A05%3A50Z%2F-1%2F%2Fb90f911f46cb68ee83fe3fdb8f2add2c6cd3b0324524fff64aecaac2041a32d7',
        'http://dbp-resource.gz.bcebos.com/51952f2a-c778-7440-cf78-8146b2001f81/69.png?authorization=bce-auth-v1%2Fa4d81bbd930c41e6857b989362415714%2F2018-06-15T02%3A05%3A51Z%2F-1%2F%2F84cd01ce7a1b363de255f1e71b23569cc254186873959c2af1629646ef13cbac',
        'http://dbp-resource.gz.bcebos.com/51952f2a-c778-7440-cf78-8146b2001f81/70.png?authorization=bce-auth-v1%2Fa4d81bbd930c41e6857b989362415714%2F2018-06-15T02%3A05%3A51Z%2F-1%2F%2Fcc26462fa01a0c2f58b57d959f1af5795006ae427d8e9e1b0090786ca77523fd',
        'http://dbp-resource.gz.bcebos.com/51952f2a-c778-7440-cf78-8146b2001f81/71.png?authorization=bce-auth-v1%2Fa4d81bbd930c41e6857b989362415714%2F2018-06-15T02%3A05%3A51Z%2F-1%2F%2F979c61c0442cb082247cea8c20df44445e73cf142e68e52db6c6a06aca218e6c',
        'http://dbp-resource.gz.bcebos.com/51952f2a-c778-7440-cf78-8146b2001f81/72.png?authorization=bce-auth-v1%2Fa4d81bbd930c41e6857b989362415714%2F2018-06-15T02%3A05%3A51Z%2F-1%2F%2Fe2b6a6a575d3d14f8f208e77dfbf29c4aab02ede40c314f7a89099e2ee4e4dc6',
        'http://dbp-resource.gz.bcebos.com/51952f2a-c778-7440-cf78-8146b2001f81/73.png?authorization=bce-auth-v1%2Fa4d81bbd930c41e6857b989362415714%2F2018-06-15T02%3A05%3A52Z%2F-1%2F%2F28f8bf749c0dac213b1298264d1f8b85755a4cb96ee07fc8d03988846ab8e35a',
        'http://dbp-resource.gz.bcebos.com/51952f2a-c778-7440-cf78-8146b2001f81/74.png?authorization=bce-auth-v1%2Fa4d81bbd930c41e6857b989362415714%2F2018-06-15T02%3A05%3A52Z%2F-1%2F%2F70b11422dd8d30ad6e28d0047025aae0ae175a998be6b3e162a4f54576277b40',
        'http://dbp-resource.gz.bcebos.com/51952f2a-c778-7440-cf78-8146b2001f81/75.png?authorization=bce-auth-v1%2Fa4d81bbd930c41e6857b989362415714%2F2018-06-15T02%3A05%3A52Z%2F-1%2F%2Ff311b19a37079d8a3dad6eed4239dad49435e699253b20a43b91f68e7256bebc',
        'http://dbp-resource.gz.bcebos.com/51952f2a-c778-7440-cf78-8146b2001f81/76.png?authorization=bce-auth-v1%2Fa4d81bbd930c41e6857b989362415714%2F2018-06-15T02%3A05%3A52Z%2F-1%2F%2F5241aed735ef199f58a8ae2f56b72e5e9a49c08dd251af2bf9ec7216bc8881fc',
        'http://dbp-resource.gz.bcebos.com/51952f2a-c778-7440-cf78-8146b2001f81/77.png?authorization=bce-auth-v1%2Fa4d81bbd930c41e6857b989362415714%2F2018-06-15T02%3A05%3A52Z%2F-1%2F%2F3684fa9daf1e4b60b00345546fdeb9f97c9de66c518cab953dffecc1c2e129c9',
        'http://dbp-resource.gz.bcebos.com/51952f2a-c778-7440-cf78-8146b2001f81/78.png?authorization=bce-auth-v1%2Fa4d81bbd930c41e6857b989362415714%2F2018-06-15T02%3A05%3A52Z%2F-1%2F%2F17b589ca076b59d816fcce98dddb3f321626dffd7f841356b1e245704c6e22cc',
        'http://dbp-resource.gz.bcebos.com/51952f2a-c778-7440-cf78-8146b2001f81/79.png?authorization=bce-auth-v1%2Fa4d81bbd930c41e6857b989362415714%2F2018-06-15T02%3A05%3A53Z%2F-1%2F%2F3a42ae78f94ddd8b1c5382055e1b4f721ccf15040b6adcac708a8c88d1bf8835',
        'http://dbp-resource.gz.bcebos.com/51952f2a-c778-7440-cf78-8146b2001f81/80.png?authorization=bce-auth-v1%2Fa4d81bbd930c41e6857b989362415714%2F2018-06-15T02%3A05%3A53Z%2F-1%2F%2Ff7eba9f71e649f0a3ca96896be27d1c9373094044d5258f236f38038a1d6fda2',
        'http://dbp-resource.gz.bcebos.com/51952f2a-c778-7440-cf78-8146b2001f81/81.png?authorization=bce-auth-v1%2Fa4d81bbd930c41e6857b989362415714%2F2018-06-15T02%3A05%3A53Z%2F-1%2F%2F8460afc83ea37471be52669a570a4d9175ebedd970947b9f41d853c968766e63',
        'http://dbp-resource.gz.bcebos.com/51952f2a-c778-7440-cf78-8146b2001f81/82.png?authorization=bce-auth-v1%2Fa4d81bbd930c41e6857b989362415714%2F2018-06-15T02%3A05%3A54Z%2F-1%2F%2Fc92e6235fa68811cefec4da145cda9abc7c416d779f3dda0bb45eb04386a1150',
        'http://dbp-resource.gz.bcebos.com/51952f2a-c778-7440-cf78-8146b2001f81/83.png?authorization=bce-auth-v1%2Fa4d81bbd930c41e6857b989362415714%2F2018-06-15T02%3A05%3A54Z%2F-1%2F%2Ffe3919d5ab9346f37f5e9c4ad4c4da7a6da42944f0834b7c1ed85d72fd67a161',
        'http://dbp-resource.gz.bcebos.com/51952f2a-c778-7440-cf78-8146b2001f81/84.png?authorization=bce-auth-v1%2Fa4d81bbd930c41e6857b989362415714%2F2018-06-15T02%3A05%3A54Z%2F-1%2F%2Ff2a62966852d9bfa5ba9c23c8b91ac43218a4e27c30387b1d272905557624dc7',
        'http://dbp-resource.gz.bcebos.com/51952f2a-c778-7440-cf78-8146b2001f81/85.png?authorization=bce-auth-v1%2Fa4d81bbd930c41e6857b989362415714%2F2018-06-15T02%3A05%3A54Z%2F-1%2F%2F127329b0a80ddf578774ced43094e554f6ab9c0d627e0d06a66e479145b3f70d',
        'http://dbp-resource.gz.bcebos.com/51952f2a-c778-7440-cf78-8146b2001f81/86.png?authorization=bce-auth-v1%2Fa4d81bbd930c41e6857b989362415714%2F2018-06-15T02%3A05%3A54Z%2F-1%2F%2Fed67bf2251a94ea442d99770ae87d35e153493941753fc225b5694d23b636774',
        'http://dbp-resource.gz.bcebos.com/51952f2a-c778-7440-cf78-8146b2001f81/87.png?authorization=bce-auth-v1%2Fa4d81bbd930c41e6857b989362415714%2F2018-06-15T02%3A05%3A54Z%2F-1%2F%2F54a2e6f83446e6b52cbe624d5a2c39bd3e966f13bf6c4f9f34d177e943697c51',
        'http://dbp-resource.gz.bcebos.com/51952f2a-c778-7440-cf78-8146b2001f81/88.png?authorization=bce-auth-v1%2Fa4d81bbd930c41e6857b989362415714%2F2018-06-15T02%3A05%3A55Z%2F-1%2F%2F6ad1f5209f0e25d79789c72960edeb393796f212dafc7803ecbb4f583ff8171f',
        'http://dbp-resource.gz.bcebos.com/51952f2a-c778-7440-cf78-8146b2001f81/89.png?authorization=bce-auth-v1%2Fa4d81bbd930c41e6857b989362415714%2F2018-06-15T02%3A05%3A55Z%2F-1%2F%2Fa10db062492894c09b65f4869a1a9e5a3309d686d2ebb72c56dea686192ee905',
        'http://dbp-resource.gz.bcebos.com/51952f2a-c778-7440-cf78-8146b2001f81/90.png?authorization=bce-auth-v1%2Fa4d81bbd930c41e6857b989362415714%2F2018-06-15T02%3A05%3A55Z%2F-1%2F%2Fdef621366c474dcaa938ba7a4df3b140ae6f8934555fa23309c753729b294653',
        'http://dbp-resource.gz.bcebos.com/51952f2a-c778-7440-cf78-8146b2001f81/91.png?authorization=bce-auth-v1%2Fa4d81bbd930c41e6857b989362415714%2F2018-06-15T02%3A05%3A55Z%2F-1%2F%2F700a9703ccd809f61a3540ffef9489111d5cdd3ae6483dea4a36140c25e16478',
        'http://dbp-resource.gz.bcebos.com/51952f2a-c778-7440-cf78-8146b2001f81/92.png?authorization=bce-auth-v1%2Fa4d81bbd930c41e6857b989362415714%2F2018-06-15T02%3A05%3A55Z%2F-1%2F%2F22821c4f0101359f99349fc71b35715bd7b65f39a29681902f077b0466662629',
        'http://dbp-resource.gz.bcebos.com/51952f2a-c778-7440-cf78-8146b2001f81/93.png?authorization=bce-auth-v1%2Fa4d81bbd930c41e6857b989362415714%2F2018-06-15T02%3A05%3A55Z%2F-1%2F%2F6f02fb76e3c39d67c098170325b6adbb3136c86ea873544ca4e0884b038bb795',
        'http://dbp-resource.gz.bcebos.com/51952f2a-c778-7440-cf78-8146b2001f81/94.png?authorization=bce-auth-v1%2Fa4d81bbd930c41e6857b989362415714%2F2018-06-15T02%3A05%3A56Z%2F-1%2F%2Fd89c4727c1d568fe2256ee12ac1df1f1735b1ac9f540872745edcb611dce8890',
        'http://dbp-resource.gz.bcebos.com/51952f2a-c778-7440-cf78-8146b2001f81/95.png?authorization=bce-auth-v1%2Fa4d81bbd930c41e6857b989362415714%2F2018-06-15T02%3A05%3A56Z%2F-1%2F%2F4271ba3fe5ad96532905343b49ac9c4781b68369edae78e5acab36dc2104f615',
        'http://dbp-resource.gz.bcebos.com/51952f2a-c778-7440-cf78-8146b2001f81/96.png?authorization=bce-auth-v1%2Fa4d81bbd930c41e6857b989362415714%2F2018-06-15T02%3A05%3A56Z%2F-1%2F%2F42daf37db5c2c92f0745d2c2a8a358ac4106cc96fda6416f9a76e38a03951c3c',
        'http://dbp-resource.gz.bcebos.com/51952f2a-c778-7440-cf78-8146b2001f81/97.png?authorization=bce-auth-v1%2Fa4d81bbd930c41e6857b989362415714%2F2018-06-15T02%3A05%3A56Z%2F-1%2F%2F3755892bdc9548a78f3eff532ff7ccaa8a5fbd37c8ae63723537746d608cd88e',
        'http://dbp-resource.gz.bcebos.com/51952f2a-c778-7440-cf78-8146b2001f81/98.png?authorization=bce-auth-v1%2Fa4d81bbd930c41e6857b989362415714%2F2018-06-15T02%3A05%3A56Z%2F-1%2F%2Ffca804587e7baa54b80390f9052a98dec7dae9a1a8e6761f844e8d4f9f86e3b4',
        'http://dbp-resource.gz.bcebos.com/51952f2a-c778-7440-cf78-8146b2001f81/99.png?authorization=bce-auth-v1%2Fa4d81bbd930c41e6857b989362415714%2F2018-06-15T02%3A05%3A56Z%2F-1%2F%2Fd1f193da00d53d9a7de4384eea76678465829fbb05e9c3b3e599cc8c7bae10ff',
        'http://dbp-resource.gz.bcebos.com/51952f2a-c778-7440-cf78-8146b2001f81/100.png?authorization=bce-auth-v1%2Fa4d81bbd930c41e6857b989362415714%2F2018-06-15T02%3A06%3A07Z%2F-1%2F%2F01ed2f80d937658b0100b5b4e8b40fccfa3bb2ef587d0e5f15b6e62e28e3c925'
    ]

if __name__ == '__main__':

    pass