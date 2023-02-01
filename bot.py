import os
from typing import List

import discord
from discord.ext import commands
from dotenv import find_dotenv, load_dotenv

from ascii import art
from ship import Ship

dotenv_path = find_dotenv()
load_dotenv(dotenv_path)
TOKEN = os.getenv("TOKEN")

# ------------ INTENTS ARE REQUIRED BY DISCORD
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(
    command_prefix="/",
    intents=intents,
)


# ------------ CREATING BUTTONS WHICH CONTAIN GAME LOGIC
class GridButton(discord.ui.Button):
    """button created by Game() class. contains most game logic.

    Methods:
        callback (discord.Interaction): on click of specific button. Ship() contained in Game() will update players boards with either "/" if hit or "*" if miss. content will be changed accordingly and passed into response.edit_message()
        
        after player1's turn ship will check if player1 has won if so buttons will disable and ai will not get a turn. else ai will take a turn and update players boards.
        
        at the very end both initial message with buttons and followup will be updated properly
    """

    def __init__(self, x: int, y: int, label: str):
        super().__init__(style=discord.ButtonStyle.secondary,
                         label=label,
                         row=y)
        self.x = x
        self.y = y
        self.timeout = 60

    async def callback(self, interaction: discord.Interaction):
        assert self.view is not None
        view: Game = self.view
        ship = view.ship

        # player turn logic
        is_sunk = ship.p2.update_board("/", False,
                                       [self.x, self.y])  # update there board
        if is_sunk:
            ship.p1.update_board("/", True,
                                 [self.x, self.y])  # update your hits board
            self.style = discord.ButtonStyle.success
            content = "HIT! Where would you like to strike next?"
        else:
            ship.p1.update_board("*", True,
                                 [self.x, self.y])  # update your hits board
            self.style = discord.ButtonStyle.danger
            content = "Miss! Where would you like to strike next?"

        if ship.p2.check_winner():
            content = "**You Win!**"
            view.stop()
            for child in view.children:
                child.disabled = True

        # ai turn (does not execute if player wins)
        else:
            missile = ship.p1.gen_cord(*view.exclusions)
            view.exclusions.append(missile)
            is_sunk = ship.p1.update_board("/", False,
                                           missile)  # updates player board
            if is_sunk:
                ship.p2.update_board("/", True,
                                     missile)  #updates ai hits board
            else:
                ship.p2.update_board("*", True,
                                     missile)  #updates ai hits board

            if ship.p1.check_winner():
                content = "**Sorry our ai is TOO POWERFUL, you lose...**"
                view.stop()
                for child in view.children:
                    child.disabled = True

        self.disabled = True  # disable current button that was clicked
        await interaction.response.edit_message(content=content, view=view)
        await view.edit_followup_msg(view.ship.p1.ascii)


# ------------ GAME CLASS CREATION -> THE DISCORD.UI.VIEW
class Game(discord.ui.View):
    """game logic from Ship(). This class is only ran once after the initial slash command. Creates new Ship() game and discord.ui.View.Button 's in the same grid sequence as ship.p2.board

    Attributes:
        player1 (str): name of player1
        player2 (str): name of player2
        ship (Class): Ship() class
        hits : hits board from ship for ease of use
        followup_msg (str): the attribute used to store the initial followup message
        exclusions (list): list of coordinates the ai has already taken
    Methods:
        edit_followup_msg(): used to change the followup message sent to player. 
    """
    children: List[GridButton]

    def __init__(self):
        super().__init__()
        self.player1 = "player1"
        self.player2 = "player2"
        self.ship = Ship()
        self.ship.start_game(self.player1)
        hits = self.ship.p2.hits
        self.followup_msg: discord.Message = None
        self.exclusions: list = []

        # creating the buttons according to ship.board
        y = 0
        for row in hits:
            x = 0
            for space in row:
                self.add_item(GridButton(x, y, space))
                x += 1
            y += 1

    async def edit_followup_msg(self, new_msg):
        """used to change the followup message sent to player. 

        Args:
            new_msg (str): the new message you wish to edit followup_msg with
        """
        if self.followup_msg:
            await self.followup_msg.edit(content=new_msg)


# ------------ INIT BOT
def run_discord_bot():
    """Called in main.py. Starts bot
    """
    bot.run(TOKEN)


@bot.event
async def on_ready():
    """When bot is initialized prints out bot is ready and also syncs all bot commands
    """
    print(f"{bot.user} is now running!")
    try:
        synced = await bot.tree.sync()
        print(f"Synced {len(synced)} command(s)")
    except Exception as e:
        print(e)


# ------------ BOT COMMANDS
# FIXME couldnt get help slash commands to work
@bot.tree.command(name="help_command",
                  description="Displays a list of all Commands")
async def help_command(interaction: discord.Interaction):
    await interaction.response.send_message("Work in progress")


# TODO add 'against' selector in the slash command before member
@bot.tree.command(name="play",
                  description="Start a game against either AI or a friend.")
async def play(interaction: discord.Interaction):
    view = Game()
    await interaction.response.send_message(
        "Your turn, where would you like to attack?", view=view)
    view.followup_msg = await interaction.followup.send(view.ship.p1.ascii,
                                                        ephemeral=True)


@bot.tree.command(name="art", description="Print out a cool piece of art.")
async def artt(interaction: discord.Interaction):
    await interaction.response.send_message(art)


if __name__ == "__main__":
    # run the bot
    run_discord_bot()
