import discord
import game_manager
from character_sheet import CharacterSheet
from cards import generic_deck
from TOKEN import TOKEN
import logging
from discord import app_commands

handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
MY_GUILD = discord.Object(id=1112196248921972746)  # replace with your guild id


class MyClient(discord.Client):
    def __init__(self, *, intents: discord.Intents):
        super().__init__(intents=intents)
        # A CommandTree is a special type that holds all the application command
        # state required to make it work. This is a separate class because it
        # allows all the extra state to be opt-in.
        # Whenever you want to work with application commands, your tree is used
        # to store and work with them.
        # Note: When using commands.Bot instead of discord.Client, the bot will
        # maintain its own tree instead.
        self.tree = app_commands.CommandTree(self)

    # In this basic example, we just synchronize the app commands to one guild.
    # Instead of specifying a guild to every command, we copy over our global commands instead.
    # By doing so, we don't have to wait up to an hour until they are shown to the end-user.
    async def setup_hook(self):
        # This copies the global commands over to your guild.
        self.tree.copy_global_to(guild=MY_GUILD)
        await self.tree.sync(guild=MY_GUILD)


intents = discord.Intents.default()
client = MyClient(intents=intents)


@client.tree.command()
async def hello(interaction: discord.Interaction):
    """Says hello!"""
    await interaction.response.send_message(f'Hi, {interaction.user.mention}')

# TODO: how can I use the add function in another project where a second discord bot can use the same event?
@client.tree.command()
@app_commands.describe(
    first_value='The first value you want to add something to',
    second_value='The value you want to add to the first value',
)
async def add(interaction: discord.Interaction, first_value: int, second_value: int = 2):
    """Adds two numbers together."""
    await interaction.response.send_message(f'{first_value} + {second_value} = {first_value + second_value}')

@client.event
async def on_ready():
    global gameManager
    print(f'Logged in as {client.user} (ID: {client.user.id})')
    print('------')
    gameManager = game_manager.GameManager()
    gameManager.render()

# This context menu command only works on members
@client.tree.context_menu(name='Show Join Date')
async def show_join_date(interaction: discord.Interaction, member: discord.Member):
    # The format_dt function formats the date time into a human readable representation in the official client
    await interaction.response.send_message(f'{member} joined at {discord.utils.format_dt(member.joined_at)}')

# This context menu command only works on messages
@client.tree.context_menu(name='Report to Moderators')
async def report_message(interaction: discord.Interaction, message: discord.Message):
    # We're sending this response message with ephemeral=True, so only the command executor can see it
    await interaction.response.send_message(
        f'Thanks for reporting this message by {message.author.mention} to our moderators.', ephemeral=True
    )

    # Handle report by sending it into a log channel
    log_channel = interaction.guild.get_channel(0)  # replace with your channel id

    embed = discord.Embed(title='Reported Message')
    if message.content:
        embed.description = message.content

    embed.set_author(name=message.author.display_name, icon_url=message.author.display_avatar.url)
    embed.timestamp = message.created_at

    url_view = discord.ui.View()
    url_view.add_item(discord.ui.Button(label='Go to Message', style=discord.ButtonStyle.url, url=message.jump_url))

    await log_channel.send(embed=embed, view=url_view)

character_list = {}
# test
character_list['1'] = [CharacterSheet('1', 'a', generic_deck), CharacterSheet('1', 'b', generic_deck)]
character_list['2'] = [CharacterSheet('2', 'c', generic_deck), CharacterSheet('2', 'd', generic_deck)]
character_list['3'] = [CharacterSheet('3', 'e', generic_deck), CharacterSheet('3', 'f', generic_deck)]
character_list['4'] = [CharacterSheet('4', 'g', generic_deck), CharacterSheet('4', 'h', generic_deck)]

# gameManager = game_manager.GameManager()
# gameManager.new_game([character_list['1'][0], character_list['2'][0]])
# gameManager.new_game([character_list['3'][0], character_list['4'][0]])
# gameManager.render()
# print(gameManager.play_card(character=0, card='0', game_id=0, target=None))
# gameManager.render()
#

try:
    client.run(TOKEN, log_handler=handler, log_level=logging.DEBUG)
except discord.errors.HTTPException as e:
    print(f'\n\n\nBLOCKED BY RATE LIMITS\nRESTARTING...\n{e}')