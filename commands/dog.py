#!/usr/bin/python3
from urllib.request import urlopen

import json

DOG_API_URL = 'https://api.thedogapi.com/v1/images/search?mime_types=png,jpg'
BREED_URL = 'https://api.thedogapi.com/v1/images/search?mime_types=png,jpg&breed_ids='


def load_dog_url(url):
    json_data = json.loads(urlopen(url).read())
    return json_data[0].get('url')


class DogQueue():
    def __init__(self, breeds=None):
        if breeds == None:
            self.url = DOG_API_URL
        else:
            self.url = BREED_URL + ",".join(breeds)

    def get(self):
        return load_dog_url(self.url)


if __name__ == "__main__":
    dog_queue = DogQueue(breeds=['242'])
    while True:
        input("Press enter to fetch a dog\n")
        file_name = dog_queue.get()
        print(file_name)
