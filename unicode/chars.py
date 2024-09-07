import json
import unicodedata

print(chr(140000))

#dict = {}
string = ""
for i in range(int(0x10ffff)):
    character = chr(i)
    try:
        key = unicodedata.name(character)
    except ValueError:
        key = character
    #dict[key] = character
    string += key + " " + character
    print(i)
print('done')
with open("chars.txt", "w", encoding="utf-8") as f:
    f.write(string)
# json.dump(string, open("chars.json", "w", encoding="utf-8"), ensure_ascii=False)
