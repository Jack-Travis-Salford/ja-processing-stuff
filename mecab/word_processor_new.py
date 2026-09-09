import json
import os
from collections import Counter
from pathlib import Path


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

def strip_tag(s):
    return s.split('-')[0] if s else ""


class Stats:
    def __init__(self):
        self.zero_hits = 0
        self.one_hit = 0
        self.one_hit_exact_match_and_en = 0
        self.two_plus_hit_exact_match_and_en = Counter()
        self.one_hit_exact_match = 0
        self.two_plus_hit_exact_match = Counter()
        self.one_hit_exact_en = 0
        self.two_plus_exact_en = Counter()
        self.one_alt_match = 0
        self.two_plus_alt_match = Counter()
        self.unresolved = Counter()

    def print(self):
        _json = {
            "zero_hits": self.zero_hits,
            "one_hit": self.one_hit,
            "one_hit_exact_match_and_en": self.one_hit_exact_match_and_en,
            "two_plus_hit_exact_match_and_en": self.two_plus_hit_exact_match_and_en,
            "one_hit_exact_match": self.one_hit_exact_match,
            "two_plus_hit_exact_match": self.two_plus_hit_exact_match,
            "one_hit_exact_en": self.one_hit_exact_en,
            "two_plus_exact_en": self.two_plus_exact_en,
            "one_alt_match": self.one_alt_match,
            "two_plus_alt_match": self.two_plus_alt_match,
            "unresolved": self.unresolved
        }

        json.dump(_json, open("word_matching_stats.json", 'w', encoding='utf-8'), ensure_ascii=False, indent=2)


def kana_resolve_return(mode, all_hits, match_ids, search_terms, word_mecab):
    if mode != 0:
        return get_return_body(all_hits, match_ids)

    # Kana resolve
    clean_kana_base = "".join(strip_tag(t["kanaBase"]) for t in word_mecab)
    resolve_search_terms = [*search_terms, clean_kana_base]
    resolve_all_hit_ids = set()

    for search_term in resolve_search_terms:
        if hit := jmdict_index["kana_ver"].get(search_term, False):
            for hit_version in hit:
                resolve_all_hit_ids.add(hit_version["id"])
    # Compare hit ids to kanji matches.
    tiebreaker_matches= match_ids.intersection(resolve_all_hit_ids)
    if len(tiebreaker_matches) == 1:
        return get_return_body(all_hits, tiebreaker_matches)

    else:
        return get_return_body(all_hits, match_ids)



def get_return_body(all_hits:list, match_ids:set):
    all_hits_by_id = {}
    for hit in all_hits:
        hit_id = hit["hit"]["id"]
        if hit_id in all_hits_by_id:
            continue
        all_hits_by_id[hit_id] = hit

    return_hits = []
    for id in match_ids:
        return_hits.append(all_hits_by_id[id])

    if len(return_hits) < 1:
        print("Something went wrong")

    return  return_hits if len(return_hits) > 1 else return_hits[0]


def process_word_candidate(jmdict_index:dict, sent_en:str, word_mecab:dict, stats:Stats):


    clean_orth_base = "".join(strip_tag(t["orthBase"]) for t in word_mecab)
    clean_orth = "".join(strip_tag(t["orth"]) for t in word_mecab)
    clean_lemma = "".join(strip_tag(t["lemma"]) for t in word_mecab)

    sent_en = sent_en.lower()

    search_terms = {kata_to_hira(clean_lemma), hira_to_kata(clean_lemma), kata_to_hira(clean_orth_base), hira_to_kata(clean_orth_base)}

    if len(word_mecab) > 1:
        search_terms.update({kata_to_hira(clean_orth), hira_to_kata(clean_orth)})

    zero_hits_counter = 0
    all_hit_ids = set()
    g_all_hits = []

    for x in range(2):
        all_hits = []

        for search_term in search_terms:
            if hit := jmdict_index["kanji_ver" if x==0 else "kana_ver"].get(search_term, False):
                for hit_version in hit:
                    all_hits.append({"search_term": search_term, "hit": hit_version})
                    g_all_hits.append({"search_term": search_term, "hit": hit_version})
                    all_hit_ids.add(hit_version["id"])
        # No hits
        if len(all_hits) == 0:
            stats.zero_hits += 1
            zero_hits_counter += 1
            continue

        # Only hit
        if len(all_hits) == 1:
            stats.one_hit += 1
            return get_return_body(all_hits, {all_hits[0]["hit"]["id"]})


        # Tie braking logic
        all_exact_term_common = set()
        all_alt_term_common = set()
        all_exact_eng = set()

        for hit in all_hits:
            "has exact_common, has secondary_common has_text_match"
            search_term = hit["search_term"]
            exact_term_common  = False
            alt_term_common = False
            exact_eng = False

            hit_id = hit["hit"]["id"]


            for kanji_word in hit["hit"]["kanji"]:
                if kanji_word["common"]:
                    if kanji_word["text"] == search_term:
                        exact_term_common = True
                    else:
                        alt_term_common = True

            for kanji_word in hit["hit"]["kana"]:
                if kanji_word["common"]:
                    if kanji_word["text"] == search_term:
                        exact_term_common = True
                    else:
                        alt_term_common = True

            for sense in hit["hit"]["sense"]:
                for gloss in sense["gloss"]:
                    gloss_text = gloss["text"].lower()
                    if gloss_text in sent_en:
                        exact_eng = True

            if exact_term_common:
                all_exact_term_common.add(hit_id)
            if alt_term_common:
                all_alt_term_common.add(hit_id)
            if exact_eng:
                all_exact_eng.add(hit_id)


        """
        Match success order: 
        EXACT + EXACT_EN
        EXACT
        EXACT_EN (+ ALT tiebreaker)
        ALT
        UNABLE_TO_REFINE
        """

        exact_match_and_en = all_exact_eng.intersection(all_exact_term_common)

        if len(exact_match_and_en) > 0:
            if len(exact_match_and_en) == 1:
                stats.one_hit_exact_match_and_en += 1
                return get_return_body(all_hits, exact_match_and_en)
            stats.two_plus_hit_exact_match_and_en.update([len(exact_match_and_en)])
            return kana_resolve_return(x, all_hits, exact_match_and_en, search_terms, word_mecab)

        if len(all_exact_term_common) > 0:
            if len(all_exact_term_common) == 1:
                stats.one_hit_exact_match += 1
                return get_return_body(all_hits, all_exact_term_common)
            stats.two_plus_hit_exact_match.update([len(all_exact_term_common)])
            return kana_resolve_return(x, all_hits, all_exact_term_common, search_terms, word_mecab)

        if len(all_exact_eng) > 0:
            if len(all_exact_eng) == 1:
                stats.one_hit_exact_en += 1
                return get_return_body(all_hits, all_exact_eng)
            stats.two_plus_exact_en.update([len(all_exact_eng)])
            return  kana_resolve_return(x, all_hits, all_exact_eng, search_terms, word_mecab)

        if len(all_alt_term_common) > 0:
            if len(all_alt_term_common) == 1:
                stats.one_alt_match += 1
                return get_return_body(all_hits, all_alt_term_common)
            stats.two_plus_alt_match.update([len(all_alt_term_common)])
            return kana_resolve_return(x, all_hits, all_alt_term_common, search_terms, word_mecab)




    if zero_hits_counter < 2:
        stats.unresolved.update([len(all_hit_ids)])
        return get_return_body(g_all_hits, all_hit_ids)

    stats.zero_hits += 1
    return False


def process_sentences(jmdict_index:dict, sent_entry: dict, stats:Stats):
    en = sent_entry["en"]
    candidates = sent_entry["p_candidates"]
    mecab_all = sent_entry["mecab"]

    confident_hits = []
    unresolved_hits = []

    for candidate in candidates:
        dict_form, [mecab_start, macab_end] = candidate
        mecab_parts = mecab_all[mecab_start:macab_end]
        search_res =  process_word_candidate(jmdict_index, en, mecab_parts, stats)
        if not search_res:
            continue
        if isinstance(search_res, dict):
            confident_hits.append({"candidate":[mecab_start,macab_end], "match": search_res})
        if isinstance(search_res, list):
            unresolved_hits.append({"candidate":[mecab_start,macab_end], "match": search_res})

    return confident_hits, unresolved_hits



if __name__ == '__main__':
    unresolved_count = 0
    from uuid import uuid4
    out_f_name = f"word_processor_out_{uuid4()}.jsonl"
    # f_unresolved = open("word_processor_unresolved.jsonl", 'w', encoding='utf-8')
    f_unresolved_dir = "unresolved_cases/"
    os.makedirs(f_unresolved_dir, exist_ok=True)
    stats = Stats()
    jmdict_index = json.load(open("jmdict_by_key.json", mode='r'))
    files = []
    for file in os.listdir("./jish_mecab"):
        if file.startswith("jish_sent_with_mecab_"):
            files.append(Path("jish_mecab", file))

    x = 0
    for file in files:
        print(f"Processing {file}")
        sentences: dict = json.load(open(file, encoding='utf-8', mode='r'))

        for sent_dict in sentences.values():
            confident_hits, unresolved_hits = process_sentences(jmdict_index, sent_dict, stats)

            mecab_keys_of_interest = {"count", "orth", "orthBase", "lemma", "kanaBase"}
            new_mecab = []
            for mecab in sent_dict["mecab"]:
                _mecab = {}
                for key in mecab_keys_of_interest:
                    _mecab[key] = mecab[key]
                new_mecab.append(_mecab)

            new_dict = {
                "en": sent_dict["en"],
                "ja": sent_dict["ja"],
                "file": sent_dict["file"],
                "mecab": new_mecab,
                "confident_hits": confident_hits,
                "unresolved_hits": unresolved_hits,
                "p_candidates": sent_dict["p_candidates"]
            }

            for unresolved in unresolved_hits:
                f = open(os.path.join(f_unresolved_dir, f"{unresolved_count}.json"), 'w')

                f.write(json.dumps(unresolved, ensure_ascii=False))
                unresolved_count += 1



            with open(out_f_name, "a", encoding="utf-8") as f:
                json.dump(new_dict, f, ensure_ascii=False)
                f.write("\n")

    print(f"UNRESOLVED COUNT:{unresolved_count}")
