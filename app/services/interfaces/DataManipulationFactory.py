import abc

from models.Character import Character
from services.interfaces.APIFactory import APIFactory


class DataManipulationFactory(abc.ABC):

    @abc.abstractmethod
    def getCharacterMetadataByName(
            self,
            characterName: str,
            apiFactory: APIFactory):
        pass

    @abc.abstractmethod
    def getCharactersFromComicId(self, comicId: str, apiFactory: APIFactory):
        pass

    def extractCharacterMetadata(self, metadata) -> Character:
        name = metadata.name if metadata.name else "Character name not found."
        id = metadata.id if metadata.id else "Character ID not found."
        description = metadata.description if metadata.description else "Character description not found."
        thumbnailPath = metadata.thumbnail.path
        thumbnailExtension = metadata.thumbnail.extension
        thumbnail = ".".join([metadata.thumbnail.path, metadata.thumbnail.extension]) if (
            thumbnailPath and thumbnailExtension) else "Character thumbnail not found."
        comics = metadata.comics.items

        return Character(name, id, description, thumbnail, comics)
