#!/usr/bin/env python3
# -*- encoding=utf-8 -*-

# description:
# author:jack
# create_time: 2018/7/19

"""
    desc:pass
"""

import pymysql
import datetime


class MemberDb(object):


    def get_db(self):
        """
        :rtype: object
        """
        db = pymysql.connect('localhost', 'root', '123456', 'JISUAN', charset='utf8')
        return db

    def add_member(self, device_id):
        """
        添加会员
        :param device_id:
        :return:
        """
        db = self.get_db()
        cursor = db.cursor()
        current_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        sql = "INSERT INTO MEMBER (VERSION, CREATE_TIME, LAST_MODIFY_TIME, DEVICE_ID) VALUES (0, '%s', '%s', '%s');" \
              % (current_time, current_time, device_id)
        cursor.execute(sql)
        db.commit()
        cursor.close()
        db.cursor()

    def check_exist_member(self, device_id):
        """
        校验会员
        :param device_id:
        :return:
        """
        db = self.get_db()
        cursor = db.cursor()
        sql = "SELECT COUNT(ID) FROM MEMBER WHERE DEVICE_ID = '%s';" % device_id
        cursor.execute(sql)
        result = cursor.fetchone()
        return result[0] > 0

    def update_member_name(self, device_id, name):
        """
        更新会员昵称
        :param device_id:
        :param name:
        :return:
        """
        db = self.get_db()
        cursor = db.cursor()
        current_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        sql = "UPDATE MEMBER SET LAST_MODIFY_TIME = '%s', DISPLAY_NAME = '%s' WHERE DEVICE_ID = '%s';" % (current_time, name, device_id)
        result = cursor.execute(sql)
        db.commit()
        cursor.close()
        db.close()

    def incr_member_score(self, device_id):
        """

        :param device_id:
        :return:
        """
        db = self.get_db()
        cursor = db.cursor()
        sql = "UPDATE MEMBER SET SCORE = SCORE + 1 WHERE DEVICE_ID = '%s';" % device_id
        cursor.execute(sql)
        db.commit()
        cursor.close()
        db.close()

    def clear_score(self):
        db = self.get_db()
        cursor = db.cursor()
        sql = "UPDATE MEMBER SET SCORE = 0;"
        cursor.execute(sql)
        db.commit()
        cursor.close()
        db.close()

    def query_rank(self, limit=10):
        """
        查询绑定
        :return:
        """
        db = self.get_db()
        cursor = db.cursor()
        sql = "SELECT ID, DEVICE_ID, SCORE, rank FROM (SELECT ID, DEVICE_ID, SCORE, @curRank := IF(@prevRank = SCORE, @curRank, @incRank) AS rank, @incRank :=@incRank+ 1, @prevRank := SCORE FROM MEMBER p, ( SELECT @curRank :=0, @prevRank := NULL, @incRank := 1 ) r ORDER BY SCORE DESC ) s WHERE rank <= %s;" % limit
        cursor.execute(sql)
        result = cursor.fetchall()
        print(result)
        return result

    def query_rank_by_device_id(self, device_id):
        """
        查询排名
        :param device_id:
        :return:
        """
        db = self.get_db()
        cursor = db.cursor()
        sql = "SELECT ID, DEVICE_ID, SCORE, rank FROM (SELECT ID, DEVICE_ID, SCORE, @curRank := IF(@prevRank = SCORE, @curRank, @incRank) AS rank, @incRank :=@incRank+ 1, @prevRank := SCORE FROM MEMBER p, ( SELECT @curRank :=0, @prevRank := NULL, @incRank := 1 ) r ORDER BY SCORE DESC ) s WHERE s.DEVICE_ID = '%s';" % device_id
        cursor.execute(sql)
        result = cursor.fetchone()
        print(result)
        return result


if __name__ == '__main__':

    db = MemberDb()
    db.add_member('11112')
    # db.update_member_name('1111', 'ssss')
    print(db.check_exist_member('1111'))
    db.incr_member_score('1111200')
    # db.clear_score()
    db.query_rank_by_device_id('1111299')
    db.query_rank()
    pass