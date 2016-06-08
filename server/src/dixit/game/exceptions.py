

class GameDeckExhausted(Exception):
    """
    The card deck has been exhausted and dealing is not possible
    """


class GameRoundIncomplete(Exception):
    """
    The round can't be closed because actions are still pending
    """


class GameInvalidPlay(Exception):
    """
    The play can't be performed
    """
