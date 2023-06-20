import discord
import game_manager
from character_sheet import CharacterSheet
from cards import generic_deck
from TOKEN import TOKEN

character_list = {}
# test
character_list['1'] = [CharacterSheet('1', 'a', generic_deck), CharacterSheet('1', 'b', generic_deck)]
character_list['2'] = [CharacterSheet('2', 'c', generic_deck), CharacterSheet('2', 'd', generic_deck)]
character_list['3'] = [CharacterSheet('3', 'e', generic_deck), CharacterSheet('3', 'f', generic_deck)]
character_list['4'] = [CharacterSheet('4', 'g', generic_deck), CharacterSheet('4', 'h', generic_deck)]


class MyClient(discord.Client):
    async def on_ready(self):
        print(f'Logged on as {self.user}!')
        self.gameManager = game_manager.GameManager()
        self.gameManager.render()
    async def on_message(self, message):
        print(f'Message from {message.author}: {message.content}')
        if message.author.id != self.user.id:
            self.gameManager.render()
            await message.channel.send(file=discord.File('test_0.png'))

intents = discord.Intents.default()
intents.message_content = True

client = MyClient(intents=intents)

client.run(TOKEN)
gameManager = game_manager.GameManager()
gameManager.new_game([character_list['1'][0], character_list['2'][0]])
gameManager.new_game([character_list['3'][0], character_list['4'][0]])
gameManager.render()
print(gameManager.play_card(character=0, card='0', game_id=0, target=None))
gameManager.render()
