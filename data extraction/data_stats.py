import os
import json

data_dir = "/Users/abhi/Documents/projects/translator/experiments/kriol-data"


def get_stats(path):
    filename = os.path.basename(path)
    with open(path, "r", encoding="utf-8") as fh:
        data = json.load(fh)
    n = len(data)
    print(f"Number of pairs for {filename}: {n:_}")


get_stats(os.path.join(data_dir, "kriol_eng_pairs_dict.json"))
get_stats(os.path.join(data_dir, "kriol_eng_pairs_bible.json"))
