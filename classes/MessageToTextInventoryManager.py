import discord
from datetime import datetime
from dataclasses import dataclass
@dataclass
class CatsInventoryMessageDataclass:
    message: discord.Message
    page : int
    uid : int
    timestampCreated = datetime.timestamp(datetime.now())

class MessageToTextInventoryManager : 
    """Association class to help manipulating the displayed inventory
    """
    __assoc : dict[int ,CatsInventoryMessageDataclass] = {}
    
        
    @staticmethod
    def get() -> dict[int ,CatsInventoryMessageDataclass]:
        """Gets the association"""
        return MessageToTextInventoryManager.__assoc

    @staticmethod 
    def get_message(id : int) -> discord.Message:
        return MessageToTextInventoryManager.__assoc[id].message

    @staticmethod
    def get_page(id : int) -> int:
        """Gets page from the assoc using the message id
        Args:
            id (int): message id
        Returns:
            int: The page associated with the message
        """
        return MessageToTextInventoryManager.__assoc[id].page
    @staticmethod
    def get_user_id(id : int) -> int:
        """Gets user associated with the message from the assoc using the message id
        Args:
            id (int): message id
        Returns:
            int: The user id associated with the message
        """
        return MessageToTextInventoryManager.__assoc[id].uid
    def get_time_created(id: int) -> float:
        """Returns a timestamp"""
        return MessageToTextInventoryManager.__assoc[id].timestampCreated
    @staticmethod
    def add(message : discord.Message, page: int, uid : int):
        MessageToTextInventoryManager.__assoc[message.id] = CatsInventoryMessageDataclass(message,page,uid)
    
    @staticmethod
    def remove(message : discord.Message):
        """Removes the message from the assoc, also returns the item"""
        return MessageToTextInventoryManager.__assoc.pop(message.id)

    def increment(message: discord.Message):
        MessageToTextInventoryManager.__assoc[message.id].page += 1 
    
    def decrement(message: discord.Message):
        MessageToTextInventoryManager.__assoc[message.id].page -= 1 