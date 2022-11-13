class UnknownCommandException(Exception):
    def __str__(self) -> str:
        return "Unknown command, please use the 'help' command for more info"