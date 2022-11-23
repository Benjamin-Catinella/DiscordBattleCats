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

class CatAlreadyInInventoryException(Exception):
    def __str__(self) -> str:
        return super().__str__() + "Cat was already present in user inventory"

class InventoryFileErrorException(Exception):
    def __str__(self) -> str:
        return super().__str__() + "There was a problem when managing the inventory"