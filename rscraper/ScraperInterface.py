from abc import ABC, abstractmethod, abstractproperty


class ScraperInterface(ABC):

    @property
    def limit(self):
        pass

    @limit.setter
    def limit(self, value):
        """
        Type and Value checks
        """

        pass

    @abstractmethod
    def scrape(self):
        """
        Get the data
        """

        pass

    @abstractmethod
    def save_data(self):
        """
        Save to file
        """

        pass
