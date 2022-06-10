import csv

from logger.Logger import Logger
from models.Character import Character
from services.interfaces.CacheFactory import CacheFactory


class InMemoryCacheService(CacheFactory):
    def __init__(self):
        self.characterCache = {}

    def addCharacterToCache(self, character: Character):
        self.characterCache[character.id] = {
            "name": character.name,
            "description": character.description,
            "thumbnail": character.thumbnail,
            "comics": character.comics
        }

    def writeCacheToCsv(self, csvFile: str):
        csvColumns = ["id", "name", "description", "thumbnail"]
        dictData = []
        for characterId in self.characterCache:
            dictData.append({"id": characterId,
                             "name": self.characterCache[characterId]["name"],
                             "description": self.characterCache[characterId]["description"],
                             "thumbnail": self.characterCache[characterId]["thumbnail"]})
        try:
            with open(csvFile, 'w') as file:
                writer = csv.DictWriter(file, fieldnames=csvColumns)
                writer.writeheader()
                for data in dictData:
                    writer.writerow(data)
        except IOError as ioe:
            Logger.logError(ioe)
