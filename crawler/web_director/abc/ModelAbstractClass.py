from abc import ABC, abstractmethod


class ModelABC(ABC):

    @abstractmethod
    def accept(self, comments):
        pass
