#!/usr/bin/python3
import argparse
import discord
from discord import app_commands
from commands.dog import DogQueue
from commands.breeds import NAMES_IDS

parser = argparse.ArgumentParser(description='Run a discord bot.')
parser.add_argument('--token', type=str,
                    help='API token for the discord bot, retrieved from https://discord.com/developers')
parser.add_argument('--client_id', type=str,
                    help='Client ID of the bot, retrieved from https://discord.com/developers')
parser.add_argument('--creator', type=str,
                    help='Discord ID of the creator of this bot, that\'s you!')
args = parser.parse_args()

CLIENT_ID = args.client_id
API_TOKEN = args.token
CREATOR = args.creator

INVITE_LINK = f'https://discord.com/oauth2/authorize?client_id={CLIENT_ID}&scope=bot&permissions=2048'

dog_queue = DogQueue()

BREED_QUEUES = {}
for name, breed_id in NAMES_IDS.items():
    BREED_QUEUES[name] = DogQueue(breeds=[breed_id])


def add_whitespace(text):
    return "".join([(' ' + char if char.isupper() else char) for char in list(text)]).strip()


def get_dog_breed(breed):
    name = add_whitespace(breed)
    image = BREED_QUEUES[breed].get()
    return 'Here\'s your ' + name + ' dog! ' + image


def breed_list_chunks():
    # ponytail: Discord caps a message at 2000 chars; ~160 breeds overflow, so pack into lines
    chunks, cur = [], ''
    for name in NAMES_IDS:
        piece = (', ' if cur else '') + name
        if len(cur) + len(piece) > 1900:
            chunks.append(cur)
            cur = name
        else:
            cur += piece
    if cur:
        chunks.append(cur)
    return chunks


class DogApiBot(discord.Client):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.tree = app_commands.CommandTree(self)

    async def setup_hook(self):
        await self.tree.sync()


intents = discord.Intents.default()
client = DogApiBot(intents=intents)


@client.tree.command(name='dog', description='Get a random dog image')
async def dog(interaction: discord.Interaction):
    await interaction.response.send_message('Here\'s your dog! ' + dog_queue.get())


@client.tree.command(name='dogbreeds', description='List available dog breeds')
async def dogbreeds(interaction: discord.Interaction):
    chunks = breed_list_chunks()
    await interaction.response.send_message('Breeds: ' + chunks[0])
    for chunk in chunks[1:]:
        await interaction.followup.send(chunk)


@client.tree.command(name='breed', description='Get a dog of a specific breed')
@app_commands.describe(name='The breed of dog you want')
async def breed(interaction: discord.Interaction, name: str):
    if name not in NAMES_IDS:
        await interaction.response.send_message(
            f'Unknown breed "{name}". Use /dogbreeds to see the list.', ephemeral=True)
        return
    await interaction.response.send_message(get_dog_breed(name))


@breed.autocomplete('name')
async def breed_autocomplete(interaction: discord.Interaction, current: str):
    # ponytail: Discord caps choices at 25, so filter by what's typed and slice
    matches = [n for n in NAMES_IDS if current.lower() in n.lower()]
    return [app_commands.Choice(name=add_whitespace(n), value=n) for n in matches[:25]]


@client.tree.command(name='doginvite', description='Get a link to invite the bot to your server')
async def doginvite(interaction: discord.Interaction):
    await interaction.response.send_message(
        f'Please use this link to invite me to your server: {INVITE_LINK}')


client.run(API_TOKEN)
