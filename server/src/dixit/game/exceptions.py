

class GameDeckExhausted(Exception):
    """
    The card deck has been exhausted and dealing is not possible
    """


class GameRoundIncomplete(Exception):
    """
    The roudn can't be closed because actions are still pending
    """
