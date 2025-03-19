import json
import jsonlines
import time
import openai
import pickle
from collections import defaultdict
from gpt4access import call_gpt4v
from tqdm import tqdm
openai.api_key = "xxxxxxxxxxxxxxxxx"


data = dict()
rag_info = dict()
answer = defaultdict(dict)
id = 0

with open("the path of the jsonl test file", "r", encoding='utf8') as fin:
    for item in jsonlines.Reader(fin):
        data[id] = item
        id += 1
    fin.close()


for key in tqdm(data.keys()):
    if 'text' in data[key]:
        meme_text = data[key]['text']
    else:
        meme_text = data[key]['org_sent']
    if 'img' in data[key]:
        img = data[key]['img']
    else:
        img = data[key]['image']

    if 'id' in data[key]:
        id = data[key]['id']
    else:
        id = img.replace('.png', '')
    
    img_path = "the path of the meme image file"+img

    INSTRUCTION = "Given the meme, with the text '"+meme_text+"' accompanied by the image, is this meme harmful? Answer: only Yes/No."

    response = call_gpt4v(img_path, INSTRUCTION)

    if response != "":
        try:
            response = response.json()
        except:
            response = ""

    #ans = response["choices"][0]["message"]["content"]

    answer[id] = response

    with open("the file name of the pickle file", "wb") as fout:
        pickle.dump(answer, fout)