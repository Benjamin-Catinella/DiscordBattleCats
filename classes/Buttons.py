from typing import Optional, Union
import discord
from .Exceptions import CallbackNotChangedException
class CatchButton(discord.ui.Button):
    def __init__(self):
        super().__init__(style = discord.ButtonStyle.green, label="Catch!")


    async def callback(self, interaction: discord.Interaction):
        """Callback the will be used to catch a cat

        Args:
            interaction (discord.Interaction): Discord interaction
            mid (_type_): Message id
            uid (_type_): User id

        Returns:
            nothing
        """
        raise CallbackNotChangedException