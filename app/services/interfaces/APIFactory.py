import abc


class APIFactory(abc.ABC):

    @abc.abstractmethod
    def queryApiByCharacter(self, characterName: str):
        pass

    @abc.abstractmethod
    def queryApiByComicId(self, comicId: str):
        pass
