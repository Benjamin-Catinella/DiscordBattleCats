import discord
import random
import json

#Globals
CATS_JSON_PATH = "data/cats/cats.json"
CAT_SPRITES_PATH = "resources/Cat_Sprites/"
# Enums
class Rarity :
    COMMON = 1
    RARE = 2
    SUPER_RARE = 3

# Classes
class Cat :
    name   : str
    image  : str
    power  : int
    health : int
    rarity : Rarity

    def __init__(self, name :str, rarity : Rarity, power : int, health : int ,image : str = "unknown.webp",):
        self.name = name
        self.image = image
        self.rarity = rarity
        self.power = power
        self.health = health


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

    cats_list_json : dict = json.loads(open(CATS_JSON_PATH, 'r').read())
    
    def summon_cat(cat : Cat):
        pass

    async def try_summon_cat_in_channel(channel : discord.TextChannel):
        catToSummon = CatFactory.createCatFromJsonString(cats_list_json[ random.choice( list(cats_list_json) ) ])

        with open(f"{CAT_SPRITES_PATH + catToSummon.image}", "rb") as f:
            await channel.send(f"A wild {catToSummon.name} appeared ! ", file=discord.File(f))

        return

    # -- Events
    @client.event
    async def on_ready():
        print(f'We have logged in as {client.user}')

    @client.event
    async def on_message(message : discord.Message):
        if message.author == client.user:
            return
        

        if message.content == "$summon":
            await try_summon_cat_in_channel(message.channel)




    # Running server    
    client.run(token)