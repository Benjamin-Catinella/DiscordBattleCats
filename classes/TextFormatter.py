from .Cat import Cat
from globals import *
from .CatModel import CatModel
class TextFormatter:
    """Formats lots of things to be displayed in a human readable format and be used in a discord message
    """
    
    @staticmethod
    def format_rarity(r):
        pass
        
    @staticmethod
    def format_cats_inventory(cats : list[Cat]):
        """Example: 
        Your inventory:
            - Axe cat | Special | HP : 10 | Power : 5

        Args:
            cats (list[Cat]): should be the array of cats
        """
        t = "```"
        for i, cat in enumerate(cats):
            t += f"- {cat.name} | { RARITY_MAP.get(str.upper(CatModel.get_cat_property(cat.name, 'rarity'))) } | Level : {'Not implemented yet'}"
            t += "\n"
            if( i > 10):
                t += "And more... Use /cat_stats for statistics"
                break
        return t + "```"