from network.models import *
import json
from pprint import pprint


with open("MOCK_DATA.json", "r") as file:
    data = json.load(file)

for row in data:
    Post.objects.create(**row)