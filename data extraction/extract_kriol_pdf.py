import os
import re
import json
from tqdm import tqdm
from PyPDF2 import PdfReader

from common import BASE_DIR, DATA_DIR

raw_data_path = os.path.join(DATA_DIR, "raw")
filename = "BelizeKriol_EngDic_49337_2009.pdf"

output_path = os.path.join(DATA_DIR, "eng-kriol-pairs")

filepath = os.path.join(raw_data_path, filename)
reader = PdfReader(filepath)

with open(os.path.join(DATA_DIR, "pos.json"), "r", encoding="utf-8") as fh:
    POS = json.load(fh)


def is_valid_sent(text):
    to_return = True
    n_words = len(text.split())
    if (
            n_words < 3 or
            any(char in text for char in ";:[(") or
            any(char.isdigit() for char in text) or
            "Kriol tu Inglish" in text or
            text[0] != text[0].upper()
    ):
        to_return = False
    return to_return


def get_blocks(text):
    delimiters = list(POS.keys())
    pattern = rf"(?<=[. ])(?:{"|".join(map(re.escape, delimiters))})"
    split_text = [s.strip().replace("\n", "") for s in re.split(pattern, text) if s]
    return split_text


def postprocess_sent(text):
    if text.startswith(")"):
        text = text.replace(")", "").strip()
    text = text.replace("’", "'").replace("‘", "'")
    text = text.replace("–", "-")
    return text

def get_sents(text):
    sent_splits = [s.strip() for s in re.findall(r"[^.?]+[.?]", text) if s]  # end with period or question mark
    kr_eng_sents = []
    for sent in sent_splits:
        if not is_valid_sent(sent):
            continue
        sent = postprocess_sent(sent)
        kr_eng_sents.append(sent)
        if len(kr_eng_sents) == 2:
            return kr_eng_sents[0], kr_eng_sents[1]
    return None, None

def get_pairs(page_text, leftover=None):
    blocks = get_blocks(page_text)

    if leftover:
        blocks[0] = leftover + blocks[0]

    kr_eng_pairs = []
    for block in blocks:
        kriol_sent, eng_sent = get_sents(block)
        if kriol_sent is not None and eng_sent is not None:
            kr_eng_pairs.append((kriol_sent, eng_sent))

    return kr_eng_pairs, leftover


if __name__ == "__main__":
    eng_kriol_data = []
    start_page, end_page = 32-1, 392
    leftover = None
    for i in tqdm(range(start_page, end_page)):
        text = reader.pages[i].extract_text(0)
        kr_eng_pairs, leftover = get_pairs(text, leftover)
        eng_kriol_data.extend(kr_eng_pairs)

    print("Number of Eng-Kriol pairs:", len(eng_kriol_data))

    with open(os.path.join(output_path, "kriol_eng_pairs_dict.json"), "w") as fh:
        json.dump(eng_kriol_data, fh, ensure_ascii=False)
