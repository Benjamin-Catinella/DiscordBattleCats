class UnknownRarityException(Exception):
    def __str__(self) -> str:
        return super().__str__()

class CallbackNotChangedException(Exception):
    def __str__(self) -> str:
        return super().__str__()

class UnknownCommandException(Exception):
    def __str__(self) -> str:
        return "Unknown command, please use the 'help' command for more info"

class MessageNotReturnedException(Exception):
    def __str__(self) -> str:
        return super().__str__() + "Message expected but not returned"