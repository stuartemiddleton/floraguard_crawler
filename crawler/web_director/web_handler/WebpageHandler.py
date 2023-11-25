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
import datetime
from web_director.user.Seller import SellerInfo
from web_director.user.User import UserInfo
from web_director.abc import MarketPlaceABC, WebAbstractClass
#import pandas
import codecs, json

NOT_FOUND = 'NOT FOUND'

#Default values
DEFAULT_SAVE_FILE = "interesting_users"
DEFAULT_USER_COMMENT_LIMIT = 100

class WebpageHandler:

    def __init__(self, webpage, thread_model, comment_model, comment_keyword_names, filter_comments, anonymous, **kargs):
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
        self.save_location = kargs["resource_location"]["save_file_location"]
        self.webpage_config_location = kargs["resource_location"]["webpage_location"]
        self.lexicon_config_location = kargs["resource_location"]["lexicon_location"]
        self.save_file_name = kargs["save_file_name"] if kargs["save_file_name"] != None else DEFAULT_SAVE_FILE
        self.user_comment_limit = kargs["user_comment_limit"] if kargs["user_comment_limit"] != None else DEFAULT_USER_COMMENT_LIMIT
        if self.webpage.timeout_hours != None :
            self.timeout_hours = datetime.datetime.utcnow() + datetime.timedelta( hours=self.webpage.timeout_hours )
        else :
            self.timeout_hours = None
        logging.info('*** crawl webpage handler init - timeout ' + str(self.timeout_hours) + ' ***')


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

                #logging.info( 'BLOCK USER_NAME == ' + repr(user_name) )
                #logging.info( 'BLOCK USER_NAME text == ' + repr(user_name.text) )
                #logging.info( 'BLOCK USER_LINK == ' + repr(user_link) )

                if user_name is not None:
                    name = pretty(user_name.text)

                if user_link is not None:
                    # stop if we get a username and a link, otherwise keep looking in block in case there is another better entry
                    break

            if user_link == None :
                user_link = NOT_FOUND

            # Hashing name if anonymous is active
            if self.anonymous == True :
                name = str(abs(hash(name)) % (10 ** 8))
                user_link = NOT_FOUND

            if block.find(**self.webpage.comment_regex()) is None:
                #logging.info( 'NUM COMMENTS = 0' )
                continue

            comment = pretty(block.find(**self.webpage.comment_regex()).get_text())
            date = dparser.parse(block.find(**self.webpage.date_regex()).text,fuzzy=True).strftime("%d %b, %Y")

            #if 'test post for Red unicorn' in comment :
            #    logging.info( 'COMMENT == ' + repr(comment) )
            #    logging.info( 'NAME == ' + repr(name) )
            #    logging.info( 'USER_LINK == ' + repr(user_link) )

            # Creating a new Person & their comment (if person already exists then just adding the comment)
            # note: if name is not found (e.g. profile regex not setup) then the whole comment will be ignored
            if name is not None and user_link is not None:

                #Existing user and comment
                if (name in self.people) and (comment in self.people[name].get_all_comments()):
                    continue
                # Existing User but new comment
                elif (name in self.people) and (comment not in self.people[name].get_all_comments()):
                    self.people[name].add_comment(comment, str(soup.find(**self.webpage.thread_name_regex()).text), url, date, note="Existing User")
                    #if 'test post for Red unicorn' in comment :
                    #    logging.info( 'NEW PERSON == ' + repr(self.people[name]) )

                # New User
                else:
                    if user_link == NOT_FOUND :
                        user_link_href = NOT_FOUND
                    else :
                        user_link_href = user_link['href']

                    if user_link_href.startswith('./'):
                        user_link_href = self.webpage.root_page_url + user_link_href[2:]

                    person = UserInfo(name, user_link_href, comment_limit=self.user_comment_limit)
                    person.add_comment(comment, str(soup.find(**self.webpage.thread_name_regex()).text), url, date, note="New User")
                    self.people[name] = person
                    #if 'test post for Red unicorn' in comment :
                    #    logging.info( 'EXISTING PERSON == ' + repr(self.people[name]) )

        for link in self.direct_crawler():
            self.crawler_stats["Profiles scraped"] += 1
            if link != NOT_FOUND :
                self.process(str(requests.get(link).text.encode('utf-8')), link)


        self.finish()
        logging.info('*** Saved ***')

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

        self.finish()
        logging.info('*** Saved ***')

    """
        Function identifying the interesting people (profile page links)
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
                    logging.info("COMMENTS: " + repr(person.get_all_comments()))
                    if person.get_profile_url() != NOT_FOUND :
                        profile_links.append(person.get_profile_url())
                    self.interesting_people.append(username)

        return profile_links

    """
        Finished crawling
        dump results so far, overwriting existing results, so if crawl is long and fails we still have something serialized
    """

    def finish(self):

        #import datetime
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

        #
        # codec file handle for serializing json (old code prob ok but this is consistent with csv code now)
        #        
        str_filename = self.save_location + os.sep + self.save_file_name + '_' + self.webpage.name + '.json'
        write_handle = codecs.open( str_filename, 'w', 'utf-8', errors = 'replace' )
        write_handle.write( json.dumps(exported_data) + '\n' )
        write_handle.close()

        '''
        import json
        with open('..' + os.sep + 'crawler' + os.sep + 'exported_users' + os.sep + 'interesting_users_' + self.webpage.name + '.json', 'w') as fp:
            json.dump(exported_data, fp)
        '''

        self.csv_export(exported_data)

    def csv_export(self, exported_data):

        csv_export = {"user": [], "comment": [], "thread_url": [], "profile_link": [], "thread_title": [], "date": []}
        ners = []

        if issubclass(self.webpage.__class__, MarketPlaceABC.MarketPlaceABC):
            csv_export["price"] = []
            csv_export["description"] = []

        ######### CUSTOM NERS ##########
        path = self.lexicon_config_location
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

                    path = self.lexicon_config_location

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

        #
        # CSV serialization tab delimited code using codecs (to ensure upper range UTF-8 characters like emojis are serialized correctly)
        #
        str_filename = self.save_location + os.sep + self.save_file_name + '_' + self.webpage.name + '.csv'
        str_filename_encoded = self.save_location + os.sep + self.save_file_name + '_' + self.webpage.name + '.encoded.csv'
        write_handle = codecs.open( str_filename, 'w', 'utf-8', errors = 'replace' )
        write_handle_encoded = codecs.open( str_filename_encoded, 'w', 'utf-8', errors = 'replace' )

        list_keys = list( csv_export.keys() )

        # header row
        write_handle.write( '#' )
        write_handle_encoded.write( '#' )
        for key in list_keys :
            write_handle.write( key )
            write_handle_encoded.write( key )
            if key != list_keys[-1] :
                write_handle.write( '\t' )
                write_handle_encoded.write( '\t' )
        write_handle.write( '\n' )
        write_handle_encoded.write( '\n' )

        # data rows (one per post/comment)
        for i in range(len(csv_export[list_keys[0]])) :
            for key in list_keys :
                element = csv_export[key][i]
                if element != NOT_FOUND :
                    # use json encoded strings to escape (a) newlines and tabs and (b) upper range UTF-8 entries
                    # dont bother with the "" as these are all strings
                    str_entry = json.dumps( element )
                    write_handle_encoded.write( str_entry[1:-1] )

                    # unencoded dump (potentially unsafe)
                    if isinstance( element, str ) :
                        write_handle.write( element.replace('\t',' ').replace('\n',' ') )
                    else :
                        write_handle.write( str_entry[1:-1] )

                if key != list_keys[-1] :
                    write_handle.write( '\t' )
                    write_handle_encoded.write( '\t' )
            write_handle.write( '\n' )
            write_handle_encoded.write( '\n' )
        write_handle.close()
        write_handle_encoded.close()
        
        '''
        # OLD PANDAS CSV serialization code
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
        '''

def pretty(s):
    return s
'''
    # removed all pretty printing and emoji removal as its not needed or wanted
    import re
    import demoji

    s = demoji.replace_with_desc(str(s))
    s = re.sub(r'[^\x00-\x7f]', r'', s)

    return re.sub(' +', ' ', s.replace('\n', ' ').replace('\r', '').replace('\t', '')).rstrip().lstrip()
'''

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
