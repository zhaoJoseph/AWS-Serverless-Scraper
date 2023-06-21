from abc import abstractmethod

class ApiScraper():

    @abstractmethod
    def get(self):
        pass
    
    @abstractmethod
    def collect(self, data):
        pass