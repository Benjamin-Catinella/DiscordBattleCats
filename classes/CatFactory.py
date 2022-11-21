from .Cat import *
class CatFactory:
    
    @staticmethod
    def createCatFromDatabaseEntry(jsonString : dict):
        
        name = jsonString["name"]
        
        return Cat(name)