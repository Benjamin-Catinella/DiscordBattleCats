import discord
from .Cat import Cat

class MessageToCat : 
    """Association class to manipulate the summoned cats and the messages they appeared in
    """
    __assoc : dict[int ,list[discord.Message, Cat]] = {}
    
        
    @staticmethod
    def get():
        return MessageToCat.__assoc

    @staticmethod   
    def get_message(id : int):
        return MessageToCat.__assoc[id]

    @staticmethod
    def get_cat(id : int) -> Cat:
        """Gets cat from the assoc using the message id

        Args:
            id (int): message id

        Returns:
            Cat: The cat associated with the message
        """
        return MessageToCat.__assoc[id][1]
    @staticmethod
    def add(message : discord.Message, cat: Cat):
        MessageToCat.__assoc[message.id] = [message,cat]
    
    @staticmethod
    def remove(message : discord.Message):
        MessageToCat.__assoc.pop(message.id)