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

        Returns:
            coro
        """
        raise CallbackNotChangedException

class ButtonNextPage(discord.ui.Button):
    def __init__(self, disabled = False):
        super().__init__(style=discord.ButtonStyle.blurple, label=">>", disabled=disabled)
    async def callback(self, interaction: discord.Interaction):
        """Callback the will be used to go to next page

        Args:
            interaction (discord.Interaction): Discord interaction

        Returns:
            coro
        """
        raise CallbackNotChangedException
class ButtonPreviousPage(discord.ui.Button):
    def __init__(self, disabled = False):
        super().__init__(style=discord.ButtonStyle.blurple, label="<<", disabled=disabled)
    
    async def callback(self, interaction: discord.Interaction):
        """Callback the will be used to go to previous page

        Args:
            interaction (discord.Interaction): Discord interaction

        Returns:
            coro
        """
        return await super().callback(interaction)