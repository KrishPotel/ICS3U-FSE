import json

file = open("example.json")
f = json.load(file)

print(f["Settings"])