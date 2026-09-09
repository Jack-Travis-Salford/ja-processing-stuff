import json


all_data = json.load(open("./jmdict-eng-3.6.2.json", 'r', encoding='utf-8'))


all_combos = {"kanji_ver":{}, "kana_ver":{}, "by_id":{}}
id_mapping = {}

for _data in all_data["words"]:
    id_mapping[_data["id"]] =  _data

print(all_data.keys())
skip_keys = {"1311125"}
merge_keys = {}

for val in merge_keys.values():
    skip_keys.update(val)

for _data in all_data["words"]:
    d_id = _data["id"]
    if d_id in skip_keys:
        continue
    alternate_meanings = []
    if d_id in merge_keys:
        for alt_meaning in merge_keys[d_id]:
            alternate_meanings.append(id_mapping[alt_meaning])


    compact_sense = []
    for sense in _data["sense"]:
        compact_sense.append({"gloss":sense["gloss"]})

    compact_kanji = []
    for kanji in _data["kanji"]:
        compact_kanji.append({"common": kanji["common"], "text": kanji["text"]})

    compact_kana = []
    for kana in _data["kana"]:
        compact_kana.append({"common": kana["common"], "text": kana["text"]})

    for alt_meaning in alternate_meanings:

        for sense in alt_meaning["sense"]:
            compact_sense.append({"gloss": sense["gloss"]})

        for kanji in alt_meaning["kanji"]:
            compact_kanji.append({"common": kanji["common"], "text": kanji["text"]})

        for kana in alt_meaning["kana"]:
            compact_kana.append({"common": kana["common"], "text": kana["text"]})

    data = {
        "id": _data["id"],
        "kanji":compact_kanji,
        "kana": compact_kana,
        "sense" : compact_sense,
        "alts": alternate_meanings
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