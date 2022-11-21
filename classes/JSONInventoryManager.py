import json
from utils import Logger
from globals import *
from .Cat import Cat
from os import path
from .CatFactory import CatFactory

class JSONInventoryManager:
    """ Static class containing every function in relation to the inventory system
    """
    @staticmethod
    def create_new_inventory_from_id(uid : int):
        """Creates inventory file from user id, usually called when the file is non-existent.
        TODO Later use this function to reset inventories

        Args:
            uid (int): Discord Member id 
        """
        Logger.log(f"Creating inventory file for {uid}")
        json_data = ""
        with open(INVENTORY_TEMPLATE_FILE_PATH, 'r') as f:
            json_data = json.loads(f.read())
        
        with open(f"{USER_INVENTORY_FOLDER_PATH}{str(uid)}.json", "w") as f:
            json.dump(json_data, f, indent=4) 
    @staticmethod
    def get_player_inventory_file(uid: int):
        """Centralized method to get the file

        Args:
            uid (int): Member user id

        Returns:
            str: File name
        """
        return str(uid)+".json"


    @staticmethod
    def add_cat_to_player_inventory(uid: int, cat :Cat):
        jsonInventory : dict
        try:
            with open(USER_INVENTORY_FOLDER_PATH+JSONInventoryManager.get_player_inventory_file(uid), "r") as f:
                jsonInventory = json.load(f)
                jsonInventory["cats"].append(cat.toJson())
            with open(USER_INVENTORY_FOLDER_PATH+JSONInventoryManager.get_player_inventory_file(uid), "w") as f:
                f.write(json.dumps(jsonInventory, indent=4))
        except:
            JSONInventoryManager.create_new_inventory_from_id(uid)
            JSONInventoryManager.add_cat_to_player_inventory(uid, cat)


    @staticmethod
    def remove_cat_from_player_inventory(id: int, cat : Cat):
        pass
    
    @staticmethod
    def get_player_inventory_from_id(uid : int):
        """Returns player inventory as json flat string

        Args:
            uid (int): User id

        Returns:
            str: json flat string of player inventory
        """
        #If inventory doesn't exist
        Logger.log(f"Getting inventory from {uid}", debug_level= 3)

        if(not path.isfile(USER_INVENTORY_FOLDER_PATH + str(uid) +".json")):
            Logger.log(f"Tried getting inventory of {uid} but file was absent", debug_level=2)
            JSONInventoryManager.create_new_inventory_from_id(uid)
            
        with open(f"{USER_INVENTORY_FOLDER_PATH}{uid}.json", 'r') as f:
            return f.read()
    @staticmethod
    def get_cats_from_id(uid :int):
        """ Gets all cats from a player's inventory

        Args:
            uid (int): user id

        Returns:
            list[object]: List of json objects
        """
        return json.loads(JSONInventoryManager.get_player_inventory_from_id(uid=uid))["cats"]

    @staticmethod
    def get_cats_from_id_as_cats(uid :int):
        """ Gets all cats from a player's inventory but returns a list with cat objects for easier manipulation

        Args:
            uid (int): user id

        Returns:
            list[Cat]: List of cats
        """
        cats : list(dict(str,object)) = JSONInventoryManager.get_cats_from_id(uid=uid)
        catsToReturn : list(Cat) = []
        for cat in cats:
            catsToReturn.append(CatFactory.createCatFromDatabaseEntry(cat)) 
        return catsToReturn