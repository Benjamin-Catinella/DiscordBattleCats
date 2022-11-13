
class Logger:
    """Custom logger class
    """
    
    DEBUG_LEVEL : int = 5
    
    @staticmethod
    def log( *args, debug_level : int = 1):
        """Logs a message if the input debug level (default 1) is higher than the gobal Debug level

        Args:
            debug_level (int, optional): Debug level. Defaults to 1.
        """
        if  debug_level <= Logger.DEBUG_LEVEL:
            
            print(str(args))