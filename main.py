import os
import json
import discord
from discord.ext import commands

TOKEN = os.getenv('TOKEN')

# Guild設定のデフォルトテンプレート
DEFAULT_GUILD_CONFIG = {
    "prefix": "!",
    "log_channel_id": None,
    "admin_role_id": None,
    "approved_role_id": None
}

def load_guild_config(guild_id):
    config_path = f'guild/{guild_id}.json'
    if not os.path.exists(config_path):
        with open(config_path, 'w') as config_file:
            json.dump(DEFAULT_GUILD_CONFIG, config_file, indent=4)
    with open(config_path, 'r') as config_file:
        return json.load(config_file)

def get_prefix(bot, message):
    guild_id = message.guild.id
    config = bot.config(guild_id)
    return config.get("prefix", "!")

if __name__ == "__main__":
    if TOKEN is None:
        raise ValueError("No TOKEN environment variable set")    

    intents = discord.Intents.all()
    intents.messages = True
    intents.message_content = True

    bot = commands.Bot(command_prefix=get_prefix, intents=intents)

    bot.config = load_guild_config

    @bot.event
    async def setup_hook():
        for filename in os.listdir('./cogs'):
            if filename.endswith('.py'):
                try:
                    await bot.load_extension(f'cogs.{filename[:-3]}')
                except Exception as e:
                    print(f"拡張機能{filename[:-3]}のロードに失敗しました: {e}")

    @bot.event
    async def on_ready():
        print(f'Logged in as {bot.user}')

    @bot.event
    async def on_guild_join(guild):
        load_guild_config(guild.id)

    @bot.command()
    @commands.has_permissions(administrator=True)
    async def setconfig(ctx, key: str, value: str):
        guild_id = ctx.guild.id
        config = bot.config(guild_id)
        config[key] = value
        config_path = f'guild/{guild_id}.json'
        with open(config_path, 'w') as config_file:
            json.dump(config, config_file, indent=4)
        await ctx.send(f'Set {key} to {value} for this guild.')

    bot.run(TOKEN)

