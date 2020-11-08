class FeedDoesntExist(Exception):

    def __init__(self, steam_id: int):
        self.steam_id = steam_id

    def __str__(self):
        return f'Feed doesnt exist for steam_id={self.steam_id}'
