

class GameException(Exception):

    def __init__(self, error=None):
        self.error = error

    @property
    def msg(self):
        return getattr(self, 'error', None) or str(self)


class GameDeckExhausted(GameException):
    """
    The card deck has been exhausted and dealing is not possible
    """

    def __init__(self, error=None, round=None, **kwargs):
        self.round = round
        super().__init__(**kwargs)


class GameRoundIncomplete(GameException):
    """
    The round can't be closed because actions are still pending
    """


class GameInvalidPlay(GameException):
    """
    The play can't be performed
    """


class GameFinished(GameException):
    """
    The game has finished and can't be played any longer
    """
