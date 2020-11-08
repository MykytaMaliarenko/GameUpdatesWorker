class GameBasedChannelNotFoundException(Exception):

    def __str__(self):
        return f'game based channel for game not found '


class GameNotFoundException(Exception):

    def __str__(self):
        return f'game not found'
