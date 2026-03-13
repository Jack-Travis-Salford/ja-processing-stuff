import json
from conjugator import kanarizor



all_sent = json.load(open("./files/all_jisho.json"))

print(len(all_sent))


def wk_sentence_adder():
    all_data = json.load(open("./files/wk_out.json"))

    types = {}
    x = 0
    for data_row in all_data["all"]:
        data_type = data_row["object"]
        if data_type == "vocabulary":
            #print(json.dumps(data_row, indent=3))
            sentences = data_row["data"]["context_sentences"]
            for sentence in sentences:
                en_sent = sentence["en"]
                ja_sent = sentence["ja"]
                kana_sent = kanarizor(ja_sent)

                if ja_sent not in all_sent:
                    all_sent[ja_sent] = {
                        "ja_sent":ja_sent,
                        "en_sent":en_sent,
                        "ja_kana":kana_sent
                    }
    with open("./files/all_jisho_and_wk.json", mode='w') as writer:
        writer.write(json.dumps(all_sent, indent=2))


                #
                # if kana_sent is False:
                #     print("Error for:")
                #     print(en_sent)
                #     print(ja_sent)
                #     print()

                # if ja_sent in main.all_added["sentence"]:
                #     print("Sent already processed")
                #     continue
                # elif ja_sent in main.backlog["sentence"]:
                #     print("Sent already in backlog")
                #     continue
                # x += 1
                # if x % 10 == 0:
                #     print(x)

                #main.add_sent(ja_sent, en_sent, kana_sent)

    # main.save_all()
    # print(x)
wk_sentence_adder()