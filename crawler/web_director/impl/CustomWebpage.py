from web_director.abc import WebAbstractClass


class CustomWebpage(WebAbstractClass.WebpageAbstractClass):

    def __init__(self, name, anonymous):
        self.name = name
        self.anonymous = anonymous
        self.root_page_url = ""
        self.general_profile_url = ""
        self.general_threads_page_url = ""
        self.general_thread_url = ""
        self._thread_name_regex = {}
        self._block_regex = {}
        self._comment_regex = {}
        self._profile_regex = {}
        self._profile_name_regex = {}
        self._profile_link_regex = {}
        self._attributes_regex = {}

    def get_root_page_url(self):
        return self.root_page_url

    def get_general_threads_page_url(self):
        return self.general_threads_page_url

    def get_general_thread_url(self):
        return self.general_thread_url

    def get_general_profile_url(self):
        return self.general_profile_url

    def thread_name_regex(self):
        return self._thread_name_regex

    def block_regex(self):
        return self._block_regex

    def comment_regex(self):
        return self._comment_regex

    def profile_regex(self):
        return self._profile_regex

    def profile_name_regex(self):
        return self._profile_name_regex

    def profile_link_regex(self):
        return self._profile_link_regex

    def attributes_regex(self):
        return self._attributes_regex
