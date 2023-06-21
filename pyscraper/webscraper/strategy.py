from abc import abstractmethod

class ScrapeStrategy():

    @abstractmethod
    def get(self):
        pass
    