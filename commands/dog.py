#!/usr/bin/python3
from telegram.ext import CommandHandler
from urllib.request import urlopen
from functools import partial

from .breeds import NAMES_IDS

import json
import threading
import queue
import time

DOG_API_URL = 'https://api.thedogapi.com/v1/images/search?mime_types=png,jpg'
BREED_URL = 'https://api.thedogapi.com/v1/images/search?mime_types=png,jpg&breed_ids='

def load_dog_url(url):
    json_data = json.loads(urlopen(url).read())
    return json_data[0].get('url')


class DogQueue():
    def __init__(self, breeds=None, capacity=10):
        self.queue = queue.Queue(capacity)
        if breeds == None:
            self.url = DOG_API_URL
        else:
            self.url = BREED_URL + ",".join(breeds)
        self.thread = threading.Thread(target=self.dog_pusher, daemon=True)
        self.thread.start()

    def dog_pusher(self):
        while True:
            self.queue.put(load_dog_url(self.url))

    def get(self):
        return self.queue.get()

    def size(self):
        return self.queue.qsize()


if __name__ == "__main__":
    dog_queue = DogQueue(breeds=['242'])
    while True:
        input("Press enter to fetch a dog\n")
        file_name = dog_queue.get()
        print(file_name)
        print("Size: " + str(dog_queue.size()))
