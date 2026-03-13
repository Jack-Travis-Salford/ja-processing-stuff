import json


all_jisho:dict = json.load(open("./files/all_jisho 2 - Copy.json"))
with open("./files/all_jisho_readable.json", mode='w', encoding='utf-8') as writer:
    writer.write(json.dumps(all_jisho, ensure_ascii=False, indent=2))

#print(all_jisho)

#print(json.dumps(all_jisho[all_jisho.keys()[0]] , indent =2))