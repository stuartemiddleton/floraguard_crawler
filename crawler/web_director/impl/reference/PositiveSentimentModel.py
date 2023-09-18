from web_director.abc import ModelAbstractClass

import re
import stanza


class CommentsPositiveSentiment(ModelAbstractClass.ModelABC):

    def __init__(self, comment_length):
        self.nlp = stanza.Pipeline(lang='en', processors='tokenize,sentiment')
        self.comment_length = comment_length

    def accept(self, comments):
        if len(comments) < self.comment_length:
            return False
        comments_no_urls = [remove_url(x) for x in comments]
        sentiment = 0
        for comment in comments_no_urls:
            processed = self.nlp(comment).sentences
            for sentence in processed:
                # Negative sentiment is -1, neutral is 0, positive is 1
                sentiment = (sentence.sentiment - 1)

        # All comments return a positive sentiment
        return sentiment > 0


def remove_url(txt):
    return " ".join(re.sub("([^0-9A-Za-z \t])|(\w+:\/\/\S+)", "", txt).split())