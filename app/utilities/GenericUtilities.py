import time
import os


class GenericUtilities:

    def getPublicKey():
        return os.getenv("MARVEL_PUBLIC_KEY")

    def getPrivateKey():
        return os.getenv("MARVEL_PRIVATE_KEY")

    def getCurrentTime():
        return int(time.time())
