import os
import sys
import logging
import argparse
import configparser
import pandas as pd

from progressbar import ProgressBar

from models.Credentials import Credentials
from logger.Logger import Logger
from services.MarvelAPIService import MarvelAPIService
from services.MarvelDataManipulationService import MarvelDataManipulationService
from services.InMemoryCacheService import InMemoryCacheService
from services.MySqlPersistenceService import MySqlPersistenceService
from utilities.DataUtilities import DataUtilities


def _extractComicIdsFromUris(comics):
    return [int(comic.resourceURI.split("comics/")[1]) for comic in comics]

def main():
    if len(sys.argv) < 2:
        Logger.logError("Usage: python3 main.py [optional: 'showKeys'] [required: <character>] [optional: 'clean']")
        sys.exit(1)

    configuration = configparser.ConfigParser()
    configuration.read("configuration/configuration.ini")
    databaseHost = configuration["default"]["database_host"]
    databaseUser = configuration["default"]["database_user"]
    databasePassword = configuration["default"]["database_password"]
    databaseName = configuration["default"]["database_name"]
    tableName = configuration["default"]["table_name"]

    parser = argparse.ArgumentParser(description="Marvel Impossible Travel Challenge")
    parser.add_argument("--character", type=str, help="Optional string positional argument")
    parser.add_argument("--showKeys", action="store_true", help="Optional boolean positional argument")
    parser.add_argument("--showTable", action="store_true", help="Optional boolean positional argument")
    parser.add_argument("--cleanTable", action="store_true", help="Optional boolean positional argument")
    args = parser.parse_args()

    try:
        PUBLIC_KEY = os.environ["MARVEL_PUBLIC_KEY"]
        PRIVATE_KEY = os.environ["MARVEL_PRIVATE_KEY"]
        Logger.log("Public and private keys detected.")
    except KeyError as ke:
        Logger.logError("ERROR: An error occurred while obtaining public/private keys. Did you source an .env file?")
        sys.exit(1)
        
    characterOfInterest, showKeys, showTable, cleanTable = args.character, args.showKeys, args.showTable, args.cleanTable

    databaseCredentials = Credentials(host=databaseHost, user=databaseUser, password=databasePassword)
    apiFactory = MarvelAPIService()
    dataManipulationFactory = MarvelDataManipulationService()
    cacheFactory = InMemoryCacheService()
    persistenceFactory = MySqlPersistenceService(databaseName=databaseName, tableName=tableName)

    if showTable:
        persistenceFactory.getAllFromTable(databaseCredentials)
        if characterOfInterest is None:
            sys.exit(0)
    if showKeys:
        Logger.log("Public Key: {}".format(PUBLIC_KEY))
        Logger.log("Private Key: {}".format(PRIVATE_KEY))
    else:
        Logger.log("Keys have been redacted from this log.")

    Logger.log("Character of interest: {}".format(characterOfInterest))

    pbar = ProgressBar()
    csvFile = "bluevoyant_charactersToUpload.csv"

    character = dataManipulationFactory.getCharacterMetadataByName(str(characterOfInterest), apiFactory)
    cacheFactory.addCharacterToCache(character)

    comicIds = _extractComicIdsFromUris(character.comics)

    Logger.log("Exfiltrating data from Marvel...")

    for comicId in pbar(comicIds):
        charactersInComicId = dataManipulationFactory.getCharactersFromComicId(comicId, apiFactory)
        for character in charactersInComicId:
            extractedCharacter = dataManipulationFactory.extractCharacterMetadata(character)
            if extractedCharacter.id not in cacheFactory.characterCache:
                cacheFactory.addCharacterToCache(extractedCharacter)
            else:
                continue

    if len(cacheFactory.characterCache) == 1:
        Logger.log("No data found from exfiltration.")
        sys.exit(0)

    cacheFactory.writeCacheToCsv(csvFile)

    dataframe = DataUtilities.transformCsvToPandasDf(csvFile)
    Logger.log(dataframe)


    Logger.log("Verifying connectivity to database...")
    persistenceFactory.verifyDatabaseConnectivity(databaseCredentials)

    if cleanTable:
        Logger.log("Cleaning database...")
        persistenceFactory.cleanTable(databaseCredentials)

    Logger.log("Feeding database...")
    persistenceFactory.feedDatabase(dataframe, databaseCredentials)

    Logger.log("Reading from database to verify insertion of entities...")
    persistenceFactory.getAllFromTable(databaseCredentials)



if __name__ == '__main__':
    main()
