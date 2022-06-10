class Character:

    def __init__(
            self,
            name: str,
            id: str,
            description: str,
            thumbnail: str,
            comics: list):
        self.name = name
        self.id = id
        self.description = description
        self.thumbnail = thumbnail
        self.comics = comics
