import json


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

# def lookup_candidate(jmdict_index, word_parts):
#     """
#     Try to find a match in jmdict_index for a candidate.
#     Returns jmdict entry or None.
#     """
#     # Build list of keys to try, in order of preference
#     if len(word_parts) == 1:
#         wp = word_parts[0]
#         keys_to_try = [
#             wp["orth"],
#             wp["orthBase"],
#             wp["lemma"],
#             kata_to_hira(wp["kanaBase"]),
#         ]
#     else:
#         # composite: join each field across tokens
#         keys_to_try = [
#             ''.join(t["orth"] for t in word_parts),
#             ''.join(t["orthBase"] for t in word_parts),
#             ''.join(t["lemma"] for t in word_parts),
#             kata_to_hira(''.join(t["kanaBase"] for t in word_parts)),
#         ]
#
#     for key in keys_to_try:
#         if key and key in jmdict_index:
#             return jmdict_index[key]
#
#     return None

def lookup_candidate(jmdict_index, text,  mecab_part):
    word_parts = mecab_part
    opts = {
        "orthBase": ''.join(t["orthBase"] for t in word_parts),
        "lemma": ''.join(t["lemma"] for t in word_parts),
        "orth": ''.join(t["orth"] for t in word_parts),
    }

    # Check all possible kanji permutations
    for key, val in opts.items():
        if not val:
            continue
        # Ensure all kana is hira
        val_hira = kata_to_hira(val)
        if val_hira in jmdict_index["kanji_ver"]:
            print(f"{key} hira hit: Org;{text} Match:{val_hira}")
            return text

        val_kata = hira_to_kata(val)
        if val_kata in jmdict_index["kanji_ver"]:
            print(f"{key} kana hit: Org;{text} Match:{val_kata}")
            return text

    # If none, try kana matching
    kana = "".join(t["kanaBase"] for t in word_parts)
    if len(kana) < 2:
        return None
    hiragana = kata_to_hira(kana)
    if hiragana in jmdict_index["kanji_ver"]:
        print(f"hira hit: Org;{text} Match:{hiragana}")
        return text
    if hiragana in jmdict_index["kana_ver"]:
        print(f"hira hit: Org;{text} Match:{hiragana}")
        return text

    katakana = hira_to_kata(kana)
    if katakana in jmdict_index["kanji_ver"]:
        print(f"kata hit:{text} Match:{katakana}")
        return text
    if katakana in jmdict_index["kana_ver"]:
        print(f"kata hit:{text} Match:{katakana}")
        return text

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
sentences:dict = json.load(open("jish_sent_with_mecab_0.json", encoding='utf-8', mode='r'))
print("sents loaded")
sents = list(sentences.items())[:26]

x = 0
for key, sent in sents:
    print(f"[{x}]")
    x += 1
    print(sent["ja"])
    words = process_candidates(sent["mecab"], sent["p_candidates"])
    print(words)
    print("\n"*1)
#hira hit: Org;ため、 Match:ため
