class GameBasedChannelNotFoundException(Exception):

    def __int__(self, game_steam_id: int):
        self.game_steam_id = game_steam_id

    def __str__(self):
        return f'game based channel for game with ' \
               f'steam_id={self.game_steam_id} not found'


class GameNotFoundException(Exception):

    def __init__(self, game_id: int):
        self.game_id = game_id

    def __str__(self):
        return f'game with id={self.game_id} not found'


class GameNotFoundBySteamIdException(Exception):

    def __init__(self, steam_id: int):
        self.steam_id = steam_id

    def __str__(self):
        return f'game with steam_id={self.steam_id} not found'
