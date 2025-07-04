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
class UserInfo:

    def __init__(self, username, profile_url, comment_limit=100):
        self.username = username
        self.comments = {}
        self.attributes = {}
        self.profile_url = profile_url
        self.comment_limit = comment_limit

    def add_comment(self, comment, thread, url, date, **kargs):

        if url in self.comments:
            # Limiting it to the most recent 100 comments in order to keep the memory impact low
            if len(self.comments) > self.comment_limit:
                self.comments[url].pop()
            self.comments[url].append({
                "comment": comment,
                "date": date,
                "url": url,
                "thread": thread
            })
        else:
            self.comments[url] = [{
                "comment": comment,
                "date": date,
                "url": url,
                "thread": thread
            }]

    def add_attribute(self, attribute_name, attribute):
        if attribute_name in self.attributes:
            self.attributes[attribute_name] += [attribute]
        else:
            self.attributes[attribute_name] = [attribute]

    def get_profile_url(self):
        return self.profile_url

    def get_all_comments(self):
        all_comments = []
        for thread, comments in self.comments.items():
            comment_list = [x["comment"] for x in comments]
            all_comments += comment_list

        return all_comments

    def __str__(self):
        return "Username: " + self.username + "\nProfile URL extension : " + self.profile_url + "\nAttributes: " + str(
            self.attributes) + "\nList of comments:" + str(self.comments)
