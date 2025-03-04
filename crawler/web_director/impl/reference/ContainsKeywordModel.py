from web_director.abc import ModelAbstractClass
import re

class ContainsKeywordModel(ModelAbstractClass.ModelABC):

    def __init__(self, regex, comment_length):
        self.regex = regex
        self.comment_length = comment_length

    def accept(self, text):
        if type(text) is list:
            if len(text) < self.comment_length:
                return False
            for comment in text:
                if re.search(self.regex, comment):
                    return True
            return False
        if re.search(self.regex, text):
            return True
        return False


