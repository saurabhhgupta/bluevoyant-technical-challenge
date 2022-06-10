import requests

from services.interfaces.APIFactory import APIFactory
from utilities.GenericUtilities import GenericUtilities
from utilities.EncryptionUtilities import EncryptionUtilities


class MarvelAPIService(APIFactory):

    def __init__(self):
        self.publicKey = GenericUtilities.getPublicKey()
        self.privateKey = GenericUtilities.getPrivateKey()

    def _generateDefaultQueryParameters(self):
        timestamp = GenericUtilities.getCurrentTime()
        return {"ts": timestamp,
                "apikey": self.publicKey,
                "hash": EncryptionUtilities.hashKeys(
                    timestamp,
                    self.privateKey,
                    self.publicKey
                )
                }

    def queryApiByCharacter(self, characterName: str):
        characterKeyValue = {"name": str(characterName)}
        queryParameters = {
            **self._generateDefaultQueryParameters(),
            **characterKeyValue}
        request = requests.get(
            "http://gateway.marvel.com/v1/public/characters",
            params=queryParameters)

        return request

    def queryApiByComicId(self, comicId: str):
        queryParameters = self._generateDefaultQueryParameters()
        request = requests.get(
            "http://gateway.marvel.com/v1/public/comics/{}/characters".format(comicId),
            params=queryParameters)

        return request
