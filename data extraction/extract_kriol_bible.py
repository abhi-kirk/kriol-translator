import os
import json
from tqdm import tqdm
from selenium import webdriver
from selenium.webdriver.common.by import By

base_url = "https://live.bible.is/bible"
kriol_bible, eng_bible = "BZJBSW", "ENGWEB"

base_path = "/Users/abhi/Documents/projects/translator/experiments/kriol-data/"
with open(os.path.join(base_path, "bible_authors_dict.json"), "r", encoding="utf-8") as fh:
    AUTHORS = json.load(fh)

op = webdriver.ChromeOptions()
op.add_argument("headless")
driver = webdriver.Chrome(options=op)

def scrape_webpage(url):
    texts = {}
    driver.get(url)
    elements = driver.find_elements(By.XPATH, "//span[@data-verseid]")
    verse_num = 1
    for element in elements:
        text = element.text.strip()
        if len(text) > 0 and text[0].isdigit():
            num = int(text.split()[0])
            verse_text = text.replace(str(verse_num), "").strip()
            if abs(num - verse_num) > 5:
                break
            while num != verse_num:
                texts[verse_num] = "-"
                verse_num += 1
            texts[verse_num] = verse_text
            verse_num += 1
    return list(texts.values())


def postprocess_texts(kr_list, eng_list):
    kr_list_new, eng_list_new = [], []
    n = len(kr_list)
    for i in range(n):
        if kr_list[i] == "-" and i < n-1:
            eng_list[i+1] = " ".join([eng_list[i], eng_list[i+1]])
        else:
            kr_list_new.append(kr_list[i])
            eng_list_new.append(eng_list[i])

    assert len(kr_list_new) == len(eng_list_new)
    return kr_list_new, eng_list_new


def get_pairs(author, page_id):
    kriol_url = "/".join([base_url, kriol_bible, author, str(page_id)])
    eng_url = "/".join([base_url, eng_bible, author, str(page_id)])

    kriol_texts = scrape_webpage(kriol_url)
    eng_texts = scrape_webpage(eng_url)
    if len(eng_texts) > len(kriol_texts):
        eng_texts = eng_texts[:len(kriol_texts)]
    elif len(kriol_texts) > len(eng_texts):
        kriol_texts = kriol_texts[:len(eng_texts)]

    kriol_texts, eng_texts = postprocess_texts(kriol_texts, eng_texts)
    return list(zip(kriol_texts, eng_texts))


if __name__ == "__main__":
    eng_kriol_data = []
    for author in AUTHORS:
        attr = AUTHORS[author]
        num_pages = int(attr.split("/")[1])
        for page_id in tqdm(range(1, num_pages+1), desc=author):
            kr_eng_pairs = get_pairs(author, page_id)
            eng_kriol_data.extend(kr_eng_pairs)

    print("Number of Eng-Kriol pairs:", len(eng_kriol_data))

    with open(os.path.join(base_path, "kriol_eng_pairs_bible.json"), "w") as fh:
        json.dump(eng_kriol_data, fh, ensure_ascii=False)
