from web_director.abc import ModelAbstractClass
import re

class ContainsKeywordModel(ModelAbstractClass.ModelABC):

    def __init__(self, regex):
        self.regex = regex

    def accept(self, text):
        if type(text) is list:
            for comment in text:
                print(comment,self.regex,re.match(self.regex, comment))
                if re.match(self.regex, comment):
                    print("Interesting User")
                    return True
            return False
        if re.match(self.regex, text):
            print("INTERESTING")
            print(text)
            return True
        return False
