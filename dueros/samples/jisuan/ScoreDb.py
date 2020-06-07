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

class ScoreDb(object):

    def get_db(self):
        """
        :rtype: object
        """
        db = pymysql.connect('localhost', 'root', '123456', 'JISUAN', charset='utf8')
        return db

    pass


if __name__ == '__main__':
    pass