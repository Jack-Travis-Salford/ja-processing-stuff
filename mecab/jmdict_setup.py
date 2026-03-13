import json
from xml.etree.ElementTree import indent

all_data = json.load(open("./jmdict-eng-3.6.2.json", 'r', encoding='utf-8'))


all_combos = {"kanji_ver":{}, "kana_ver":{}}

print(all_data.keys())

for data in all_data["words"]:
    for kanji_opt in data["kanji"]:
        kanji_opt_text = kanji_opt["text"]
        all_combos["kanji_ver"].setdefault(kanji_opt_text, []).append(data)

    for kana_opt in data["kana"]:
        kana_opt_text = kana_opt["text"]
        all_combos["kana_ver"].setdefault(kana_opt_text, []).append(data)

#json.dump(all_combos, open("jmdict_by_key.json", 'w'))
json.dump(all_combos, open("jmdict_by_key.json", 'w'))
json.dump(all_combos, open("jmdict_by_key_readable.json", 'w', encoding='utf-8'), indent=2, ensure_ascii=False)

print(len(all_combos))