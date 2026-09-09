from collections import Counter
import json
import csv


kanji_chars = set()
kanji_chars.update([chr(s) for s in range(0x3400, 0x4DBF)])
kanji_chars.update([chr(s) for s in range(0x4E00, 0x9FFF)])
kanji_chars.update([chr(s) for s in range(0xF900, 0xFAFF)])

kanji_counter = Counter()

f_sents = open("word_processor_out_98f1ddf3-b41c-4b81-bd62-2e047eef6c3e.jsonl", 'r',  encoding='utf-8')
for sent_row in f_sents.readlines():
    sent_json = json.loads(sent_row)
    ja_sent = sent_json["ja"]
    for char in ja_sent:
        if char in kanji_chars:
            kanji_counter.update([char])

f_sents.close()
with open("kanji_popularity_stats.csv", 'w', encoding='utf-8', newline="") as csv_out:
    writer = csv.writer(csv_out, dialect="excel")
    writer.writerow(["kanji", "count"])

    for kanji, count in kanji_counter.most_common():
        writer.writerow([kanji, str(count)])
