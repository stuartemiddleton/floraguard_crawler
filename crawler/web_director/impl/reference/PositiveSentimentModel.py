from crawler.web_director.abc import ModelAbstractClass

import re
from textblob import TextBlob


class CommentsPositiveSentiment(ModelAbstractClass.ModelABC):

    def accept(self, comments):
        if len(comments) < 15:
            return False
        comments_no_urls = [remove_url(x) for x in comments]
        sentiment_objects = [TextBlob(comment) for comment in comments_no_urls]
        positive, negative = 0,0
        for x in sentiment_objects:
            if x.polarity > 0:
                positive+=1
            else:
                negative+=1
        print("POSITIVE COMMENTS:", positive ,"NEGATIVE COMMENTS:",negative)
        return positive > negative


def remove_url(txt):
    return " ".join(re.sub("([^0-9A-Za-z \t])|(\w+:\/\/\S+)", "", txt).split())