import discord

class MessageToTextInventory : 
    """Association class to help manipulating the displayed inventory
    """
    __assoc : dict[int ,list[discord.Message, int]] = {}
    
        
    @staticmethod
    def get() -> dict[int ,list[discord.Message, int]]:
        """Gets the association
        """
        return MessageToTextInventory.__assoc

    @staticmethod 
    def get_message(id : int) -> discord.Message:
        return MessageToTextInventory.__assoc[id][0]

    @staticmethod
    def get_page(id : int) -> int:
        """Gets page from the assoc using the message id
        Args:
            id (int): message id
        Returns:
            int: The page associated with the message
        """
        return MessageToTextInventory.__assoc[id][1]
    
    @staticmethod
    def add(message : discord.Message, page: int):
        MessageToTextInventory.__assoc[message.id] = [message,page]
    
    @staticmethod
    def remove(message : discord.Message):
        MessageToTextInventory.__assoc.pop(message.id)

    def increment(message: discord.Message):
        MessageToTextInventory.__assoc[message.id][1] += 1 
    
    def decrement(message: discord.Message):
        MessageToTextInventory.__assoc[message.id][1] -= 1 