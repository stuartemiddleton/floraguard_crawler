from crawler.web_director.abc import ModelAbstractClass


class CustomModel(ModelAbstractClass.ModelABC):

    def __init__(self, model, acceptance):
        self.acceptance = acceptance
        self.model = model

    def accept(self, comments):
        return self.acceptance(self.model.predict(comments))
