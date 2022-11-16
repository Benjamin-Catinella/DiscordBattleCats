import discord
import random
import json
from os import path
from enum import Enum
from utils import *
from exceptions import *
from discord import interactions
from discord import app_commands

"""
Stuff to change later:
    - Load/Reload JSON periodically in memory instead of opening the file for every operation; Possible performance gain
        userinventories["uid"]*dict -> on_content_changed -> save to [userid].json*file


    - Cat / CatModel separation

                                | Cat           |
                                | name, level   | 
                                    |
                                    v
        [ CatModel ]-> get_cat_rarity -> rarity
                    -> get_cat_image  -> image
        
        Could be a better design instead of storing properties multiple times, because for now the database and the object are too tied, meaning that for example
        if i wanted to change a cat's image (eg: custom cat having a sprite update), i'd have to change it in every player inventory too, same for the rarity
        or other properties i could add later



        
"""


#Globals
# Path related
RESOURCES_FOLDER = "resources/"
DATA_FOLDER = "data/"
CATS_JSON_DB_FILE_PATH = f"{DATA_FOLDER}cats/cats.json"
CAT_SPRITES_FOLDER_PATH = f"{RESOURCES_FOLDER}Cat_Sprites/"
USER_INVENTORY_FOLDER_PATH = f"{DATA_FOLDER}inventories/"
INVENTORY_TEMPLATE_FILE_PATH = f"{DATA_FOLDER}inventory_template.json"

# Command related
USER_COMMAND_PREFIX = "dbc! "

# Other
MAIN_CHANNEL_ID = 1041000719467151392
DEBUG = True
print(f"Logger debug level set to {Logger.DEBUG_LEVEL}")
CAT_ENCOUNTER_CHANCE = 1
REACTIONS = {
    "catch" : "🟩",
    "no"    : "❌"
}


# Enums
RARITY_MAP = {
    "COMMON" : "Common",
    "SPECIAL" : "Special",
    "RARE" : "Rare",
    "SUPER_RARE" : "Super rare",
    "UBER_RARE" : "Uber rare",
    "LEGEND_RARE" : "Legend rare"
}



# Classes
class Encounterable:
    pass


class Cat(Encounterable) :
    name   : str

    def __init__(self, name :str):
        self.name = name

    def __str__(self) -> str:
        return f"{self.name}"

    def toJson(self):
        return {"name" : self.name}

class CatModel:
    """ Bunch of static methods to get cat properties from the json database
    """
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



# Factories
class CatFactory:
    
    @staticmethod
    def createCatFromDatabaseEntry(jsonString : dict):
        
        name = jsonString["name"]
        
        return Cat(name)

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
        t = ""
        for cat in cats:
            t += f"- {cat.name} | { CatModel.get_cat_property(cat.name, 'rarity') } | Level : {'Not implemented yet'}"
            t += "\n"

        return t

# TODO Implement this in some way later for an easier time with encounter mechanics
class Encounter:
    def __init__(self, encounterable : Encounterable):
        pass


# Managers
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
        except json.JSONDecodeError:
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




if __name__ == "__main__":

    # -- Getting the token
    token = open("token", 'r').read()

    # -- Initial setup
    intents = discord.Intents.default()
    intents.message_content = True
    intents.members = True
    client = discord.Client(intents = intents)
    
    # -- interactions
    

    main_channel : discord.TextChannel
    members : list[discord.Member] = []
    guilds : list[discord.Guild] = []

    # "pointer" variables
    member_being_processed : discord.member
    message_being_processed : discord.Message

    # -- Loading cats
    cats_list_json : dict = json.loads(open(CATS_JSON_DB_FILE_PATH, 'r').read())
    
    # -- Functions

    async def DEBUG_try_summon_cat_in_channel(channel : discord.TextChannel, catName = None, message : discord.Message = None):
        """DEBUG !!! Used to summon cats for debug purposes

        Args:
            channel (discord.TextChannel): The channel to summon the cat in
            catName (str, optional): The name of the cat passed as argument. Defaults to None.
            message (discord.Message, optional): _description_. Defaults to None.

        Returns:
            _type_: _description_
        """
        catToSummon : Cat = None
        try:
            if catName is not None:
                catToSummon = CatFactory.createCatFromDatabaseEntry(cats_list_json[catName])
            else:
                catToSummon = CatFactory.createCatFromDatabaseEntry(cats_list_json[ random.choice( list(cats_list_json) ) ])
        except:
            catToSummon = CatFactory.createCatFromDatabaseEntry(cats_list_json[ random.choice( list(cats_list_json) ) ])
        message_sent = await channel.send(
            f"A wild **{RARITY_MAP[ str.upper(CatModel.get_cat_property(catToSummon, 'rarity'))]}** {catToSummon.name} appeared ! Capture it by clicking {REACTIONS['catch']}! ", 
            file=discord.File( CatModel.get_cat_image_image_fullpath(catToSummon) ) 
            )
        MessageToCat.add(message=message_sent, cat=catToSummon)
        Logger.log(f"Added {catToSummon} to {message.id} ", debug_level=3)
        return message_sent


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
                catsInventoryMessage = TextFormatter.format_cats_inventory(catsArray)
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
    def capture_cat(mid: int, uid : int):
        """ Capture a summoned cat, returns True if succeeded
        Args:
            mid (int): Message id
            uid (int): User id
        """
        try:
            JSONInventoryManager.add_cat_to_player_inventory(
                uid,
                MessageToCat.get_cat(mid)
            )
        except Exception as e:
            raise e
        return True
        

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


    # -- On reaction add event
    ## Used for the capture mechanic
    @client.event
    async def on_reaction_add(reaction : discord.Reaction, user : discord.Member):
        print(f"Reaction added from {user.name}")
        channel : discord.TextChannel = reaction.message.channel
        #send("<@" + str(user_id) + ">")
        if user == client.user:
            return
        
        
        if reaction.emoji == REACTIONS["catch"]:

            if capture_cat(reaction.message.id, user.id):
                capturedCat = MessageToCat.get_cat(reaction.message.id)
                await reaction.message.delete()
                await channel.send("<@" + str(user.id) + f"> Captured {capturedCat.name} !")


        elif reaction.emoji == REACTIONS["no"]:
            await reaction.message.delete()
    

    # -- On message Event
    @client.event
    async def on_message(message : discord.Message):
        """On message event \n
        Contains the command processing instructions as well as the cat encounter mechanics

        Args:
            message (discord.Message): _description_
        """
        Logger.log(f"event.on_message : Message from {message.author.name} : {message.content}", debug_level=3)
        #Logger doesn't work here for some reason

        if message.author == client.user or message.author.bot:
            return
        
        # User Commands

        if message.content.startswith(USER_COMMAND_PREFIX):
            
            await process_command(message, message.content.removeprefix(USER_COMMAND_PREFIX))
            return



        # Debug commands
        if not DEBUG:
            return
        if message.content.startswith("$summon"):
            args : list = message.content.split(" ")[1:]
            cat = ' '.join(args)
            try:
                encounterMessage = await DEBUG_try_summon_cat_in_channel(message.channel, cat, message=message)
                await encounterMessage.add_reaction(REACTIONS["catch"])
                await encounterMessage.add_reaction(REACTIONS["no"])
                
                

            except Exception as e:
                await sendErrorInChat(message.channel, f"Couldn't summon a cat: \n {e}")
                raise e
            return
        
        # if(random.randint(0,100) >= CAT_ENCOUNTER_CHANCE):
        #     # TODO Don't forget to remove this later because it's mad ugly
        #     encounterMessage = await DEBUG_try_summon_cat_in_channel(message.channel)
        #     await encounterMessage.add_reaction(REACTIONS["catch"])
        #     await encounterMessage.add_reaction(REACTIONS["no"])

    # Running server    
    client.run(token)