# !/usr/bin/env python
# -*- coding: utf-8 -*-

###########################################################################################################
#
# (c) Copyright University of Southampton and Royal Botanic Gardens, Kew, 2022
#
# Copyright in this software belongs to University of Southampton
# Highfield, University Road, Southampton SO17 1BJ
# and
# Royal Botanic Gardens, Kew # Kew, Richmond, London, TW9 3AE
#
# Created By : Alex Kazaryan
# Created Date : 2022/08/18
# Project : Illegal Wildlife Trade Challenge Fund project IWT114
# ###########################################################################################################


import os
import re
import requests
import logging
import dateutil.parser as dparser
from bs4 import BeautifulSoup
from datetime import datetime
from web_director.user.Seller import SellerInfo
from web_director.user.User import UserInfo
from web_director.abc import MarketPlaceABC, WebAbstractClass

NOT_FOUND = 'NOT FOUND'

class WebpageHandler:

    def __init__(self, webpage, thread_model, comment_model, comment_keyword_names, filter_comments, anonymous):
        if anonymous: logging.info("Anonymous crawling activated")

        self.crawler_stats = {"Threads seen": 0, "Profiles scraped": 0}
        self.webpage = webpage
        self.thread_model = thread_model
        self.comment_model = comment_model
        self.comment_keyword_names = comment_keyword_names
        self.people = {}
        self.interesting_people = []
        self.anonymous = anonymous
        self.filter_comments = filter_comments


    """ -----------------------------------------------------------------------------------
    * Given the page content & URL, processes the html.
    * Returns True if all URLS on the page should be extracted, False otherwise.
    * --------------------------------------------------------------------------------- """
    def process(self, page, url):
        # Forum
        if issubclass(self.webpage.__class__, WebAbstractClass.WebpageAbstractClass):
            # Thread page
            if self.webpage.get_general_page_url() in url:
                if self.important_thread(page):
                    self.thread_page_handler(page, url)
                    return True
                return False

            # Profile page
            if self.webpage.get_general_profile_url() in url:
                self.profile_page_handler(page)
            return True

        # Marketplace
        elif issubclass(self.webpage.__class__, MarketPlaceABC.MarketPlaceABC):
            if self.webpage.get_general_page_url() in url:
                self.item_page_handler(page, url)
                return False
        return True

    #############################################################################################################
    ############################################## FORUM HANDLERS ###############################################
    #############################################################################################################

    """ -----------------------------------------------------------------------------------
    * Extracts the comments and commenter from the page while storing it
    * --------------------------------------------------------------------------------- """
    def thread_page_handler(self, page, url):
        soup = BeautifulSoup(page, 'html.parser', from_encoding='utf-8')
        self.crawler_stats["Threads seen"] += 1
        block_list = soup.find_all(**self.webpage.block_regex())
        for block in block_list:
            user_link = None
            name = None

            for profile in block.find_all(**self.webpage.profile_regex()):
                # Get the html username & profile link
                user_name = profile.find(**self.webpage.profile_name_regex())
                user_link = profile.find(**self.webpage.profile_link_regex())

                if user_name and user_link is not None:
                    name = pretty(user_name.text)

                    # Hashing name if anonymous is active
                    if self.anonymous:
                        name = str(abs(hash(name)) % (10 ** 8))
                        user_link = NOT_FOUND
                    break

            if block.find(**self.webpage.comment_regex()) is None:
                continue

            comment = pretty(block.find(**self.webpage.comment_regex()).get_text())
            date = dparser.parse(block.find(**self.webpage.date_regex()).text,fuzzy=True).strftime("%d %b, %Y")

            # Creating a new Person & their comment (if person already exists then just adding the comment)
            if name is not None and user_link is not None:
                # Existing User
                if name in self.people and comment not in self.people[name].get_all_comments():
                    self.people[name].add_comment(comment, str(soup.find(**self.webpage.thread_name_regex()).text), url, date)
                # New User
                else:
                    if user_link == NOT_FOUND :
                        user_link_href = NOT_FOUND
                    else :
                        user_link_href = user_link['href']

                    if user_link_href.startswith('./'):
                        user_link_href = self.webpage.root_page_url + user_link_href[2:]

                    person = UserInfo(name, user_link_href)
                    person.add_comment(comment, str(soup.find(**self.webpage.thread_name_regex()).text), url, date)
                    self.people[name] = person

        for link in self.direct_crawler():
            self.crawler_stats["Profiles scraped"] += 1
            if link != NOT_FOUND :
                self.process(str(requests.get(link).text.encode('utf-8')), link)

    """
        Extracts the attributes of the commenter 
    """

    def profile_page_handler(self, page):
        soup = BeautifulSoup(page, 'html.parser')
        username = soup.find(**self.webpage.attributes_regex()['username'])
        if username is None:
            return
        username = username.get_text()
        if self.anonymous:
            # Hashing name if anonymous is active
            username = str(abs(hash(username)) % (10 ** 8))
        if username not in self.people:
            return
        for name, regex in self.webpage.attributes_regex().items():
            for data in soup.find_all(**regex):
                self.people[username].add_attribute(name, data.get_text())

    """
        Determines if the thread is something we want to keep looking at
    """

    def important_thread(self, page):
        soup = BeautifulSoup(page, 'html.parser')
        title = soup.find(**self.webpage.thread_name_regex())
        if title is None:
            return True

        return self.thread_model.accept(title.text)

    #############################################################################################################
    ######################################### MARKETPLACE HANDLERS ##############################################
    # This is a hack solution for the marketplace stuff, not really the best approach but the crawler was not
    # designed for marketplaces. A whole refactor of the code would take way too long and honestly I just dont
    # think that it is worth it
    #############################################################################################################
    #############################################################################################################

    def item_page_handler(self, page, url):
        #print("On item page")
        soup = BeautifulSoup(page, 'html.parser', from_encoding='utf-8')
        item_name = soup.find(**self.webpage.sale_item_name_regex())

        seller_block = soup.find(**self.webpage.seller_block_regex())

        seller_url = seller_block.find(**self.webpage.seller_url_regex())
        name = seller_block.find(**self.webpage.seller_name_regex())
        seller_description = soup.find(**self.webpage.seller_description_regex())

        date = soup.find(**self.webpage.date_regex())
        if date is None or self.webpage.date_regex() == {}:
            date = NOT_FOUND
        else:
            date = pretty(date.text)

        price_block = soup.find(**self.webpage.price_regex())
        price = pretty(price_block.get_text())

        if item_name is not None:

            if name is None:
                name = NOT_FOUND
            else:
                name = pretty(name.get_text())
                # Hashing name if anonymous is active
                if self.anonymous:
                    name = str(abs(hash(name)) % (10 ** 8))

            if seller_description is None:
                text = NOT_FOUND
            else:
                if self.webpage.root_page_url == "https://www.ebay.com/":
                    text = pretty(BeautifulSoup(requests.get(seller_description["src"]).content, "html.parser").get_text())
                else:
                    text = pretty(seller_description.get_text())

            if seller_url is None or self.webpage.seller_url_regex() == {} or self.anonymous:
                seller_url = NOT_FOUND
            else:
                seller_url = seller_url['href']

            if name in self.people:
                self.people[name].add_item(url, text, date, price, pretty(item_name.get_text()))
                for n, regex in self.webpage.attributes_regex().items():
                    for data in soup.find_all(**regex):
                        self.people[name].add_attribute(n, pretty(data.get_text()))
            else:

                person = SellerInfo(name, seller_url)
                person.add_item(url, text, date, price, pretty(item_name.get_text()))
                self.people[name] = person
                for n, regex in self.webpage.attributes_regex().items():
                    for data in soup.find_all(**regex):
                        self.people[name].add_attribute(n, pretty(data.get_text()))

        self.direct_crawler()

    """
        Function identifying the interesting people
    """

    def direct_crawler(self):
        profile_links = []
        for username, person in self.people.items():
            if username in self.interesting_people:
                continue
            else:
                if self.comment_model.accept(person.get_all_comments()):
                    logging.info("INTERESTING USER: " + str(username))
                    logging.info("URL: " + str(person.get_profile_url()))
                    if person.get_profile_url() != NOT_FOUND :
                        profile_links.append(person.get_profile_url())
                    self.interesting_people.append(username)
                    self.finish()
                    logging.info('*** Saved ***')

        return profile_links

    """
        Finished crawling
    """

    def finish(self):

        import datetime
        exported_data = {}
        for person in self.interesting_people:
            comments = self.people[person].comments
            if self.filter_comments:
                filtered = {}
                for thread, com_dict_list in comments.items():

                    filtered_comments = []
                    for comment in com_dict_list:
                        if self.comment_model.accept(comment["comment"]):
                            filtered_comments.append(comment)
                    if len(filtered_comments) == 0:
                        continue

                    filtered[thread] = filtered_comments
                comments = filtered

            exported_data[person] = {
                **{
                    "exported_date": datetime.date.today().isoformat(),
                    "username": person,
                    "comments": comments,
                    "profile_url": self.people[person].get_profile_url()
                }, **self.people[person].attributes}

        import json
        with open('..' + os.sep + 'crawler' + os.sep + 'exported_users' + os.sep + 'interesting_users_' + self.webpage.name + '.json', 'w') as fp:
            json.dump(exported_data, fp)

        self.csv_export(exported_data)


    def csv_export(self, exported_data):
        import pandas
        csv_export = {"user": [], "comment": [], "thread_url": [], "profile_link": [], "thread_title": [], "date": []}
        ners = []

        if issubclass(self.webpage.__class__, MarketPlaceABC.MarketPlaceABC):
            csv_export["price"] = []
            csv_export["description"] = []

        ######### CUSTOM NERS ##########
        path = '..' + os.sep + 'crawler' + os.sep + 'web_director' + os.sep + 'lexicon'
        for file in self.comment_keyword_names:
            res = file.replace(".txt", "").replace("_", " ").title().replace(" ", "")
            csv_export["NER-" + res] = []
            ners.append("NER-" + res)
        ################################

        for k, v in exported_data.items():
            for url, comments in exported_data[k]["comments"].items():
                for comment in comments:

                    csv_export["user"].append(k)
                    csv_export["comment"].append(comment["comment"])
                    csv_export["thread_url"].append(url)
                    csv_export["profile_link"].append(exported_data[k]["profile_url"])
                    csv_export["date"].append(comment["date"])
                    csv_export["thread_title"].append(comment["thread"])

                    path = '..' + os.sep + 'crawler' + os.sep + 'web_director' + os.sep + 'lexicon'

                    for file in self.comment_keyword_names:
                        regex = read_txt(path + os.sep + file)
                        ner_tags = []
                        res = file.replace(".txt", "").replace("_", " ").title().replace(" ", "")
                        for words in re.findall(regex, comment["comment"]):
                            ner_tags.append("NER-" + res + ":" + str(words))

                        csv_export["NER-" + res].append(ner_tags)
                    ################################

                    if issubclass(self.webpage.__class__, MarketPlaceABC.MarketPlaceABC):
                        csv_export["price"].append(comment["price"])
                        csv_export["description"].append(comment["description"])

        if issubclass(self.webpage.__class__, MarketPlaceABC.MarketPlaceABC):
            csv_export.pop("thread_title")
            csv_export["item"] = csv_export.pop("comment")
            csv_export["item_url"] = csv_export.pop("thread_url")

        df = pandas.DataFrame(csv_export)

        # Reordering cols
        if issubclass(self.webpage.__class__, MarketPlaceABC.MarketPlaceABC):
            df = df[["item", "price", "description", "item_url", "user", "profile_link", "date"] + ners]
        else:
            df = df[["comment", "thread_title", "thread_url", "user", "profile_link", "date"] + ners]

        # Drop col if not found at all
        for i in csv_export:
            not_found = all(element == NOT_FOUND for element in csv_export[i])
            if not_found: df = df.drop(i, axis=1)

        df.to_csv('..' + os.sep + 'crawler' + os.sep + 'exported_users' + os.sep + 'interesting_users_' + self.webpage.name + '.csv')

def pretty(s):
    import re
    import demoji

    s = demoji.replace_with_desc(str(s))
    s = re.sub(r'[^\x00-\x7f]', r'', s)

    return re.sub(' +', ' ', s.replace('\n', ' ').replace('\r', '').replace('\t', '')).rstrip().lstrip()

def url_fixer(string):
    if string[0] != "/":
        if str(string[0]).isalpha():
            return "/" + string
        else:
            return url_fixer(string[1:])
    else:
        return string


def chunks(l, n):
    if n == 0:
        n = 1
    # For item i in a range that is a length of l,
    for i in range(0, len(l), n):
        # Create an index range for l of n items:
        yield l[i:i + n]


def read_txt(path):
    regex = r"(?i).*"
    with open(path, encoding='utf-8') as f:
        lines = f.readlines()
        for i in range(0, len(lines)):
            if i == 0:
                regex += r"(\b" + lines[i].strip() + r"\b"
            else:
                regex += r"|\b" + lines[i].strip() + r"\b"
        regex += r").*"
    return regex
