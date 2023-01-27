import os

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
class Test(discord.ui.View):
    """docstring for Confirm."""

    def __init__(self):
        super().__init__()
        self.value = None
        self.timeout = 5

    @discord.ui.button(label="confirm", style=discord.ButtonStyle.green)
    async def confirm(self, interaction: discord.Interaction,
                      button: discord.ui.Button):
        await interaction.response.send_message("Confirming")
        self.value = True
        self.stop()

    @discord.ui.button(label="cancel", style=discord.ButtonStyle.grey, row=1)
    async def cancel(self, interaction: discord.Interaction,
                     button: discord.ui.Button):
        await interaction.response.send_message("cancelling")
        self.value = False
        self.stop()


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
    view = Test()
    await interaction.response.send_message(
        "Your turn, where would you like to attack?", view=view)
    if view.value is None:
        print("timed out..")
    elif view.value:
        print("confirmed")
    else:
        print("canceled")


if __name__ == "__main__":
    # run the bot
    run_discord_bot()
