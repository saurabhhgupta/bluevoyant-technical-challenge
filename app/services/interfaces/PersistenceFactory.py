import abc


class PersistenceFactory(abc.ABC):

    @abc.abstractmethod
    def verifyDatabaseConnectivity(self, host: str, user: str, password: str):
        pass

    @abc.abstractmethod
    def feedDatabase(self, dataframe, host: str, user: str, password: str):
        pass

    @abc.abstractmethod
    def getAllFromTable(host: str, user: str, password: str):
        pass

    @abc.abstractmethod
    def cleanTable(host: str, user: str, password: str):
        pass
