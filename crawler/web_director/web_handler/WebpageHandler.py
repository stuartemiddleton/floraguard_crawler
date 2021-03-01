import requests

from bs4 import BeautifulSoup

from crawler.web_director.user.User import UserInfo


class WebpageHandler:

    def __init__(self, webpage, thread_model, comment_model):
        self.crawler_stats = {"Threads seen": 0, "Profiles scraped": 0}
        self.webpage = webpage
        self.thread_model = thread_model
        self.comment_model = comment_model
        self.people = {}
        self.interesting_people = []

    """
        Given the page content, processes the html
    """

    def process(self, page, url):
        if self.webpage.get_general_thread_url() in url:
            if self.important_thread(page):
                self.thread_page_handler(page)
                return True
            return False

        if self.webpage.get_general_profile_url() in url:
            self.profile_page_handler(page)

        return True

    """
        Extracts the comments and commenter from the page while storing it
    """

    def thread_page_handler(self, page):
        soup = BeautifulSoup(page, 'html.parser')
        self.crawler_stats["Threads seen"] += 1
        block_list = soup.find_all(**self.webpage.block_regex())
        print("On page, block amount", len(block_list))
        for block in block_list:
            user_name = None
            user_link = None

            for profile in block.find_all(**self.webpage.profile_regex()):
                user_name = profile.find(**self.webpage.profile_name_regex())
                user_link = profile.find(**self.webpage.profile_link_regex())
                if user_name and user_link is not None:
                    break
            comment = block.find(**self.webpage.comment_regex()).get_text()
            if user_name is not None and user_link is not None:
                if user_name.text in self.people:
                    self.people[user_name.text].add_comment(pretty(comment),
                                                       soup.find(**self.webpage.thread_name_regex()).text)
                else:
                    person = UserInfo(user_name.text, url_fixer(user_link['href']))
                    person.add_comment(pretty(comment), soup.find(**self.webpage.thread_name_regex()).text)
                    self.people[user_name.text] = person

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
        if username not in self.people:
            return
        for name, regex in self.webpage.attributes_regex().items():
            for data in soup.find_all(**regex):
                self.people[username].add_attribute(name, data.get_text())

    def direct_crawler(self):
        profile_links = []
        for username, person in self.people.items():
            if username in self.interesting_people:
                continue
            else:
                if self.comment_model.accept(person.get_all_comments()):
                    print("INTERESTING USER: " + username)
                    profile_links.append(self.webpage.root_page_url + person.get_profile_url())
                    self.interesting_people.append(username)

        return profile_links

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

    """
        Finished crawling
    """

    def finish(self):

        import datetime
        exported_data = {}
        for person in self.interesting_people:
            exported_data[person] = {
                **{
                    "time-stamp": datetime.date.today().isoformat(),
                    "username": person,
                    "comments": self.people[person].comments,
                    "profile_url": self.webpage.root_page_url + self.people[person].get_profile_url()
                }, **self.people[person].attributes}

        import json
        with open(r'..\exported_users\interesting_users.json', 'w') as fp:
            json.dump(exported_data, fp)

        print(self.interesting_people)
        print(self.crawler_stats)


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
