#!/usr/bin/python3
import argparse
import discord
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

BREEDS_LOWER = dict([(name.lower(), name) for name in NAMES_IDS.keys()])

DOG_EMOJIS = ['🐶', '🐕']


def add_whitespace(text):
    return "".join([(' ' + char if char.isupper() else char) for char in list(text)]).strip()


def get_dog_breed(breed):
    breed = BREEDS_LOWER[breed]
    name = add_whitespace(breed)
    image = BREED_QUEUES[breed].get()
    return 'Here\'s your ' + name + ' dog! ' + image


class DogApiBot(discord.Client):
    async def on_ready(self):
        pass

    async def on_message(self, message):
        if len(message.content) < 2 or message.content[0] != '+':
            return
        command = message.content[1:].lower()
        if command == 'dog' or command in DOG_EMOJIS:
            await message.channel.send('Here\'s your dog! ' + dog_queue.get())
        if command.startswith('dogbreeds'):
            try:
                page = int(command[9:]) - 1
            except:
                page = 0
            await message.channel.send('Breeds: ' + ', '.join(
                ['+' + name for name in NAMES_IDS.keys()][(page*40):(page*40+40)]))
        if command == 'doginvite':
            await message.channel.send(f'Please use this link to invite me to your server: {INVITE_LINK}')
        if command in BREEDS_LOWER:
            await message.channel.send(get_dog_breed(command))
        if command == 'dogservers':
            await message.channel.send("# of servers: " + str(len(self.guilds)))
        if command == 'help':
            await message.channel.send(
                'Thanks for using DogBot! \n' +
                'Commands: \n' +
                '+dog gives you a random dog image \n' +
                '+dogBreeds lists available breeds (e.g. +boxer gives you a Boxer dog) \n' +
                '+dogBreeds2 to list second page of breeds (there are 5 pages) \n' +
                '+dogInvite to invite me to another server \n' +
                '+help shows this message \n' +
                f'Any concerns, PM {CREATOR} on Discord.')


intents = discord.Intents.default()
intents.message_content = True

client = DogApiBot(intents=intents)
client.run(API_TOKEN)
