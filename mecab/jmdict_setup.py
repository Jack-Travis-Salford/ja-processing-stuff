import json


all_data = json.load(open("./jmdict-eng-3.6.2.json", 'r', encoding='utf-8'))


all_combos = {"kanji_ver":{}, "kana_ver":{}, "by_id":{}}

print(all_data.keys())

for _data in all_data["words"]:
    compact_sense = []
    for sense in _data["sense"]:
        compact_sense.append({"gloss":sense["gloss"]})

    compact_kanji = []
    for kanji in _data["kanji"]:
        compact_kanji.append({"common": kanji["common"], "text": kanji["text"]})

    compact_kana = []
    for kana in _data["kana"]:
        compact_kana.append({"common": kana["common"], "text": kana["text"]})

    data = {
        "id": _data["id"],
        "kanji":compact_kanji,
        "kana": compact_kana,
        "sense" : compact_sense
    }
    for kanji_opt in data["kanji"]:
        kanji_opt_text = kanji_opt["text"]
        all_combos["kanji_ver"].setdefault(kanji_opt_text, []).append(data)

    for kana_opt in data["kana"]:
        kana_opt_text = kana_opt["text"]
        all_combos["kana_ver"].setdefault(kana_opt_text, []).append(data)

    all_combos["by_id"][data["id"]] = data

#json.dump(all_combos, open("jmdict_by_key.json", 'w'))
json.dump(all_combos, open("jmdict_by_key.json", 'w'))
json.dump(all_combos, open("jmdict_by_key_readable.json", 'w', encoding='utf-8'), indent=2, ensure_ascii=False)

print(len(all_combos))