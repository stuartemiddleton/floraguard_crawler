from crawler.web_director.abc import ModelAbstractClass
import re

class ThreadContainsKeywordModel(ModelAbstractClass.ModelABC):

    def __init__(self, regex):
        self.regex = regex

    def accept(self, title):
        if re.match(self.regex, title):
            print("INTERESTING")
            print(title)
        return re.match(self.regex, title)
