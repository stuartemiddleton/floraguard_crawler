from web_director.abc import ModelAbstractClass


class AllModel(ModelAbstractClass.ModelABC):

    def accept(self, ignored):
        return True
