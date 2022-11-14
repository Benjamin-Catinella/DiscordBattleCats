import discord
import random
import json
from os import path
from enum import Enum
from utils import *
from exceptions import *

#Globals
# Path related
RESOURCES_FOLDER = "resources/"
DATA_FOLDER = "data/"
CATS_JSON_FILE_PATH = f"{DATA_FOLDER}cats/cats.json"
CAT_SPRITES_FOLDER_PATH = f"{RESOURCES_FOLDER}Cat_Sprites/"
USER_INVENTORY_FOLDER_PATH = f"{DATA_FOLDER}inventories/"
INVENTORY_TEMPLATE_FILE_PATH = f"{DATA_FOLDER}inventory_template.json"

# Command related
USER_COMMAND_PREFIX = "dbc! "

# Other
MAIN_CHANNEL_ID = 1041000719467151392
print(f"Logger debug level set to {Logger.DEBUG_LEVEL}")
CAT_ENCOUNTER_CHANCE = 50
REACTIONS = {
    "catch" : "🟩",
    "no"    : "❌"
}


# Enums
class Rarity(Enum) :
    COMMON = 1
    SPECIAL = 2
    RARE = 3
    SUPER_RARE = 4
    UBER_RARE = 5
    LEGEND_RARE = 6

# Classes
class Encounterable:
    pass


class Cat(Encounterable) :
    name   : str
    image  : str
    power  : int
    health : int
    rarity : Rarity

    def __init__(self, name :str, rarity : Rarity, power : int, health : int ,image : str = "unknown.webp",):
        self.name = name
        try:
            with open(CAT_SPRITES_FOLDER_PATH + image, "r") as f:
                f.close()
                self.image = image
        except:
            Logger.log(3, f"Couldn't set {self.name} image, setting default")
            self.image = "unknown.webp"

        self.rarity = rarity
        self.power = power
        self.health = health
    
    def getCatImageFilePath(self):
        return CAT_SPRITES_FOLDER_PATH + self.image

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

class JSONToDiscordMessageFormatter:
    """Formats json entries to be displayed in a human readable format to be used in a message
    """
    
    
    @staticmethod
    def format_cats_inventory(cats : list[Cat]):
        """Example: 
        Your inventory:
            - Axe cat | Special | HP : 10 | Power : 5

        Args:
            cats (list[Cat]): should be the array of cats
        """
        t = ""
        for cat in cats:
            t += f"- {cat.name} | {cat.rarity} | Health : {cat.health} | Power : {cat.power} "
            t += "\n"

        return t

# TODO Implement this in some way later
class Encounter:
    def __init__(self, encounterable : Encounterable):
        pass


# Managers
class JSONInventoryManager:
    
    @staticmethod
    def create_new_inventory_from_id(uid : int):
        Logger.log(f"Creating inventory file for {uid}")
        json_data = ""
        with open(INVENTORY_TEMPLATE_FILE_PATH, 'r') as f:
            json_data = json.loads(f.read())
        
        with open(f"{USER_INVENTORY_FOLDER_PATH}{str(uid)}.json", "w") as f:
            json.dump(json_data, f, indent=4) 
    
    @staticmethod
    def add_cat_to_player_inventory(id: int, cat :Cat):
        pass

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
        return json.loads(JSONInventoryManager.get_player_inventory_from_id(uid=uid))["cats"][0]

    @staticmethod
    def get_cats_from_id_as_cats(uid :int):
        """ Gets all cats from a player's inventory but returns a list with cat objects for easier manipulation

        Args:
            uid (int): user id

        Returns:
            list[Cat]: List of cats
        """
        cats : dict(str,object) = JSONInventoryManager.get_cats_from_id(uid=uid)
        catsToReturn : list(Cat) = []
        for cat in cats:
            print(cat)
            catsToReturn.append(CatFactory.createCatFromJsonString(cats[cat])) 
        return catsToReturn
        

if __name__ == "__main__":

    # -- Getting the token
    token = open("token", 'r').read()

    # -- Initial setup
    intents = discord.Intents.default()
    intents.message_content = True
    intents.members = True
    client = discord.Client(intents = intents)
    
    main_channel : discord.TextChannel
    members : list[discord.Member] = []
    guilds : list[discord.Guild] = []

    # "pointer" variables
    member_being_processed : discord.member
    message_being_processed : discord.Message

    # -- Loading cats
    cats_list_json : dict = json.loads(open(CATS_JSON_FILE_PATH, 'r').read())
    
    # -- Functions

    async def DEBUG_try_summon_cat_in_channel(channel : discord.TextChannel, catName = None):
        catToSummon : Cat = None
        try:
            if catName is not None:
                catToSummon = CatFactory.createCatFromJsonString(cats_list_json[catName])
            else:
                catToSummon = CatFactory.createCatFromJsonString(cats_list_json[ random.choice( list(cats_list_json) ) ])
        except:
            catToSummon = CatFactory.createCatFromJsonString(cats_list_json[ random.choice( list(cats_list_json) ) ])
        return await channel.send(f"A wild **{str.upper(Rarity(catToSummon.rarity).name)}** {catToSummon.name} appeared ! Capture it by clicking the {REACTIONS['catch']}! ", file=discord.File( catToSummon.getCatImageFilePath() ) )


    def try_create_encounter(channel : discord.TextChannel):
        # 
        pass

    async def sendErrorInChat(channel : discord.TextChannel, errorMessage):
        """ Sends the error in the main discord channel

        Args:
            channel (discord.TextChannel): _description_
            errorMessage (_type_): _description_
        """
        await channel.send(errorMessage)


    # -- Inventory related
    async def initialize_inventory_system():
        # Check if inventory exists for every user

        for member in members:
            if member.id == client.user.id:
                continue
            id = member.id
            filepath = USER_INVENTORY_FOLDER_PATH + str(id)
            if(not path.isfile(filepath+".json")):
                JSONInventoryManager.create_new_inventory_from_id(id)

    # -- Commands
    async def command_cats(message : discord.Message, args: list[str]):
        Logger.log("Executing command 'cats'", 3)
        
        # -- Show cats from inventory
        if args[0]=="show":
            # Get inventory as array
            catsArray = JSONInventoryManager.get_cats_from_id_as_cats(message.author.id)
            # Show inventory
            if(len(catsArray) > 0):
                catsInventoryMessage = JSONToDiscordMessageFormatter.format_cats_inventory(catsArray)
            else:
                await message.reply("You have no cats :C")
                return
            await message.reply(catsInventoryMessage)

        else:
            await message.reply(f"Command {args[0]} not yet implemented")
        

    async def command_items(message : discord.Message, args: list[str]):
        Logger.log("Executing command 'items'", 3)
        if args[0]=="show":
            await message.reply("You used the show command")
        else:
            await message.reply(f"Command {args[0]} not yet implemented")
        

    # -- Command management
    def parse_command(command : str):
        Logger.log(f"Parsing command {command}", 3)
        # dbc!
        command = command.split(" ")
        instruction = command[0]
        args = command[1:]
        return instruction.lower(), args

    async def process_command(message : discord.Message, command : str):
        instruction, args = parse_command(command = command)
        if instruction == "cats":
            await command_cats(message, args=args)
        elif instruction == "items":
            await command_items(message, args=args)
        else:
            await message.reply(f"The \"{instruction}\" command doesn't exist")
            # DONE : Later add a way for the bot to tell the command doesn't exist

    # -- Events
    @client.event
    async def on_ready():
        # -- Init members/guilds
        guilds = [guild async for guild in client.fetch_guilds(limit=15)]
        tmembers = []

        for guild in guilds:
            guild : discord.Guild
            tmembers = [member async for member in guild.fetch_members()]
            for member in tmembers:
                if(member not in members):
                    members.append(member)


        # -- Inventories
        await initialize_inventory_system()

        print(f'We have logged in as {client.user}')
        main_channel = client.get_channel(MAIN_CHANNEL_ID)
        if Logger.DEBUG_LEVEL >= 2:
            await main_channel.send("I'm alive !")

    @client.event
    async def on_reaction_add(reaction : discord.Reaction, user : discord.Member):
        print(f"Reaction added from {user.name}")
        channel : discord.TextChannel = reaction.message.channel
        #send("<@" + str(user_id) + ">")
        if user == client.user:
            return
        
        if reaction.emoji == REACTIONS["catch"]:
            await reaction.message.delete()
            await channel.send("<@" + str(user.id) + "> Captured the cat !")
        elif reaction.emoji == REACTIONS["no"]:
            await reaction.message.delete()
        
    # -- On message Event
    @client.event
    async def on_message(message : discord.Message):
        Logger.log(f"event.on_message : Message from {message.author.name} : {message.content}", debug_level=3)
        #Logger doesn't work here for some reason

        if message.author == client.user or message.author.bot:
            return
        
        # User Commands

        if message.content.startswith(USER_COMMAND_PREFIX):
            
            await process_command(message, message.content.removeprefix(USER_COMMAND_PREFIX))
            return


        if message.content.startswith("$summon"):
            args : list = message.content.split(" ")[1:]
            cat = ' '.join(args)
            try:
                encounterMessage = await DEBUG_try_summon_cat_in_channel(message.channel, cat)
                await encounterMessage.add_reaction(REACTIONS["catch"])
                await encounterMessage.add_reaction(REACTIONS["no"])


            except Exception as e:
                await sendErrorInChat(message.channel, f"Couldn't summon a cat: \n {e}")
            return
        
        if(random.randint(0,100) >= CAT_ENCOUNTER_CHANCE):
            # TODO Don't forget to remove this later because it's mad ugly
            encounterMessage = await DEBUG_try_summon_cat_in_channel(message.channel)
            await encounterMessage.add_reaction(REACTIONS["catch"])
            await encounterMessage.add_reaction(REACTIONS["no"])

    # Running server    
    client.run(token)