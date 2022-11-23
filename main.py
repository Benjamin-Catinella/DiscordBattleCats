import discord
import random
import json
import math
from os import path
from utils import *
from discord import app_commands, Button, ButtonStyle, components 
from classes import *
from globals import *

# TODO 1: Separate dev server inventories from others
# TODO 1: Clean up shit, and then try to deploy the bot on klowbi's and maybe the server Obi and I got, if it can handle multiple
# TODO 2: For memory usage potential issue, create a loop that will remove each element that's too old in associations
# TODO 999: Write tests :x

# --------------------------------------- MAIN --------------------------------------- #

if __name__ == "__main__":

    # -- Getting the token
    token = open("token", 'r').read()

    # -- Initial setup
    intents = discord.Intents.default()
    intents.message_content = True
    intents.members = True
    client = discord.Client(intents = intents)
    
    # -- App commands
    command_tree = app_commands.CommandTree(client)
    

    main_channel : discord.TextChannel
    members : list[discord.Member] = []
    guilds : list[discord.Guild] = []
    dev_guild = client.get_guild(DEV_SERVER_ID)

    # -- Loading cats
    cats_list_json : dict = json.loads(open(CATS_JSON_DB_FILE_PATH, 'r').read())

    # Those lists are used to categorize cats by rarity, used for example in the selection of random cats
    # TODO (?) Maybe find a better way
    common_cats     : list[Cat] = []
    rare_cats       : list[Cat] = []
    super_rare_cats : list[Cat] = []
    uber_rare_cats  : list[Cat] = []
    legend_rare_cats: list[Cat] = []
    Logger.log("Adding cat names to their respective rarity list")
    for cat in cats_list_json:
        if   cats_list_json[cat]["rarity"] == "common":
            common_cats.append(cat)
        elif cats_list_json[cat]["rarity"] == "rare" : 
            rare_cats.append(cat)
        elif cats_list_json[cat]["rarity"] == "super_rare" : 
            super_rare_cats.append(cat)
        elif cats_list_json[cat]["rarity"] == "uber_rare" : 
            uber_rare_cats.append(cat)
        elif cats_list_json[cat]["rarity"] == "legend_rare" : 
            legend_rare_cats.append(cat)
    

    # -- Functions
    async def nextPage(interaction: discord.Interaction):
        if interaction.user.id is not MessageToTextInventoryManager.get_user_id(interaction.message.id):
            await interaction.response.defer()
            return
        page = MessageToTextInventoryManager.get_page(interaction.message.id)
        try:
            await show_cats_from_player_inventory(interaction, page+1, edit=True)
        except Exception as e:
            raise e
        MessageToTextInventoryManager.increment(interaction.message)

    async def previousPage(interaction : discord.Interaction):
        if interaction.user.id is not MessageToTextInventoryManager.get_user_id(interaction.message.id):
            await interaction.response.defer()
            return
        page = MessageToTextInventoryManager.get_page(interaction.message.id)
        try:
            await show_cats_from_player_inventory(interaction, page-1, edit=True)
        except Exception as e:
            raise e
        MessageToTextInventoryManager.decrement(interaction.message)

    async def show_cats_from_player_inventory(interaction : discord.Interaction, page=1, edit=False):
        """Displays a player's cats in their inventory by page, also edits the message

        Args:
            interaction (discord.Interaction): the interaction comming from the command
        """
        Logger.log("Executing command 'Show cats'", 3)


        # Get inventory as array
        catsArray = JSONInventoryManager.get_cats_from_id_as_cats(interaction.user.id)
        tempCatsArray = []
        maxPage = math.ceil(len(catsArray) / CATS_PER_INV_PAGE)
        nextOff = False
        previousOff = False
        # If inputting a page greater than the max number of pages, shows the last one
        
        if(page >= maxPage ): 
            page = maxPage
            nextOff = True
        # If page number is 0 or less
        if(page <= 1 ): 
            page = 1
            previousOff = True

        # Show inventory
        if(len(catsArray) > 0):
            p = 1
            for i, cat in enumerate(catsArray):
                if p == page:
                    tempCatsArray.append(cat)
                if (i+1) % CATS_PER_INV_PAGE  == 0:
                    p += 1
            catsInventoryMessage = TextFormatter.format_cats_inventory_page(tempCatsArray, page, max_page = maxPage)
        else:
            catsInventoryMessage = "You have no cats :C"
        view = InventoryNavigationView(previousPage, nextPage, previousOff=previousOff, nextOff=nextOff)
        if edit:
            await interaction.response.defer(ephemeral=True)
            await MessageToTextInventoryManager.get_message(interaction.message.id).edit(content=catsInventoryMessage, view=view)
        else :
            message : discord.Message = await interaction.channel.send(catsInventoryMessage, view=view)
            await interaction.response.send_message("Displaying your inventory...", ephemeral=True)
        
        if (not edit):
            MessageToTextInventoryManager.add(message=message, page=page, uid=interaction.user.id)
        
    
    async def show_cat_stats(interaction : discord.Interaction):
        cats : list[Cat] = JSONInventoryManager.get_cats_from_id_as_cats(interaction.user.id)
        com = 0
        sp  = 0
        rar = 0
        sr  = 0
        ur  = 0
        lr  = 0
        for cat in cats:
            rarity = CatModel.get_cat_property(cat, "rarity")
            if rarity   == "common":
                com += 1
            elif rarity == "special":
                sp += 1
            elif rarity == "rare":
                rar += 1
            elif rarity == "super_rare":
                sr += 1
            elif rarity == "uber_rare":
                ur += 1
            elif rarity == "legend_rare":
                lr += 1

        await interaction.response.send_message(f"""
            You have : 
        - - {com} Common cat{"s" if com > 1 else ""}
        - - {sp} Special cat{"s" if sp > 1 else ""}
        - - {rar} *Rare* cat{"s" if rar > 1 else ""}
        - - {sr} **Super rare** cat{"s" if sr > 1 else ""}
        - - {ur} ***Uber rare*** cat{"s" if ur > 1 else ""}
        - - {lr} __***Legend rare***__ cat{"s" if lr > 1 else ""}
        """)

    async def DEBUG_force_summon_cat_in_channel(channel : discord.TextChannel, catName = None, message : discord.Message = None):
        """DEPRECATED ! DEBUG !!! Used to summon cats for debug purposes 

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
        Logger.log(f"Added {catToSummon} to {message_sent.id} ", debug_level=3)
        return message_sent

    def get_random_cat_by_rarity(rarity : str):
        """Gets a random cat from the loaded data

        Args:
            rarity (str): The rarity to look for. eg : "super_rare" | "common"

        Returns:
            Cat: The cat
        """
        if rarity == "common":
            return random.choice(common_cats)
        elif rarity == "rare":
            return random.choice(rare_cats)
        elif rarity == "super_rare":
            return random.choice(super_rare_cats)
        elif rarity == "uber_rare":
            return random.choice(uber_rare_cats)
        elif rarity == "legend_rare":
            return random.choice(legend_rare_cats)
        else: Logger.log("Rarity doesn't exist")

    async def summon_cat_in_channel(cat : Cat, channel : discord.TextChannel):
        """Summons a cat in the specified channel

        Args:
            cat (Cat | str): The cat to summon
            channel (discord.TextChannel): The TextChannel to summon the cat in
        """
        view = discord.ui.View()
        button = CatchButton()
        button.callback = try_capture_cat
        view.add_item(button)
        if type(cat) is type(""):
            cat = CatModel.get_cat_from_name(cat)
        message : discord.Message = await channel.send(
            f"A **{RARITY_MAP[ str.upper(CatModel.get_cat_property(cat, 'rarity'))]}** {cat.name}  appeared ! Quick, catch it first!",
            file=discord.File( CatModel.get_cat_image_image_fullpath(cat)),
            view=view
            )
        MessageToCat.add(message, cat)


    async def try_summon_cat_encounter(channel : discord.TextChannel, override_luck = False):
        """Tries to summon a cat depending on it's rarity, called verytime a message is sent

        Args:
            channel (discord.TextChannel): The channel in which to summon the cat
        """
        # First define if a cat should be summoned
        roll = random.randint(0,100)
        rarity_roll = random.uniform(0,100)
        if override_luck:
            roll = 0
        if not roll < CAT_ENCOUNTER_CHANCE:
            return
        
        if rarity_roll < RARITY_SUMMON_CHANCE["LEGEND_RARE"]:
            await summon_cat_in_channel(get_random_cat_by_rarity("legend_rare"), channel)
        elif rarity_roll < RARITY_SUMMON_CHANCE["UBER_RARE"]:
            await summon_cat_in_channel(get_random_cat_by_rarity("uber_rare"), channel)
        elif rarity_roll < RARITY_SUMMON_CHANCE["SUPER_RARE"]:
            await summon_cat_in_channel(get_random_cat_by_rarity("super_rare"), channel)
        elif rarity_roll < RARITY_SUMMON_CHANCE["RARE"]:
            await summon_cat_in_channel(get_random_cat_by_rarity("rare"), channel)
        else:
            await summon_cat_in_channel(get_random_cat_by_rarity("common"), channel)

            
        


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
    """
    async def command_cats(message : discord.Message,):
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
    """    

    async def command_items(message : discord.Message, args: list[str]):
        Logger.log("Executing command 'items'", 3)
        if args[0]=="show":
            await message.reply("You used the show command")
        else:
            await message.reply(f"Command {args[0]} not yet implemented")

    async def try_capture_cat(interaction : discord.Interaction):
        """Capture a summoned cat
        """
        uid ,mid = interaction.user.id, interaction.message.id
        capturedCat = MessageToCat.get_cat(mid)
        try:
            JSONInventoryManager.add_cat_to_player_inventory(
                uid,
                capturedCat
            )
        except CatAlreadyInInventoryException:
            # TRANSLATE
            await interaction.response.send_message("You already have this cat !", ephemeral=True)
            return
        except Exception as e:
            raise e
        
        await interaction.message.delete()
        await interaction.channel.send("<@" + str(uid) + f"> Captured {capturedCat.name} !")

        
    """  Text command management DEPRECATED: using slash commands now
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
    """
    # -- Events
    @client.event
    async def on_ready():
        # -- Init members/guilds
        guilds = [guild async for guild in client.fetch_guilds(limit=15)]
        tmembers = []
        await command_tree.sync(guild=None)
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
            await client.get_guild(1041000718489882634).get_channel(MAIN_CHANNEL_ID).send("We're alive!")


    # -- On reaction add event
    @client.event
    async def on_reaction_add(reaction : discord.Reaction, user : discord.Member):
        print(f"Reaction added from {user.name}")
        channel : discord.TextChannel = reaction.message.channel
        #send("<@" + str(user_id) + ">")
        if user == client.user:
            return

    

    # -- On message Event
    @client.event
    async def on_message(message : discord.Message):
        """On message event \n
        Contains the command processing instructions(Not anymore, now uses / commands) as well as the cat encounter mechanics

        Args:
            message (discord.Message): The message gathered from the event
        """
        Logger.log(f"event.on_message : Message from {message.author.name} : {message.content}", debug_level=3)

        if message.author == client.user or message.author.bot:
            return
        
        # What should happen when a message is posted
        await try_summon_cat_encounter(message.channel)


        """ DEPRECATED (User commands)
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
        """
        

    # -- Bot Slash Commands

    # --- User commands
    # ---- Cats
    @command_tree.command(name= "show_cats", description="Show cats from your inventory")
    async def command_show_cats(interaction : discord.Interaction, page : int = 1):
        await show_cats_from_player_inventory(interaction, page=page)

    
    @command_tree.command(name= "cat_stats", description="Displays statistics about the cats you own")
    async def command_show_cat_stats(interaction : discord.Interaction):
        await show_cat_stats(interaction)
        

    # ---- Inventory
    @command_tree.command(name= "show_items", description="Show your items")
    async def command_show_items(interaction : discord.Interaction):
        await interaction.response.send_message("Not implemented")

    # --- Developer commands
    @command_tree.command(name= "summon", description="DEBUG : Summons a cat", guild=dev_guild)
    async def summon_command(interaction : discord.Interaction, cat_name: str = None, rarity : str = None):
        #Creates a cat with either parameters
        if cat_name is not None:
            try:
                await summon_cat_in_channel(cat_name, interaction.channel)
            except Exception as e:
                await interaction.response.send_message(e)
            return
        elif rarity is not None :
            # Create cat from rarity
            cat = get_random_cat_by_rarity(rarity)
            await summon_cat_in_channel(cat, interaction.channel)
        else:
            await try_summon_cat_encounter(interaction.channel, override_luck=True)
        await interaction.response.send_message("Done")

    @command_tree.command(name= "test_button", description="DEBUG : Button test" , guild=dev_guild)
    async def DEBUG_button_test(interaction : discord.Interaction):
        

        await interaction.channel.send(view=CatchCatMessageView(try_capture_cat))
        await interaction.response.defer()
        
    
    # Running server    
    client.run(token)