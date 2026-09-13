import csv
import json


with open("kanji_popularity_stats.csv", 'r') as csv_file:
    reader = csv.reader(csv_file)
    reader.__next__()

    kanji_list  = list(reader)
    print(kanji_list)



wk = json.load(open("../../wani_dump/wk_data_grouped.json", 'r'))["wk_data"]["kanji"]

wk_kanji = set()

for kanji in wk:
    wk_kanji.update(kanji["data"]["slug"])


with open("kanji_popularity_stats.csv", 'w', encoding='utf-8', newline="") as csv_out:
    writer = csv.writer(csv_out, dialect="excel")
    writer.writerow(["kanji", "count"])

    for kanji, count in kanji_list:
        if kanji in wk_kanji:
            writer.writerow([kanji, str(count)])
