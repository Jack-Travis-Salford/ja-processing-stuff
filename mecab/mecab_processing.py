import json


from fugashi import Tagger
from tqdm import tqdm

pos1_translation = {
    "名詞": "Noun",
    "助詞": "Particle",
    "動詞": "Verb",
    "補助記号": "Aux symbols",
    "接尾辞": "Suffix",
    "形状詞": "Adjective",
    "助動詞": "Aux verb",
    "副詞": "Adverb",
    "代名詞": "Pronoun",
    "形容詞": "Adjective",
    "接頭辞": "Prefix",
    "連体詞": "Adnominal",
    "接続詞": "Conjunction",
    "感動詞": "Interjection",
    "記号": "Symbol",
    "空白": "Blank"
}

pos2_translation = {
    "普通名詞": "Common Noun",
    "格助詞": "Case Particle",
    "接続助詞": "Conjunction",
    "一般": "General",
    "非自立可能": "Non-independent",
    "読点": "Comma",
    "名詞的": "Noun",
    "係助詞": "Particle",
    "句点": "Period",
    "副助詞": "Adverb",
    "助動詞語幹": "Aux verb stem",
    "固有名詞": "Proper noun",
    "接頭辞": "Prefix",
    "代名詞": "Pronoun",
    "数詞": "Numeral",
    "準体助詞": "Quasi-body particle",
    "終助詞": "Final particle",
    "括弧開": "Parenthesis open",
    "括弧閉": "Parenthesis closing",
    "形容詞的": "Adjective",
    "形状詞的": "Morphological",
    "タリ": "Tali",
    "フィラー": "Filler",
    "動詞的": "verb-like",
    "文字": "Character"
}

pos3_translation = {
    "一般": "General",
    "副詞可能": "Adverb possible",
    "サ変可能": "SA possible",
    "地名": "Place names",
    "形状詞可能": "Shape word possible",
    "助数詞可能": "Particle possible",
    "助数詞": "Particle noun",
    "サ変形状詞可能": "sa inflection verb possible",
    "人名": "Persons name"
}

pos4_translation = {"国":"Country", "一般":"General", "名": "Name", "姓": "Last name"}

SKIP_POS1 = {"補助記号", "記号", "空白", "助動詞"}
BREAK_POS2 = {
    "読点",      # Comma
    "句点",      # Period
    "終助詞",    # Sentence-ending particles
    "括弧開",    # Opening bracket
    "括弧閉",    # Closing bracket
    "フィラー",  # Filler
}
tagger = Tagger()


def get_word_candidates(sentence, max_window=6):
    """
    sentence: raw Japanese string
    returns: list of (str_word, [[orth, lemma, kana, pos1, pos2, pos3, pos4], ...])
    """
    if sentence == "今やドラマや映画に引っ張りだこで、数々の作品の主演を務める俳優が、かつて10年以上の下積み時代があったと知って驚いた。":
        pass
    word_parts = []
    count = 0
    for word in tagger(sentence):
        f = word.feature

        word_parts.append({
            "count":  count,
            "orth": f.orth or word.surface,
            "orthBase": f.orthBase or word.surface,
            "kanaBase": f.kanaBase or "",
            "lemma": f.lemma or word.surface,
            "cForm": f.cForm or "",
            "cType": f.cType or "",
            "pos1": {
                "ja": f.pos1,
                "en": pos1_translation.get(f.pos1,f.pos1)
            },
            "pos2": {
                "ja": f.pos2,
                "en": pos2_translation.get(f.pos2,f.pos2)
            },
            "pos3": {
                "ja": f.pos3,
                "en": pos3_translation.get(f.pos3,f.pos3)
            },
            "pos4": {
                "ja": f.pos4,
                "en": pos4_translation.get(f.pos4,f.pos4)
            }
        })
        count += 1
    candidates = []
    n = len(word_parts)

    for start in range(n):
        break_after_add = False
        if word_parts[start]["pos1"]["ja"] in SKIP_POS1:
            continue
        if word_parts[start]["pos2"]["ja"] in BREAK_POS2:
            continue

        for window in range(1, max_window + 1):
            end = start + window
            if end > n:
                break

            # No word is likely to have comma, break if encountered
            if word_parts[end-1]["pos2"]["ja"] in BREAK_POS2:
                break

            # Suffix as window tail — emit compound then stop extending
            if word_parts[end - 1]["pos1"]["ja"] == "接尾辞" and window > 1:
                tokens = word_parts[start:end]
                str_word = ''.join(t["orth"] for t in tokens)
                if len(str_word) >= 2:
                    candidates.append((str_word, [start, end]))
                break

            # Skip just particle
            if window == 1:
                # If beginning with で/て conjunction, stop
                if word_parts[start]["pos2"]["ja"] in {"格助詞", "係助詞", "終助詞", "準体助詞",  "接続助詞"}:
                    break

                # Don't start a window on a bare numeral
                if (word_parts[start]["pos2"]["ja"] == "数詞" and
                        all(('\uff10' <= c <= '\uff19') or ('0' <= c <= '9')
                        for c in word_parts[start]["orth"])):
                    break

                # standalone suffix
                if word_parts[start]["pos1"]["ja"] == "接尾辞":
                    break_after_add = True



                # POS tags that indicate a new independent grammatical unit - safe to break
                COMPOUND_BREAKERS = {
                    "助詞",  # Particles - always start new unit
                    "助動詞",  # Aux verbs - grammatical attachment
                    "補助記号",  # Aux symbols - punctuation etc
                    "接続詞",  # Conjunctions - new clause
                    "感動詞",  # Interjections
                    "記号",  # Symbols
                    "空白",  # Blank
                }

                # pos2 values that suggest independent word even within a continuing pos1
                COMPOUND_BREAKER_POS2 = {
                    "格助詞",  # Case particles
                    "係助詞",  # Topic particles
                    "副助詞",  # Adverbial particles
                    "接続助詞",  # Conjunctive particles
                    "終助詞",  # Sentence-final particles
                }

                if (word_parts[start]["pos1"]["ja"] in {"動詞", "形容詞"} and
                        word_parts[start]["cForm"].startswith(("未然形", "連用形", "意志推量形", "仮定形"))):
                    # Look ahead to see if break point
                    if end > n:
                        break
                    next_token  = word_parts[end]
                    next_pos1 = next_token["pos1"]["ja"]
                    next_pos2 = next_token["pos2"]["ja"]
                    if next_pos1 in COMPOUND_BREAKERS or next_pos2 in COMPOUND_BREAKER_POS2:
                        break
                    # Also break if next token is another verb/adjective (not a compound pattern)
                    if next_pos1 in {"動詞", "形容詞"} and next_pos2 == "一般":
                        break



                # Stop cases where possible aux verb stem found when prev is aux verb
                if (word_parts[start]["pos2"]["ja"] == "助動詞語幹" and
                    start > 0 and
                    word_parts[start - 1]["pos1"]["ja"] == "助動詞"):
                    break

            else:
                # Check for で/て be
                if word_parts[end-1]["pos2"]["ja"] == "非自立可能":
                    if end-2 >= 0 and  word_parts[end-2]["orth"] in {"で", "て"}:
                        break

                # Break if multi-token window ends in intermediate inflection
                if (word_parts[end - 1]["pos1"]["ja"] in {"動詞", "形容詞"} and
                        word_parts[end - 1]["cForm"].startswith(("未然形", "連用形"))):
                    break



                # if prefix is encountered, break
                if word_parts[end - 1]["pos1"]["ja"] == "接頭辞":
                    break

                # Mid-window prefix (pos2) - hard boundary
                if word_parts[end - 1]["pos2"]["ja"] == "接頭辞":
                    break

                # Break if numeral appears mid-window (prevents かつて10, なく40)
                if word_parts[end - 1]["pos2"]["ja"] == "数詞":
                    break


            # Don't emit if final token is a plain particle — the surface form
            # becomes misleading (e.g. records 語は instead of 語)
            last = word_parts[end - 1]
            if (last["pos1"]["ja"] == "助詞" and last["pos2"]["ja"] in {"格助詞", "係助詞", "副助詞", "準体助詞"}):
                continue

            tokens = word_parts[start:end]
            try:
                str_word = ''.join(t["orth"] for t in tokens)
            except:
                print(f"TOKS: {tokens}")
                print(f"word_parts: {word_parts}")
                raise Exception()

            # Skip one letter kana
            if len(str_word) < 2 and ((0x3040 <= ord(str_word) <= 0x309F) or (0x30A0 <= ord(str_word) <= 0x30FF)): # Is kana
                continue
            candidates.append((str_word, [start, end]))
            if break_after_add:
                break

    return word_parts, candidates


def process_word_batch(sentences):
    completed_sents = {}
    for sentence_key, sentence_dict in tqdm(sentences.items()):
        mecab_parts, candidates = get_word_candidates(sentence_key)
        sentence_dict["mecab"] = mecab_parts
        sentence_dict["p_candidates"] = candidates
        completed_sents[sentence_key] = sentence_dict
    return completed_sents



if __name__ == '__main__':

    all_the_text = json.load(open("../../jisho_sent_out.json", 'r'))

    # Split dict into chunks of 10k
    items = list(all_the_text.items())

    chunk_size = 10000
    chunks = [
        dict(items[i:i + chunk_size])
        for i in range(0, len(items), chunk_size)
    ]


    jobs = [(process_word_batch, chunk) for chunk in chunks]
    x = 0
    for job in tqdm(jobs):
        json.dump(job[0](job[1]), open(f"jish_sent_with_mecab_{x}.json", 'w', encoding='utf-8'), ensure_ascii=False,
                  indent=2)
        x += 1



    # with ProcessPoolExecutor() as executor:
    #     futures = [executor.submit(process_word_batch, chunk) for chunk in chunks]
    #     x= 0
    #     for future in tqdm(futures):
    #         json.dump(future.result(), open(f"jish_sent_with_mecab_{x}.json", 'w', encoding='utf-8'), ensure_ascii=False, indent=2)
    #         x += 1


    #print(f"Before: {len(items)} After: {len(results)}")
    #json.dump(results, open("test_out.json", 'w', encoding='utf-8'), ensure_ascii=False, indent=2)
