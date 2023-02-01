# LIST OF THINGS TO DO FOR THE BOT IN GENERAL

1. Profile pic
2. board and pieces images
3. image generation based on the outputed board logic
4. eventually were going to have to move the sync commands to some admin slash commands
   1. @bot.command()
      async def synccmd(ctx):
        fmt = await ctx.bot.tree.sync(guild=ctx.guild)
        await ctx.send(
          f"Syncd {len(fmt)} commands to the crrent server"
        )
        return

        https://stackoverflow.com/questions/74958199/python-discord-py-slash-command-doesnt-show-up-in-server
5. 