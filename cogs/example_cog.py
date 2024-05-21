from discord.ext import commands

class ExampleCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def hello(self, ctx):
        guild_config = self.bot.config(ctx.guild.id)
        await ctx.send(f'Hello! Guild setting is: {guild_config}')

async def setup(bot):
    await bot.add_cog(ExampleCog(bot))
