import json
import csv

from conjugator import kanarizor


def _kanji_creator(kanji_dict):
    """
    Need deck 2: kana + def -> kanji
    """
    front_card = """
    <div><p class=english style="font-size: 30px; color:Red">{queue_no} -<i>Kanji</i></p></div>
    <div><p class=english style="font-size:40px; color:{mode_col}"><b>{mode}</b></p></div>
    <div><p class=japanese style="font-size:40px">{kanji}</p></div>
    """

    on_kun_primary= """
    <div>
    <p class=english style="font-size:30px"><b><u>Kana:</u></b></p>
    <p class=english style="font-size:40px"><b>ON:</b><ja_text>{on}</ja_text></p>
    <p class=english style="font-size:40px"><b>KUN:</b><ja_text>{kun}</ja_text></p>
    </div>
         
    """

    on_kun_secondary = """
    <div>
    <details><summary style="font-size:30px">Kana</summary>
    <p class=english style="font-size:40px"><b>ON:</b><ja_text>{on}</ja_text></p>
    <p class=english style="font-size:40px"><b>KUN:</b><ja_text>{kun}</ja_text></p>
    </details>
    </div>
    """

    def_primary= """
    <div>
    <p class=english style="font-size:30px"><b><u>Meaning:</u></b></p>
    <p class=english style="font-size:40px">{kanji_def}</p>
    </div>
    """

    def_secondary = """
    <div>
    <details><summary style="font-size:30px">Meaning</summary>
    <p class=english style="font-size:40px">{kanji_def}</p>
    </details>
    </div>
    """

    back_card = """
    {primary}
    {secondary}
    """

    card_deck_1 = []

    entry = []
    # meaning?
    entry.append(str(kanji_dict["queue_no"]) + "_1")
    entry.append(front_card.format(mode_col="Fuchsia", mode="Meaning?", kanji=kanji_dict["kanji"], queue_no=kanji_dict["queue_no"]))
    entry.append(back_card.format(primary=def_primary.format(kanji_def=kanji_dict["def"]),
                                    secondary=on_kun_secondary.format(on=kanji_dict["on"], kun=kanji_dict["kun"])))
    card_deck_1.append(entry)

    # on/kun?
    entry = []
    entry.append(str(kanji_dict["queue_no"]) + "_2")
    entry.append(front_card.format(mode_col="DodgerBlue", mode="On/Kun?", kanji=kanji_dict["kanji"], queue_no=kanji_dict["queue_no"]))
    entry.append(back_card.format(primary=on_kun_primary.format(on=kanji_dict["on"], kun=kanji_dict["kun"]),
                                    secondary=def_secondary.format(kanji_def=kanji_dict["def"])))#
    card_deck_1.append(entry)

    return card_deck_1, []



def _vocab_creator_kanji(vocab_dict):

    card_deck_1 = []
    card_deck_2 = []
    x = 1

    meaning_text = "Meaning? (x{})".format(len(vocab_dict["defs"])) if len(vocab_dict["defs"]) > 1 else "Meaning?"
    card_1_front = (f'<div><p class=english style="font-size: 30px; color:Aquamarine">{vocab_dict["queue_no"]} -<i>Vocab</i></p></div>'
       f'<div><p class=english style="font-size:40px; color:Fuchsia"><b>{meaning_text}</b></p></div>'
        f'<div><p class=japanese style="font-size:40px">{vocab_dict["kanji"]}</p></div>')

    card_1_back = '<div><p class=english style="font-size:30px"><b><u>Defs:</u></b></p></div>'
    for vocab_def in vocab_dict["defs"]:
        card_1_back += (f'<div><p class=english style="font-size:40px">{vocab_def["def"]}</p><div>'
        f'<details><summary style="font-size:30px">Kana</summary>'
        f'<p class=english style="font-size:30px"><b>KANJI:</b><ja_text>{vocab_def["kanji"]}</ja_text></p>'
        f'<p class=english style="font-size:30px"><b>KANA:</b><ja_text>{vocab_def["kana"]}</ja_text></p>'
        f'</details></div></div>')
        card_1_back += "<hr/>"
    card_1_back.removesuffix("<hr/>")
    card_deck_1.append([str(vocab_dict["queue_no"]) + f"_{x}", card_1_front, card_1_back])
    x += 1
    for vocab_def in vocab_dict["defs"]:
        card_2_front = (f'<div><p class=english style="font-size: 30px; color:Aquamarine">{vocab_dict["queue_no"]} -<i>Vocab</i></p></div>'
                        f'<div><p class=english style="font-size:30px; color:DodgerBlue"><b>Kana?</b></p></div>'
                        f'<div><p class=japanese style="font-size:40px">{vocab_dict["kanji"]}</p></div>'
                        f'<div><p class=english style="font-size:40px">{vocab_def["def"]}</p></div>')

        card_2_back = ('<div><p class=english style="font-size:30px"><b><u>Kanji/Kana:</u></b></p>'
                      f'<p class=english style="font-size:35px"><b>KANJI:</b><ja_text>{vocab_def["kanji"]}</ja_text></p></div>'
                      f'<p class=english style="font-size:35px"><b>KANA:</b><ja_text>{vocab_def["kana"]}</ja_text></p></div>')
        card_deck_1.append([str(vocab_dict["queue_no"]) + f"_{x}",card_2_front, card_2_back])
        x += 1
    dk_2_def_sect = ''
    for vocab_def in vocab_dict["defs"]:
        dk_2_def_sect += f'<div><p class=english style="font-size:40px">{vocab_def["def"]}</p></div>'
        dk_2_def_sect += f'<p class=english style="font-size:40px"><b>KANA:</b><ja_text>{vocab_def["kana"]}</ja_text></p></div>'
        dk_2_def_sect += "<hr/>"
    dk_2_def_sect.removesuffix("<hr/>")


    card_3_front = (f'<div><p class=english style="font-size: 30px; color:Aquamarine">{vocab_dict["queue_no"]} -<i>Vocab</i></p></div>'
                    f'{dk_2_def_sect}'



                    )
    card_3_back = f'<div><p class=japanese style="font-size:40px">{vocab_dict["kanji"]}</p></div>'

    card_deck_2.append([str(vocab_dict["queue_no"]) + f"_{x}",card_3_front, card_3_back])
    x += 1
    return card_deck_1, card_deck_2

def _sent_creator_kana(sent_dict):
    card_deck_1 = []
    card_deck_2 = []
    card_1_front = (f'<div><p class=english style="font-size: 30px; color:Thistle">{sent_dict["queue_no"]} - <i>Sent <b>(Kana only)</b></i></p></div>'
                    '<div><p class=english style="font-size:40px; color:Fuchsia"><b>Meaning?</b></p></div>'
                    f'<div><p class=japanese style="font-size:40px">{sent_dict["sent"]}</p></div>')

    card_1_back = ('<div>'
                    '<p class=english style="font-size:30px"><b><u>Meaning:</u></b></p>'
                    f'<p class=english style="font-size:40px">{sent_dict["sent_def"]}</ja_text></p>'
                    '<details><summary style="font-size:30px">Kana</summary>'
                    f'<p class=english style="font-size:40px"><ja_text>{sent_dict["sent_kana"]}</ja_text></p>'
                    '</details>'
                    '</div>')
    card_deck_1.append([str(sent_dict["queue_no"]) + "_1",card_1_front, card_1_back])


    card_2_front = (f'<div><p class=english style="font-size: 30px; color:Thistle">{sent_dict["queue_no"]} - <i>Sent <b>(Kana only)</b></i></p></div>'
                    f'<div><p class=english style="font-size:40px">{sent_dict["sent_def"]}</p></div>')

    card_2_back = (f'<p class=english style="font-size:40px"><ja_text>{sent_dict["sent"]}</ja_text></p>'
                   '<details><summary style="font-size:30px">Hiragana</summary>'
                    f'<p class=english style="font-size:40px"><ja_text>{sent_dict["sent_kana"]}</ja_text></p>'
                    '</details>')

    card_deck_2.append([str(sent_dict["queue_no"]) + "_2",card_2_front, card_2_back])
    return card_deck_1, card_deck_2

def _sent_creator_kanji(sent_dict):

    card_deck_1 = []
    card_deck_2 = []
    kanarized_kana = kanarizor(sent_dict["sent"])
    card_1_front = (
        f'<div><p class=english style="font-size: 30px; color:Coral">{sent_dict["queue_no"]} - <i>Sent</i></p></div>'
        '<div><p class=english style="font-size:40px; color:Fuchsia"><b>Meaning?</b></p></div>'
        f'<div><p class=japanese style="font-size:40px">{sent_dict["sent"]}</p></div>')

    card_1_back = ('<div>'
                   '<p class=english style="font-size:30px"><b><u>Meaning:</u></b></p>'
                   f'<p class=english style="font-size:40px">{sent_dict["sent_def"]}</p>'
                   '<details><summary style="font-size:30px">Kana</summary>'
                   f'<p class=english style="font-size:40px">Jisho:<ja_text>{sent_dict["sent_kana"]}</ja_text></p>'
                   f'<p class=english style="font-size:40px">Kanarizor:<ja_text>{kanarized_kana}</ja_text></p>'
                   '</details>'
                   '</div>')

    card_deck_1.append([str(sent_dict["queue_no"]) + "_1",card_1_front, card_1_back])

    card_2_front = (
        f'<div><p class=english style="font-size: 30px; color:Coral">{sent_dict["queue_no"]} - <i>Sent</i></p></div>'
        '<div><p class=english style="font-size:40px; color:DodgerBlue"><b>Kana?</b></p></div>'
        f'<div><p class=japanese style="font-size:40px">{sent_dict["sent"]}</p></div>')

    card_2_back = ('<div>'
                   '<p class=english style="font-size:30px"><b><u>Kana:</u></b></p>'
                   f'<p class=english style="font-size:40px">Jisho:<ja_text>{sent_dict["sent_kana"]}</ja_text></p>'
                   f'<p class=english style="font-size:40px">Kanarizor:<ja_text>{kanarized_kana}</ja_text></p>'
                   '<details><summary style="font-size:30px">Meaning</summary>'
                   f'<p class=english style="font-size:40px">{sent_dict["sent_def"]}</p>'
                   '</details>'
                   '</div>')
    card_deck_1.append([str(sent_dict["queue_no"]) + "_2",card_2_front, card_2_back])

    card_3_front = (f'<div><p class=english style="font-size: 30px; color:Coral">{sent_dict["queue_no"]} - <i>Sent</i></p></div>'
                    f'<div><p class=english style="font-size:40px">{sent_dict["sent_def"]}</p></div>'
                    '<details><summary style="font-size:30px">Kana</summary>'
                    f'<p class=english style="font-size:40px">Jisho:<ja_text>{sent_dict["sent_kana"]}</ja_text></p>'
                    f'<p class=english style="font-size:40px">Kanarizor:<ja_text>{kanarized_kana}</ja_text></p>'
                    '</details>'
                    )

    card_3_back = (f'<p class=english style="font-size:40px"><ja_text>{sent_dict["sent"]}</ja_text></p>'
                   '<details><summary style="font-size:30px">Hiragana</summary>'
                   f'<p class=english style="font-size:40px"><ja_text>{sent_dict["sent_kana"]}</ja_text></p>'
                   '</details>')

    card_deck_2.append([str(sent_dict["queue_no"]) + "_3",card_3_front, card_3_back])

    return card_deck_1, card_deck_2


def _sent_creator(sent_dict):
    if set(sent_dict["sent"]).issubset(allowed_chars):
        return _sent_creator_kana(sent_dict)
    return _sent_creator_kanji(sent_dict)



"""
sents

KANJI
ja_sent -> sent_def
ja_sent -> sent_kana

Deck 2
sent_def + (hidden) sent_kana? -> ja_sent

"""
all_added = json.load(open("./files/all_added.json", mode="r"))
kanji_obj = all_added["kanji"]['\u4e0a']

anki_queue = [None]*all_added["queue_no"]
print(len(anki_queue))


allowed_chars = set()
allowed_chars.update([chr(i) for i in range(0x0030, 0x003A)])
allowed_chars.update([chr(i) for i in range(0x0041, 0x005B)])
allowed_chars.update([chr(i) for i in range(0x0061, 0x007B)])
allowed_chars.update([chr(i) for i in range(0x3041, 0x30F3)])
allowed_chars.update([chr(i) for i in range(0x30A0, 0x30F7)])
allowed_chars.update([chr(i) for i in range(0xFF11, 0xFF3b)])
allowed_chars.update([chr(i) for i in range(0xFF41, 0xFF5b)])
allowed_chars.update("。", " ", "\t", "\n", "、", "？", "ー", "！", "・", ".", "〜", "…", "『", "』", "=",
                         "｡", "°", "₁", "<", ":", "~", "@", "?", "\"", "♡", ",", "!", "～", "(", ")", "×", "）",
                         "（", "：", "-", "%", "🧾", "％", "—", '\ufeff', '\u3000', "「", "」", ".","．", ";", "，",
                         "－", "＋", "/", "／", "+", "*", "♪", ">", "〇", "＃", "＆", "＄", "【", "】", "’" , "“",
                         "”", "②", "―", "℃", "〆", "^", "※", "○" ,"‘" ,"[" ,"]", "₂", "β", "→", "①", "Ⅰ",
                         "_", "｢", "｣", "㎏", "㌘", "|")



for key in all_added["kanji"].keys():
    kanji_obj = all_added["kanji"][key]
    kanji_obj["type"] = "kanji"
    anki_queue[kanji_obj["queue_no"]] = kanji_obj


for key in all_added["vocab"].keys():
    vocab_obj = all_added["vocab"][key]
    vocab_obj["type"] = "vocab"
    anki_queue[vocab_obj["queue_no"]] = vocab_obj


for key in all_added["sentence"].keys():
    sent_obj = all_added["sentence"][key]
    sent_obj["type"] = "sent"
    anki_queue[sent_obj["queue_no"]] = sent_obj

pathing = {
    "kanji":_kanji_creator,
    "vocab":_vocab_creator_kanji,
    "sent":_sent_creator
}
deck_1 = []
deck_2 = []
for item in anki_queue:
    if not isinstance(item, dict):
        continue
    dk_1, dk_2 = pathing[item["type"]](item)
    deck_1.extend(dk_1)
    deck_2.extend(dk_2)
    # print(f"Created cards: {len(dk_1)} - {len(dk_2)}")
    # print(item)

for item in deck_1:
    print(item)
print("/|?|?|?|?|?")
for item in deck_2:
    print(item)
# cards_deck_1, cards_deck_2 = _kanji_creator(kanji_obj)


# all_cards.extend(cards_deck_1)

with open("./files/out_for_anki_1.csv", mode='w', encoding='utf-8') as csvfile:
    f_writer = csv.writer(csvfile, dialect='excel')
    f_writer.writerows(deck_1)

with open("./files/out_for_anki_2.csv", mode='w', encoding='utf-8') as csvfile:
    f_writer = csv.writer(csvfile, dialect='excel')
    f_writer.writerows(deck_2)
