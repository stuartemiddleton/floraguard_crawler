from crawler.web_director.abc import WebAbstractClass


class PoliticalForumWebpage(WebAbstractClass.WebpageAbstractClass):

    def __init__(self):
        self.root_page_url = "http://www.politicsforum.org"

    def get_root_page_url(self):
        return self.root_page_url + "/forum"

    def get_general_threads_page_url(self):
        return self.root_page_url + "/forum"

    def get_general_thread_url(self):
        return self.root_page_url + "/forum/viewtopic.php"

    def get_general_profile_url(self):
        return self.root_page_url + "/forum/memberlist.php"

    def block_regex(self):
        regex = {
            'name': 'div',
            'class_': "panel forum-answer"
        }
        return regex

    def comment_regex(self):
        regex = {
            'name': 'div',
            'class_': "content"
        }
        return regex

    def profile_regex(self):
        regex = {
            'name': 'div',
            'class_': "panel-heading"
        }
        return regex

    def profile_name_regex(self):
        regex = {
            'name': 'a',
            'class_': "username"
        }
        return regex

    def profile_link_regex(self):
        regex = {
            'name': 'a',
            'class_': "username"
        }
        return regex

    def attributes_regex(self):
        all_regex = {"username": {'name': 'span', 'class_': 'username'}}
        return all_regex
