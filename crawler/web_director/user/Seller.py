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

    def __init__(self, username, seller_url, seller_description):
        self.username = username
        self.comments = {}
        self.profile_url = seller_url
        self.profile_description = seller_description
        self.attributes = {}

    def add_item(self, url, desc, date, price, title, reviews, **kargs):
        if url in self.comments:
            self.comments[url].append({
                "description": desc,
                "date": date,
                "price": price,
                "url": url,
                "comment": title,
                "thread": title,
                "reviews": reviews
            })
        else:
            self.comments[url] = [{
                "description": desc,
                "date": date,
                "price": price,
                "url": url,
                "comment": title,
                "thread": title,
                "reviews": reviews
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
        for _, comment in self.comments.items():
            # Title is the 'comment'
            desc_list = [x["description"] for x in comment]
            title_list = [x["comment"] for x in comment]
            all_comments += desc_list
            all_comments += title_list

            for x in comment:
                for _, review in x['reviews'].items():
                    all_comments += review.get_all_comments()

        return all_comments

    def __str__(self):
        return "Username: " + self.username + "\nProfile URL extension : " + self.profile_url + "\nDescription: " + self.profile_description + "\nAttributes: " + str(
            self.attributes) + "\nList of comments:" + str(self.comments)