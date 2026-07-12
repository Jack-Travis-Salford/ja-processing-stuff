import json
import os
import re

big_export = []

def kata_to_hira(text):
    return ''.join(
        chr(ord(c) - 0x60) if 'ァ' <= c <= 'ン' else c
        for c in text
    )


def hira_to_kata(text):
    return ''.join(
        chr(ord(c) + 0x60) if 'ぁ' <= c <= 'ん' else c
        for c in text
    )


from collections import Counter
match_count = Counter()

def check_kanas(kana_matches, search_terms):
    for kana in kana_matches:
        word_as_kana = kana["text"]
        if word_as_kana in search_terms:
            return True
        return False


def jmdict_tie_braker(text, jmdict_hits, mecab_part):

    word_kana = "".join(strip_tag(t["kanaBase"]) for t in mecab_part)
    hiragana = kata_to_hira(word_kana)
    katakana = hira_to_kata(word_kana)
    matches = set()


    for potential_hit in jmdict_hits:
        kanas = potential_hit["kana"]
        is_match = check_kanas(kanas, {hiragana, katakana})
        if is_match:
            matches.add(potential_hit["id"])


    if len(matches) == 1:
        match_count.update([1])
        return

    # 2+, attempt tie brake by common. Assumption that one might be common, the other isnt.
    # Check for exact match cases (not orth or kana ver)
    common_hits = set()
    text_match_hits = set()

    for match_id in matches:
        candidate =jmdict_index["by_id"][str(match_id)]

        for kanji_candidate in candidate["kanji"]:
            if kanji_candidate.get("common", False):
                common_hits.add(match_id)
            hit_text = kanji_candidate["text"]
            if hit_text == text:
                text_match_hits.add(match_id)

        for kana_candidate in candidate["kana"]:
            if kana_candidate.get("common", False):
                common_hits.add(match_id)

            hit_text = kana_candidate["text"]
            if hit_text == text:
                text_match_hits.add(match_id)

    len_common_hits = len(common_hits)
    len_text_match_hits = len(text_match_hits)
    len_intersection = len(common_hits.intersection(text_match_hits))

    if 1 in {len_common_hits, len_text_match_hits, len_intersection}:
        match_count.update([1])
        return

    if len_common_hits == len_text_match_hits == len_intersection == 0:
        match_count.update([len(jmdict_hits)])


        return

    min_len = 999
    match_method = False
    if len_common_hits < min_len and  len_common_hits > 0:
        min_len = len_common_hits
        match_method = "common_hits"
    if len_text_match_hits < min_len and  len_text_match_hits > 0:
        min_len = len_text_match_hits
        match_method =  "text_match_hits"
    if len_intersection < min_len and  len_intersection > 0:
        min_len = len_intersection
        match_method = "intersection"

    if 1<min_len<10:
        json_entry = {
            "text": text,
            "lowest_match_method": match_method,
            "lowest_hits_count": min_len,
            "jmdict_hits": jmdict_hits,
            "mecab_part": mecab_part,
        }
        big_export.append(json_entry)
    match_count.update([min_len])

    return



def strip_tag(s):
    return s.split('-')[0] if s else ""

def lookup_candidate(jmdict_index, text, mecab_part):
    # 1. Clean UniDic tags from INDIVIDUAL parts before joining
    # This simply splits at the hyphen and takes the first part.


    # Generate clean versions of both the orthBase and the lemma
    clean_orth_base = "".join(strip_tag(t["orthBase"]) for t in mecab_part)
    clean_orth = "".join(strip_tag(t["orth"]) for t in mecab_part)
    clean_lemma = "".join(strip_tag(t["lemma"]) for t in mecab_part)



    # 3. Search JMdict using both (lemma ensures verb hits, orthBase ensures kana hits)
    search_targets = [(clean_lemma, clean_orth_base),
                         (clean_orth_base, clean_orth_base)]
    if len(mecab_part) > 1:
        search_targets.append((clean_orth, clean_orth))
    # 2. What we actually want on the Anki card is the modern spelling

    # Match by kanji for attempt 1
    for target, display in search_targets:
        if not target:
            continue

        # Check Hiragana dictionary
        val_hira = kata_to_hira(target)
        val_kata = hira_to_kata(target)


        if  hit := jmdict_index["kanji_ver"].get(val_hira, False):
            if len(hit) > 1:
                # print(json.dumps(mecab_part, indent=2, ensure_ascii=False))
                # print()
                # print(json.dumps(hit,indent=2, ensure_ascii=False))
                jmdict_tie_braker(text, hit, mecab_part)

            return display

        if len(val_kata) > 1:
            if hit := jmdict_index["kanji_ver"].get(val_kata, False):
                if len(hit) > 1:
                    # print(json.dumps(mecab_part, indent=2, ensure_ascii=False))
                    # print()
                    # print(json.dumps(hit,indent=2, ensure_ascii=False))
                    jmdict_tie_braker(text, hit, mecab_part)
                return display

    # Match by kana for attempt 2
    for target, display in search_targets:
        if not target:
            continue

        # Check Hiragana dictionary
        val_hira = kata_to_hira(target)
        val_kata = hira_to_kata(target)

        if hit := jmdict_index["kana_ver"].get(val_hira, False):
            if len(hit) > 1:
                # print(json.dumps(mecab_part, indent=2, ensure_ascii=False))
                # print()
                # print(json.dumps(hit, indent=2, ensure_ascii=False))
                jmdict_tie_braker(text, hit, mecab_part)
            return display


        if hit := jmdict_index["kana_ver"].get(val_kata, False):
            if len(hit) > 1:
                # print(json.dumps(mecab_part, indent=2, ensure_ascii=False))
                # print()
                # print(json.dumps(hit, indent=2, ensure_ascii=False))
                jmdict_tie_braker(text, hit, mecab_part)
            return display

    return None

def process_candidates(mecab_parts, p_candidates):
    words = []
    for part, (start, end) in p_candidates:
        candidate_parts = mecab_parts[start:end]
        if word_data := lookup_candidate(jmdict_index, part, candidate_parts):
            words.append(word_data)
    return words



jmdict_index = json.load(open("jmdict_by_key.json", mode='r'))
print("jmdict loaded")
files = []
for file in os.listdir("."):
    if file.startswith("jish_sent_with_mecab_"):
        files.append(file)



#sentences:dict = json.load(open("jish_sent_with_mecab_0.json", encoding='utf-8', mode='r'))
#print("sents loaded")
#sents = list(sentences.items())

x = 0
for file in files:
    print(f"Processing {file}")
    sentences: dict = json.load(open(file, encoding='utf-8', mode='r'))
    sents = list(sentences.items())
    for key, sent in sents:
        if x > 1000:
            break
        print(f"[{x}]")
        x += 1
        print(sent["ja"])
        words = process_candidates(sent["mecab"], sent["p_candidates"])
        print(words)

print(f"Distribution: {match_count}")
print(len(big_export))

json.dump(big_export, open("the_export.json", 'w', encoding='utf-8'), indent=2, ensure_ascii=False)
    # print("\n"*1)
#hira hit: Org;ため、 Match:ため
