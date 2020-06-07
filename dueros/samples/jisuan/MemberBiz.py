#!/usr/bin/env python3
# -*- encoding=utf-8 -*-

# description:
# author:jack
# create_time: 2018/7/19

"""
    desc:pass
"""

from dueros.samples.jisuan.MemberDb import MemberDb


class MemberBiz(object):

    def get_db(self):
        dao = MemberDb()
        return dao

    def add_member(self, device_id):
        if device_id:
            if not self.get_db().check_exist_member(device_id):
                self.get_db().add_member(device_id)

    def query_rank_device_id(self, device_id):

        if device_id:
            if self.get_db().check_exist_member(device_id):
                result = self.get_db().query_rank_by_device_id(device_id)
                return result[3]
            else:
                self.get_db().add_member(device_id)
                return None

    def query_rank(self, limit=10):

        return self.get_db().query_rank(limit)

    def incr_member_score(self, device_id):
        if device_id:
            if not self.get_db().check_exist_member(device_id):
                self.get_db().add_member(device_id)
            self.get_db().incr_member_score(device_id)

if __name__ == '__main__':

    biz = MemberBiz()
    print(biz.query_rank_device_id('111'))
    pass