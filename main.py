from parse import parse
import json

info = []

for mortgage in range(6, 7):
    info = parse(mortgage)
    print(info)

with open('info_flats.json', 'w', encoding='utf-8') as file:
    json.dump(info, file, ensure_ascii=False)