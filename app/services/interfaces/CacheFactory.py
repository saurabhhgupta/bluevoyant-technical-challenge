import abc

from models.Character import Character


class CacheFactory(abc.ABC):

    @abc.abstractmethod
    def addCharacterToCache(self, character: Character):
        pass

    @abc.abstractmethod
    def writeCacheToCsv(self, csvFile: str):
        pass
