import os
import json
import main


def jisho_sentence_adder():
    all_data = json.load(open("./files/all_jisho.json"))

    x = 0
    for key in all_data:
        sent = all_data[key]
        x+= 1
        if x%100==0:
            print(f"{x}\n"*5)
        main.add_sent(sent["ja_sent"], sent["en_sent"], sent["ja_kana"])

    main.save_all()
    print(x)

jisho_sentence_adder()