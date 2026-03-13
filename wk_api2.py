import json
import os

import requests

import dotenv

dotenv.load_dotenv()


def api_data_collection():
    all_data = []
    url = "https://api.wanikani.com/v2/subjects"
    header = {
        "Authorization": f"Bearer {os.environ.get("wk_key", "")}"
    }
    while url:
        print(url)
        data = requests.get(url, headers=header).json()
        all_data.extend(data.get("data", []))
        url = data.get("pages", {}).get("next_url", None)
    json.dump({"wk_data": all_data}, open("../wani_dump/wk_data.json", 'w'))
    json.dump({"wk_data": all_data}, open("../wani_dump/wk_data_readable.json", 'w', encoding="utf-8"), ensure_ascii=False, indent=3)


def collection_grouping():
    all_data = json.load(open("../wani_dump/wk_data.json", 'r'))
    new_data = {}
    for data_row in all_data["wk_data"]:
        obj = data_row.get("object", "n/a")
        new_data.setdefault(obj, []).append(data_row)
    json.dump({"wk_data": new_data}, open("../wani_dump/wk_data_grouped.json", 'w'))
    json.dump({"wk_data": new_data}, open("../wani_dump/wk_data_grouped_readable.json", 'w', encoding="utf-8"),
              ensure_ascii=False, indent=3)


collection_grouping()