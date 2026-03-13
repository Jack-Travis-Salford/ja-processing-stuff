import json
import os
import threading
import traceback
from concurrent.futures import as_completed
import multiprocessing
from concurrent.futures.thread import ThreadPoolExecutor
import pandas as pd
import bs4.element
from tqdm import tqdm
from bs4 import BeautifulSoup

dir = "../jisho_pages"

processed_sents = {}
if os.path.exists("../jisho_sent_out.json"):
    processed_sents = json.load(open("../jisho_sent_out.json", 'r'))
processed_sents_lock = threading.Lock()

def process_jisho_file(dir, file):
    try:
        #print(f"file:///{os.path.abspath(os.path.join(dir, file))}")

        f_content = BeautifulSoup(open(os.path.join(dir, file), encoding='utf-8'), "lxml")
        sentence_list = f_content.find("ul", class_="sentences")
        if sentence_list is None:
            print(f"NO CONTENT: file:///{os.path.abspath(os.path.join(dir, file))}")
            return
        # Iter through all sentences
        sentence_list_elements =  sentence_list.find_all("li",  recursive=False)
        for sentence_obj in sentence_list_elements:
            # Get en sentence. No further modification needed.
            en_sentence = sentence_obj.find("div", class_="english_sentence").find("span", class_="english").text

            # Get ja sentence associated ul
            ja_ul = sentence_obj.find("ul", class_="japanese_sentence")
            ja_str = ""
            ja_mark_up = []
            for element in ja_ul: #For each part that makes up the sentence
                # If not inside of an li element, just get the text.
                if isinstance(element, bs4.element.NavigableString):
                    ja_str += element.text
                    if ja_str.strip() == "":
                        continue
                    ja_mark_up.append({"sent_part":element.text})
                else:
                    # Attempt furigana extraction if possible + kanji
                    furigana = element.find("span", class_="furigana")
                    ja_el_txt = element.find("span", class_="unlinked")
                    # See if kanji is a hyperlink instead if currently None
                    if ja_el_txt is None:
                        ja_el_txt = element.find("a")

                    if ja_el_txt is None: # Error check
                        print(f"file:///{os.path.abspath(os.path.join(dir, file))}")
                        print(element)
                        print(ja_ul)
                        break

                    ja_el_txt = ja_el_txt.text
                    if ja_el_txt.strip() == "":
                        continue
                    ja_str += ja_el_txt
                    ja_mark_up.append({"sent_part": ja_el_txt, "furigana": furigana.text if furigana is not None else None})
            #with processed_sents_lock:

            ja_str = ja_str.strip()
            if ja_str in processed_sents:
                continue
            ja_mark_up[0]["sent_part"] = ja_mark_up[0]["sent_part"].lstrip()
            ja_mark_up[-1]["sent_part"] = ja_mark_up[-1]["sent_part"].rstrip()
            processed_sents[ja_str] = {"en":en_sentence.strip(), "ja":ja_str, "ja_mark_down":ja_mark_up, "file":f"file:///{os.path.abspath(os.path.join(dir, file))}"}
    except:
        print(traceback.format_exc())
        print(f"file:///{os.path.abspath(os.path.join(dir, file))}")


def wk_sent_extractor():
    all_data = json.load(open("../wani_dump/wk_data_grouped.json", 'r'))["wk_data"]

    for vocab in all_data["vocabulary"]:
        vocab_word = vocab["data"]["characters"]
        for example_sentence in vocab["data"].get("context_sentences", []):
            ja_sent = example_sentence["ja"]
            en_sent = example_sentence["en"]
            if ja_sent in processed_sents:
                continue
            processed_sents[ja_sent] = {"en":en_sent, "ja":ja_sent, "file":f"wk_vocab_{vocab_word}"}

    for vocab in all_data["kana_vocabulary"]:
        vocab_word = vocab["data"]["characters"]
        for example_sentence in vocab["data"].get("context_sentences", []):
            ja_sent = example_sentence["ja"]
            en_sent = example_sentence["en"]
            if ja_sent in processed_sents:
                continue
            processed_sents[ja_sent] = {"en":en_sent, "ja":ja_sent, "file":f"wk_vocab_{vocab_word}"}


def tatoeba_processor():
    all_data = pd.read_csv("../tatoeba.tsv", sep='\t', names=["en_id", "en", "ja_id", "ja"])
    for index, data_row in all_data.iterrows():
        en = data_row["en"]
        ja = data_row["ja"]
        if en is None or ja is None:
            print(f"Missing data: {data_row}")
            continue
        if ja in processed_sents:
            continue
        processed_sents[ja] = {"en": en, "ja": ja, "file": f"tatoeba_{index}"}


if __name__ == '__main__':
    cur_tot_sents = len(processed_sents)
    # for file in tqdm(os.listdir(dir)):
    #     # single
    #     process_jisho_file(dir, file)

    tatoeba_processor()
    tot_new_sents  =len(processed_sents) - cur_tot_sents
    print(f"{tot_new_sents} new sents, {len(processed_sents)} total. ")

    json.dump(processed_sents, open("../jisho_sent_out.json", 'w'))
    json.dump(processed_sents, open("../jisho_sent_out_readable.json", 'w', encoding='utf-8'), indent=3, ensure_ascii=False)







# try:
#     f_content = BeautifulSoup(open(os.path.join(dir, file), encoding='utf-8'), "lxml")
#     if f_content is None:
#         print(f"file:///{os.path.abspath(os.path.join(dir, file))}")
#     sentence_list = f_content.find("ul", class_="sentences")
#     total_sents =  len(sentence_list.find_all("li",  recursive=False))
#     if total_sents < 1:
#         print(f"No sentences found for {os.path.join(dir, file)}")
# except:
#     print(traceback.format_exc())
#     print(f"file:///{os.path.abspath(os.path.join(dir, file))}")
