from crawler.web_director.abc import WebAbstractClass


class StackOverFlowWebpage(WebAbstractClass.WebpageAbstractClass):

    def __init__(self):
        self.root_page_url = "https://politics.stackexchange.com"

    def get_root_page_url(self):
        return self.root_page_url

    def get_general_start_page_url(self):
        return self.root_page_url + "/questions"

    def get_general_page_url(self):
        return self.root_page_url + "/questions"

    def get_general_profile_url(self):
        return self.root_page_url + "/users"

    def block_regex(self):
        regex = {
            'name': 'div',
            'class_': "post-layout"
        }
        return regex

    def comment_regex(self):
        regex = {
            'name': 'div',
            'class_': "s-prose js-post-body"
        }
        return regex

    def profile_regex(self):
        regex = {
            'name': 'div',
            'class_': "user-details"
        }
        return regex

    def profile_name_regex(self):
        regex = {
            'name': 'span',
            'class_': "d-none"
        }
        return regex

    def profile_link_regex(self):
        regex = {
            'name': 'a',
            'href': True
        }
        return regex

    def attributes_regex(self):
        all_regex = {"username": {'name': 'div', 'class_': 'grid--cell fw-bold'},
                     "bio": {'name': 'div', 'class_': 'grid--cell mt16 s-prose profile-user--bio'},
                     "top tags": {'name': 'a', 'class_': 'post-tag'},
                     "supporting information": {'name': 'div', 'class_': 'grid gs8 gsx ai-center'}
                     }
        return all_regex