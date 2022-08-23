# !/usr/bin/env python
# -*- coding: utf-8 -*-

######################################################################
#
# (c) Copyright University of Southampton, 2022
# # Copyright in this software belongs to University of Southampton,
# Highfield, University Road, Southampton SO17 1BJ
#
# Created By : Sohaib Karous
# Created Date : 2022/08/18
# Project : FloraGuard
# ######################################################################

class SellerInfo:

    def __init__(self, username, seller_url):
        self.username = username
        self.comments = {}
        self.profile_url = seller_url
        self.attributes = {}

    def add_item(self, url, desc, date, price, title):
        if url in self.comments:
            self.comments[url].append({
                "description": desc,
                "date": date,
                "price": price,
                "url": url,
                "comment": title,
                "thread": title
            })
        else:
            self.comments[url] = [{
                "description": desc,
                "date": date,
                "price": price,
                "url": url,
                "comment": title,
                "thread": title
            }]

    def get_profile_url(self):
        return self.profile_url

    def get_all_comments(self):
        all_comments = []
        for _, comment in self.comments.items():
            # Title is the 'comment'
            comment_list = [x["comment"] for x in comment]
            all_comments += comment_list

        return all_comments
