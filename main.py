import discord
import random
import json
from enum import Enum
from utils import *
#Globals
CATS_JSON_PATH = "data/cats/cats.json"
CAT_SPRITES_PATH = "resources/Cat_Sprites/"
Logger.DEBUG_LEVEL = 1

# Enums
class Rarity(Enum) :
    COMMON = 1
    SPECIAL = 2
    RARE = 3
    SUPER_RARE = 4
    UBER_RARE = 5
    LEGEND_RARE = 6

# Classes
class Cat :
    name   : str
    image  : str
    power  : int
    health : int
    rarity : Rarity

    def __init__(self, name :str, rarity : Rarity, power : int, health : int ,image : str = "unknown.webp",):
        self.name = name
        try:
            with open(CAT_SPRITES_PATH + image, "r") as f:
                f.close()
                self.image = image
        except:
            Logger.log(3, f"Couldn't set {self.name} image, setting default")
            self.image = "unknown.webp"

        self.rarity = rarity
        self.power = power
        self.health = health
    
    def getCatImageFilePath(self):
        return CAT_SPRITES_PATH + self.image

    def __str__(self) -> str:
        return f"{self.name} , Image:{self.image} , Rarity:{self.rarity} , Power:{self.power} , Health:{self.health}"

# Factories
class CatFactory:
    
    @staticmethod
    def createCatFromJsonString(jsonString : dict):
        
        name = jsonString["name"]
        image = jsonString["image"]
        rarity = getattr(Rarity, str.upper(jsonString["rarity"]))
        power = int(jsonString["power"])
        health = int(jsonString["health"])
        return Cat(name,rarity,power,health,image)


if __name__ == "__main__":
    #Getting the tokens
    token = open("token", 'r').read()

    #Initial setup
    intents = discord.Intents.default()
    intents.message_content = True

    client = discord.Client(intents = intents)
    main_channel : discord.TextChannel
    cats_list_json : dict = json.loads(open(CATS_JSON_PATH, 'r').read())
    
    def summon_cat(cat : Cat):
        pass

    async def try_summon_cat_in_channel(channel : discord.TextChannel, catName = None):
        catToSummon : Cat = None
        try:
            if catName is not None:
                catToSummon = CatFactory.createCatFromJsonString(cats_list_json[catName])
            else:
                catToSummon = CatFactory.createCatFromJsonString(cats_list_json[ random.choice( list(cats_list_json) ) ])
        except:
            catToSummon = CatFactory.createCatFromJsonString(cats_list_json[ random.choice( list(cats_list_json) ) ])
        await channel.send(f"A wild **{str.upper(Rarity(catToSummon.rarity).name)}** {catToSummon.name} appeared ! ", file=discord.File( catToSummon.getCatImageFilePath() ) )

        return

    async def sendErrorInChat(channel : discord.TextChannel, errorMessage):
        await channel.send(errorMessage)
    

    # -- Events
    @client.event
    async def on_ready():
        print(f'We have logged in as {client.user}')
        main_channel = client.get_channel(1041000719467151392)
        if Logger.DEBUG_LEVEL >= 2:
            await main_channel.send("I'm alive !")
        

    @client.event
    async def on_message(message : discord.Message):
        if message.author == client.user:
            return

        if message.content.startswith("$summon"):
            args : list = message.content.split(" ")[1:]
            cat = ' '.join(args)
            try:
                await try_summon_cat_in_channel(message.channel, cat)
            except Exception as e:
                await sendErrorInChat(message.channel, f"Couldn't summon a cat: \n {e}")
            



    # Running server    
    client.run(token)