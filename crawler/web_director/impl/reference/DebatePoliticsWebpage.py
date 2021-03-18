from crawler.web_director.abc import WebAbstractClass


class DebatePoliticsWebpage(WebAbstractClass.WebpageAbstractClass):

    def __init__(self):
        self.root_page_url = "https://debatepolitics.com"

    def get_root_page_url(self):
        return self.root_page_url

    def get_general_start_page_url(self):
        return self.root_page_url + "/whats-new/posts/295247/"

    def get_general_page_url(self):
        return self.root_page_url + "/threads"

    def get_general_profile_url(self):
        return self.root_page_url + "/members"

    def block_regex(self):
        regex = {
            'name': 'article',
            'class_': "message message--post js-post js-inlineModContainer"
        }
        return regex

    def comment_regex(self):
        regex = {
            'name': 'div',
            'class_': "bbWrapper"
        }
        return regex

    def profile_regex(self):
        regex = {
            'name': 'div',
            'class_': "message-cell message-cell--user"
        }
        return regex

    def profile_name_regex(self):
        regex = {
            'name': 'h4',
            'class_': "message-name"
        }
        return regex

    def profile_link_regex(self):
        regex = {
            'name': 'a',
            'href': True
        }
        return regex

    def attributes_regex(self):
        all_regex = {"username": {'name': 'span', 'class_': 'username'},
                     "userTitle": {'name': 'span', 'class_': 'userTitle'},
                     "supporting information" : {'name' : 'dl', 'class_' : 'pairs pairs--columns pairs--fixedSmall'}
                     }
        return all_regex
