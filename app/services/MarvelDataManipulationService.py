import requests
import json

from types import SimpleNamespace

from logger.Logger import Logger
from models.Character import Character
from services.interfaces.DataManipulationFactory import DataManipulationFactory
from services.interfaces.APIFactory import APIFactory


class MarvelDataManipulationService(DataManipulationFactory):

    def getCharacterMetadataByName(
            self,
            characterName: str,
            apiFactory: APIFactory) -> Character:
        try:
            request = apiFactory.queryApiByCharacter(characterName)
        except Exception as e:
            Logger.logError(e)

        character = json.loads(
            request.text,
            object_hook=lambda d: SimpleNamespace(
                **d))
        metadata = character.data.results[0]

        return super().extractCharacterMetadata(metadata)

    def getCharactersFromComicId(self, comicId, apiFactory: APIFactory):
        try:
            request = apiFactory.queryApiByComicId(comicId)
        except Exception as e:
            Logger.logError(e)

        characters = json.loads(
            request.text,
            object_hook=lambda d: SimpleNamespace(
                **d))
        metadata = characters.data.results

        return metadata
