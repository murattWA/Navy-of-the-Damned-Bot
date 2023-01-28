import os
from typing import List

import discord
from discord.ext import commands
from dotenv import find_dotenv, load_dotenv

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


# ------------ CREATING BUTTON CLASS
class Test(discord.ui.Button):
    """docstring for Confirm."""

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
            print("You Win!")
            content = "You Win!"
            view.stop()
            for child in view.children:
                child.disabled = True

        await interaction.response.edit_message(content=content, view=view)

    # @discord.ui.button(label="confirm", style=discord.ButtonStyle.green)
    # async def confirm(self, interaction: discord.Interaction,
    #                   button: discord.ui.Button):
    #     await interaction.response.send_message("Confirming")
    #     self.value = True
    #     self.stop()

    # @discord.ui.button(label="cancel", style=discord.ButtonStyle.grey, row=1)
    # async def cancel(self, interaction: discord.Interaction,
    #                  button: discord.ui.Button):
    #     await interaction.response.send_message("cancelling")
    #     self.value = False
    #     self.stop()


# ------------ GAME CLASS CREATION -> THE DISCORD.UI.VIEW
class Game(discord.ui.View):
    """docstring for Game."""
    children: List[Test]

    def __init__(self):
        super().__init__()
        self.player1 = "player1"
        self.player2 = "player2"
        self.ship = Ship()
        self.ship.start_game(self.player1)
        hits = self.ship.p2.hits

        # creating the buttons according to ship.board
        y = 0
        for row in hits:
            x = 0
            for space in row:
                self.add_item(Test(x, y, space))
                x += 1
            y += 1

        # debugging
        self.ship.p2.print_board()


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


if __name__ == "__main__":  # remove this section when done
    # run the bot
    run_discord_bot()
