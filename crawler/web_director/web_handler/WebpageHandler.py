import requests

from bs4 import BeautifulSoup

from web_director.user.Seller import SellerInfo
from web_director.user.User import UserInfo
from web_director.abc import MarketPlaceABC, WebAbstractClass


class WebpageHandler:

    def __init__(self, webpage, thread_model, comment_model, filter_comments, anonymous):
        if anonymous:
            print("Anonymous crawling active")
        self.crawler_stats = {"Threads seen": 0, "Profiles scraped": 0}
        self.webpage = webpage
        self.thread_model = thread_model
        self.comment_model = comment_model
        self.people = {}
        self.interesting_people = []
        self.anonymous = anonymous
        self.filter_comments = filter_comments

    """
        Given the page content, processes the html
        Returns True or False if it should extract all the URLS on that page
    """

    def process(self, page, url):
        if issubclass(self.webpage.__class__, WebAbstractClass.WebpageAbstractClass):
            if self.webpage.get_general_page_url() in url:
                if self.important_thread(page):
                    self.thread_page_handler(page, url)
                    return True
                return False

            if self.webpage.get_general_profile_url() in url:
                self.profile_page_handler(page)

            return True
        elif issubclass(self.webpage.__class__, MarketPlaceABC.MarketPlaceABC):
            if self.webpage.get_general_page_url() in url:
                self.item_page_handler(page, url)
                return False
        return True

    ######################################### FORUM HANDLERS ####################################################
    """
        Extracts the comments and commenter from the page while storing it
    """

    def thread_page_handler(self, page, url):
        soup = BeautifulSoup(page, 'html.parser')
        self.crawler_stats["Threads seen"] += 1
        block_list = soup.find_all(**self.webpage.block_regex())
        print("On page, block amount", len(block_list))
        for block in block_list:
            user_link = None
            name = None

            for profile in block.find_all(**self.webpage.profile_regex()):
                user_name = profile.find(**self.webpage.profile_name_regex())
                user_link = profile.find(**self.webpage.profile_link_regex())
                if user_name and user_link is not None:
                    name = user_name.text
                    if self.anonymous:
                        # Hashing name if anonymous is active
                        name = str(abs(hash(name)) % (10 ** 8))
                    break
            comment = block.find(**self.webpage.comment_regex()).get_text()
            date = block.find(**self.webpage.date_regex()).get_text()
            if name is not None and user_link is not None:
                if name in self.people:
                    self.people[name].add_comment(pretty(comment),
                                                  soup.find(**self.webpage.thread_name_regex()).text, url, date)
                else:
                    person = UserInfo(name, url_fixer(user_link['href']))
                    person.add_comment(pretty(comment), soup.find(**self.webpage.thread_name_regex()).text, url, date)
                    self.people[name] = person

        for link in self.direct_crawler():
            self.crawler_stats["Profiles scraped"] += 1
            self.process(requests.get(link).text, link)

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
        interesting = self.thread_model.accept(title.text)
        return interesting

    ######################################### MARKETPLACE HANDLERS ####################################################
    # This is a hack solution for the marketplace stuff, not really the best approach but the crawler was not
    # designed for marketplaces. A whole refactor of the code would take way too long and honestly I just dont
    # think that it is worth it

    def item_page_handler(self, page, url):
        print("On item page")
        soup = BeautifulSoup(page, 'html.parser')
        item_name = soup.find(**self.webpage.sale_item_name_regex())

        seller_block = soup.find(**self.webpage.seller_block_regex())
        if seller_block is None:
            return

        print("Found seller block")
        seller_url = seller_block.find(**self.webpage.seller_url_regex())
        name = seller_block.find(**self.webpage.seller_name_regex())
        seller_description = soup.find(**self.webpage.seller_description_regex())
        date = pretty(soup.find(**self.webpage.date_regex()).text)
        price = pretty(soup.find(**self.webpage.price_regex()).text)
        if item_name is not None:
            print("Item: " + pretty(item_name.get_text()))

            if name is None:
                name = "NOT FOUND"
            else:
                name = pretty(name.get_text())
            if seller_description is None:
                text = "{Cant find}"
            else:
                text = pretty(seller_description.get_text())

            if seller_url is None:
                seller_url = {'href': "NOT FOUND"}

            print("Seller name: " + name)
            # print("Seller url: " + seller_url['href'])
            print("Seller decr: " + pretty(text))

            if name in self.people:
                self.people[name].add_item(url, pretty(text), date, price, pretty(item_name.get_text()))
                for n, regex in self.webpage.attributes_regex().items():
                    for data in soup.find_all(**regex):
                        self.people[name].add_attribute(n, data.get_text())
            else:
                person = SellerInfo(name, url_fixer(seller_url['href']))
                person.add_item(url, pretty(text), date, price, pretty(item_name.get_text()))
                self.people[name] = person
                for n, regex in self.webpage.attributes_regex().items():
                    for data in soup.find_all(**regex):
                        self.people[name].add_attribute(n, data.get_text())

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
                    print(username)
                    print("INTERESTING USER: " + username)
                    profile_links.append(self.webpage.root_page_url + person.get_profile_url())
                    self.interesting_people.append(username)
                    self.finish()

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
                    "profile_url": self.webpage.root_page_url + self.people[person].get_profile_url()
                }, **self.people[person].attributes}

        import json
        print(exported_data)
        with open(r'..\crawler\exported_users\interesting_users_' + self.webpage.name + '.json', 'w') as fp:
            json.dump(exported_data, fp)

        self.csv_export(exported_data)

        print(self.interesting_people)
        print(self.crawler_stats)

    def csv_export(self, exported_data):
        import pandas
        csv_export = {"user": [], "comment": [], "thread_url": [], "profile_link": [], "thread_title": [], "date": []}
        if issubclass(self.webpage.__class__, MarketPlaceABC.MarketPlaceABC):
            csv_export["price"] = []
            csv_export["description"] = []

        for k, v in exported_data.items():
            for url, comments in exported_data[k]["comments"].items():
                for comment in comments:
                    csv_export["user"].append(k)
                    csv_export["comment"].append(comment["comment"])
                    csv_export["thread_url"].append(url)
                    csv_export["profile_link"].append(exported_data[k]["profile_url"])
                    csv_export["date"].append(comment["date"])
                    csv_export["thread_title"].append(comment["thread"])
                    if issubclass(self.webpage.__class__, MarketPlaceABC.MarketPlaceABC):
                        csv_export["price"].append(comment["price"])
                        csv_export["description"].append(comment["description"])

        df = pandas.DataFrame(csv_export)
        df.to_csv(r'..\crawler\exported_users\interesting_users_' + self.webpage.name + '.csv')


def pretty(string):
    import re
    return re.sub(' +', ' ', string.replace('\n', ' ').replace('\r', '').replace('\t', '')).rstrip().lstrip()


def url_fixer(string):
    if string[0] is not "/":
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
