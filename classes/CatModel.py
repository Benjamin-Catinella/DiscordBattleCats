import json
from globals import *
from .Cat import Cat
from .CatFactory import CatFactory

class CatModel:
    """ Bunch of static methods to get cat properties from the json database
    """
    @staticmethod
    def get_cat_from_name(catName) -> Cat:
        with open(CATS_JSON_DB_FILE_PATH, "r") as f:
            jsondb = json.load(f)
            try:
                return CatFactory.createCatFromDatabaseEntry(jsondb[catName])
            except:
                raise Exception(f"Cat {catName} doesn't exist in database")

    @staticmethod
    def get_cat_property(catName, property : str) -> str:
        """ Fetches a property of a specified cat from the database

        Args:
            catName (strorCat): str
            property (str): _description_

        Raises:
            Exception: Cat doesn't exist in database
            Exception: Property doesn't exist on the cat

        Returns:
            str: _description_
        """
        if type(catName) is Cat:
            catName = catName.name
        with open(CATS_JSON_DB_FILE_PATH, "r") as f:
            jsondb = json.load(f)
            try:
                jsondb[catName]
            except:
                raise Exception(f"Cat {catName} doesn't exist in database")
            try:
                return jsondb[catName][property]
            except:
                raise Exception(f"Property {property} doesn't exist on {catName}")
    
    def get_cat_image_image_fullpath(cat : Cat):
        with open(CATS_JSON_DB_FILE_PATH, "r") as f:
            jsondb = json.load(f)
            return CAT_SPRITES_FOLDER_PATH + jsondb[cat.name]["image"]