class UnknownRarityException(Exception):
    def __str__(self) -> str:
        return super().__str__()

class CallbackNotChangedException(Exception):
    def __str__(self) -> str:
        return super().__str__()
