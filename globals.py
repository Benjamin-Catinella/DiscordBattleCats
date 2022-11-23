from utils import Logger
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
CATS_PER_INV_PAGE = 7

# Other
MAIN_CHANNEL_ID = 1041000719467151392
DEV_SERVER_ID = 1041000718489882634
DEBUG = True
print(f"Logger debug level set to {Logger.DEBUG_LEVEL}")

# Cat encounter
CAT_ENCOUNTER_CHANCE = 2
CAT_ENCOUNTER_CHANCE_BONUS = 6
REACTIONS = {
    "catch" : "🟩",
    "no"    : "❌"
}
RARITY_MAP = {
    "COMMON" : "Common",
    "SPECIAL" : "Special",
    "RARE" : "Rare",
    "SUPER_RARE" : "Super rare",
    "UBER_RARE" : "Uber rare",
    "LEGEND_RARE" : "Legend rare"
}
RARITY_ID = {
    "COMMON" : 1,
    "SPECIAL" : 2,
    "RARE" : 3,
    "SUPER_RARE" : 4,
    "UBER_RARE" : 5,
    "LEGEND_RARE" : 6
}
RARITY_SUMMON_CHANCE = {
    "COMMON"        : 50,
    "RARE"          : 31,
    "SUPER_RARE"    : 15,
    "UBER_RARE"     : 3.5,
    "LEGEND_RARE"   : 0.5
}