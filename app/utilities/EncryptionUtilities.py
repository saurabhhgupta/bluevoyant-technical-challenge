import hashlib


class EncryptionUtilities:

    def hashKeys(timestamp, privateKey, publicKey):
        stringToEncode = str(timestamp) + str(privateKey) + str(publicKey)
        result = hashlib.md5(stringToEncode.encode()).hexdigest()
        return result
