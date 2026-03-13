import json
import os.path
import shutil

from conjugator import kanarizor, conjugate_and_kanarize

allowed_chars = set()  # All processed chars
backlog_kanji = {} # All chars encountered that are yet to be added. {char: Total encounters}

backlog = { # The full backlog
    "vocab":{},
    "sentence":{},
}

all_added = {
    "kanji":{},
    "vocab":{},
    "sentence":{},
    "queue_no":0
}

def allowed_chars_init():
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
                         "_", "｢", "｣", "㎏", "㌘")



def save_all():
    with open("./files/allowed_chars.json", mode='w') as file_writer:
        file_writer.write(json.dumps({"chars":[*allowed_chars]}, indent=2))
    with open("./files/backlog_kanji.json", mode='w') as file_writer:
        file_writer.write(json.dumps(backlog_kanji, indent=2))
    with open("./files/backlog.json", mode='w') as file_writer:
        file_writer.write(json.dumps(backlog, indent=2))
    with open("./files/all_added.json", mode='w') as file_writer:
        file_writer.write(json.dumps(all_added, indent=2))

def load_all():
    global backlog_kanji
    backlog_kanji = json.load(open("./files/backlog_kanji.json"))
    global backlog
    backlog = json.load(open("./files/backlog.json"))
    global all_added
    all_added = json.load(open("./files/all_added.json"))
    global allowed_chars
    allowed_chars = {*json.load(open("./files/allowed_chars.json"))["chars"]}

def backup():
    if not os.path.exists("./backup"):
        os.makedirs("./backup", exist_ok=True)
    f_count = len(os.listdir("./backup"))
    name_not_found = True
    while name_not_found:
        if os.path.exists(f"./backup/{f_count}"):
            f_count += 1
        else:
            name_not_found = False
    base_dir = f"./backup/{f_count}"
    os.makedirs(base_dir, exist_ok=True)
    try:
        shutil.copy("./files/allowed_chars.json", os.path.join(base_dir,"allowed_chars.json"))
        shutil.copy("./files/backlog_kanji.json", os.path.join(base_dir, "backlog_kanji.json"))
        shutil.copy("./files/backlog.json", os.path.join(base_dir, "backlog.json"))
        shutil.copy("./files/all_added.json", os.path.join(base_dir, "all_added.json"))

    except:
        print("Backup failed when attempting to copy files. Maybe they dont already exist?")


def check_sent_backlog(add_to_active_queue=False, iter_chars=None):
    if iter_chars == None:
        iter_chars = allowed_chars
    elif isinstance(iter_chars, str):
        iter_chars = [iter_chars]
    for kanji in iter_chars:
        to_pop = []
        for key in backlog["sentence"]:
            sentence: dict = backlog["sentence"][key]
            awaiting = sentence["awaiting"]
            if kanji in awaiting:
                awaiting.remove(kanji)
                sentence["awaiting"] = awaiting
            if len(awaiting) == 0 and add_to_active_queue is True:
                sentence.pop("awaiting")
                all_added["sentence"][key] = {
                    **sentence,
                    "queue_no": all_added["queue_no"]
                }
                all_added["queue_no"] += 1
                to_pop.append(key)
                print(f"SENT: {key} added to list")
        for pop in to_pop:
            backlog["sentence"].pop(pop)


def check_vocab_backlog_for_char(kanji):
    if kanji in backlog_kanji:
        backlog_kanji.pop(kanji)
        to_pop = []
        for key in backlog["vocab"]:
            vocab:dict = backlog["vocab"][key]
            awaiting = vocab["awaiting"]
            if kanji in awaiting:
                awaiting.remove(kanji)
                vocab["awaiting"] = awaiting
            if len(awaiting) == 0:
                vocab.pop("awaiting")
                all_added["vocab"][key] = {
                    **vocab,
                    "queue_no": all_added["queue_no"]
                }
                all_added["queue_no"] += 1
                to_pop.append(key)
                print(f"VOCAB: {key} added to list")
        for pop in to_pop:
            backlog["vocab"].pop(pop)




def add_kanji(kanji, kanji_dict:dict):

    all_added["kanji"][kanji] = {
        **kanji_dict,
        "queue_no":all_added["queue_no"]
    }
    all_added["queue_no"] += 1
    allowed_chars.add(kanji)
    print(f"KANJI: {kanji} now added.")
    check_vocab_backlog_for_char(kanji)




def get_missing_chars(obj):
    if isinstance(obj, str):
        missing_chars = []
        for letter in obj:
            if letter not in allowed_chars:
                if letter in backlog_kanji:
                    backlog_kanji[letter] += 1
                else:
                    backlog_kanji[letter] = 1
                if letter not in missing_chars:
                    missing_chars.append(letter)
    else:
        missing_chars = []
        for row in obj["defs"]:
            word = row["kanji"]
            for letter in word:
                if letter not in allowed_chars:
                    if letter in backlog_kanji:
                        backlog_kanji[letter] += 1
                    else:
                        backlog_kanji[letter] = 1
                    if letter not in missing_chars:
                        missing_chars.append(letter)
    return missing_chars



def add_vocab(vocab, vocab_dict:dict):
    needed_chars = get_missing_chars(vocab_dict)
    if len(needed_chars) == 0:
        all_added["vocab"][vocab] = {
            **vocab_dict,
            "queue_no": all_added["queue_no"]
        }
        all_added["queue_no"] += 1
        print(f"VOCAB: {vocab} added to list")

    else:
        backlog["vocab"][vocab] = {
            **vocab_dict,
            "awaiting":needed_chars
        }
        print(f"{vocab} added to backlog. Awaiting kanji:{needed_chars}")


def add_sent(sent, sent_def, sent_kana):
    needed_chars = get_missing_chars(sent)
    # if len(needed_chars) == 0:
    #     all_added["sentence"][sent] = {
    #         "sent": sent,
    #         "sent_def": sent_def,
    #         "sent_kana": sent_kana,
    #         "queue_no": all_added["queue_no"]
    #     }
    #     all_added["queue_no"] += 1
    #     print(f"{sent} added to list")
    #
    # else:
    backlog["sentence"][sent] = {
        "sent": sent,
        "sent_def": sent_def,
        "sent_kana": sent_kana,
        "awaiting": needed_chars
    }
    print(f"{sent} added to backlog. Awaiting kanji:{needed_chars}")


def confirmation(msg="All good? (T/F):"):
    while True:
        details_correct = get_input(msg).lower()
        if details_correct == "t":
            return True
        elif details_correct == "f":
            return False



def print_kanji_backlog():
    sorted_keys = sorted(backlog_kanji , key=backlog_kanji.get)
    for key in sorted_keys:
        print(f"{key}:{backlog_kanji[key]} -> {hex(ord(key))}")




def get_input(question):
    reply = input(question)
    reply =  reply.replace("\\n", "\n")
    reply = reply.strip()
    return reply


def kanji_input_handler():
    kanji = get_input("Kanji:")
    if kanji in all_added["kanji"]:
        print("Kanji already processed")
        return
    vals = {
        "kanji": kanji,
        "on": get_input("On:"),
        "kun": get_input("Kun:"),
        "def": get_input("Def:"),
    }
    print(json.dumps(vals, indent=2, ensure_ascii=False))
    if confirmation() is False:
        return
    add_kanji(kanji, vals)

def vocab_input_handler():
    vocab = get_input("Vocab (dict form):")
    if vocab in all_added["vocab"]:
        print("Vocab already processed")
        return
    elif vocab in backlog["vocab"]:
        print("Vocab already in backlog")
        return
    defs = []
    is_more_defs = True
    is_verb = vocab[-1] in {"る","す", "い", "く", "う"} and confirmation("Confirm is verb? (Y/N):")
    # else:
    #     is_verb = confirmation("Is verb (T/F)?:")
    while is_more_defs:
        new_def = {
            "def": get_input("Def:"),
            # "kanji":get_input("Vocab (Kanji - All forms):"),
            # "kana":get_input("Kana:")
        }

        if not is_verb:
            new_def["kanji"] = vocab
            kana = kanarizor(vocab)
            if confirmation(f"Kana is {kana}(T/F)?:"):
                new_def["kana"] = kana
            else:
                new_def["kana"] = get_input("Kana form:")
        else:
            if confirmation(f"{vocab} -> {kanarizor(vocab)} (T/F)?") is True:
                conjugated = conjugate_and_kanarize(vocab)
                if conjugated[0] is not False:
                    new_def["kanji"] = conjugated[0]
                    new_def["kana"] = conjugated[1]
                else:
                    print("Conjugator failed")
                    new_def["kanji"] = get_input("Kanji (dict, Present, te):")
                    new_def["kana"] = get_input("Kana (dict, Present, te):")
            else:
                new_def["kanji"] = get_input("Kanji (dict, Present, te):")
                new_def["kana"] = get_input("Kana (dict, Present, te):")
        defs.append(new_def)
        is_more_defs = confirmation("More defs? (T/F)")
    vocab_dict = {
        "defs": defs,
        "kanji": vocab
    }

    print(json.dumps(vocab_dict, indent=2, ensure_ascii=False))
    if confirmation() is False:
        return
    add_vocab(vocab, vocab_dict)

def sent_input_handler():
    sent = get_input("Sent (kanji):")
    if sent in all_added["sentence"]:
        print("Sent already processed")
        return
    elif sent in backlog["sentence"]:
        print("Sent already in backlog")
        return
    sent_kana = kanarizor(sent)
    sent_def = get_input("Def:")
    print(f"Sent:{sent}\nDef:{sent_def}\nKana:{sent_kana}")
    if confirmation() is False:
        return
    add_sent(sent, sent_def, sent_kana)


backup()
load_all()

if __name__ == '__main__':
    # allowed_chars_init()
    #
    # all_sent = json.load(open("./files/all_jisho_and_wk.json"))
    # for key in all_sent:
    #     sent = all_sent[key]
    #     add_sent(sent["ja_sent"],sent["en_sent"], sent["ja_kana"])
    # save_all()
    # print("Done")
    # exit()

    should_continue = True

    while should_continue:
        print("1: Kanji, 2:Vocab, 3:Sent, 4:Add allowed char, 5:See allowed chars, 6: See backlog 7: Process sent backlog")
        try:
            inpt_type = int(get_input("what are you adding:"))
        except:
            continue
        if inpt_type == 1:
           kanji_input_handler()
        elif inpt_type == 2:
            vocab_input_handler()
        elif inpt_type == 3:
            sent_input_handler()
        elif inpt_type == 4:
            allow_char = get_input("Char to add to allow list:")
            print(f"Selected char {allow_char}")
            if confirmation() is False:
                continue
            allowed_chars.add(allow_char)
            check_vocab_backlog_for_char(allow_char)
            check_sent_backlog()
        elif inpt_type == 5:
            print("Allowed chars:")
            chars = sorted(allowed_chars)
            for x in range(0, len(chars), 20):
                print(chars[x:x+20])
        elif inpt_type == 6:
            print_kanji_backlog()
        elif inpt_type == 7:
            char = get_input("Which char (blank if check all):")
            if char == "":
                check_sent_backlog(True)
            else:
                if char not in allowed_chars:
                    print("Error: Char not found in allowed chars. Checking cancelled")
                else:
                    check_sent_backlog(True, char)
        save_all()
        print(("="*80 + "\n")*2)
    
