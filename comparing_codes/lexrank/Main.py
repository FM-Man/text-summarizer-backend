import json
import math

import pandas as pd
from lexrank import STOPWORDS, LexRank
from path import Path
from nltk.tokenize import RegexpTokenizer
import re
from rouge import Rouge


def _custom_tokenizer(text, dividers):
    # idk what this regex part is doing. got it from stack overflow.
    divider_pattern = '|'.join(map(re.escape, dividers))
    tokenizer = RegexpTokenizer(f'[^{divider_pattern}]+|[{divider_pattern}]')
    tokens = tokenizer.tokenize(text)

    # removes the divider tokens and also strips them
    processed_tokens = []
    for token in tokens:
        if token.strip() and token not in dividers:
            processed_tokens.append(token.strip())

    return processed_tokens

def dataset_testing(document, summary_1, summary_2, summary_3, serial_no,result_compilation,rouge,lxr):
    print("#######", serial_no, "#############")
    row = {}

    row["document"] = document
    row["summary"] = summary_1

    sentence_dividers = ['।', '|', '!', '\n', '?', ":"]
    sentences = _custom_tokenizer(document, sentence_dividers)
    summary_array = lxr.get_summary(sentences, threshold=None)
    machine_summary = "। ".join(summary_array)
    row["machine-summary"] = machine_summary

    rouge_score = rouge.get_scores(machine_summary, summary_1)[0]
    row["rouge-1-r"] = rouge_score['rouge-1']['r']
    row["rouge-1-p"] = rouge_score['rouge-1']['p']
    row["rouge-1-f"] = rouge_score['rouge-1']['f']
    row["rouge-2-r"] = rouge_score['rouge-2']['r']
    row["rouge-2-p"] = rouge_score['rouge-2']['p']
    row["rouge-2-f"] = rouge_score['rouge-2']['f']
    row["rouge-l-r"] = rouge_score['rouge-l']['r']
    row["rouge-l-p"] = rouge_score['rouge-l']['p']
    row["rouge-l-f"] = rouge_score['rouge-l']['f']
    print(rouge_score["rouge-1"]["f"], " ", rouge_score["rouge-2"]["f"], " ", rouge_score["rouge-l"]["f"])
    result_compilation.append(row)

    row = {}
    row["document"] = document
    row["summary"] = summary_2
    summary_array = lxr.get_summary(sentences, threshold=None)
    machine_summary = "। ".join(summary_array)
    row["machine-summary"] = machine_summary

    rouge_score = rouge.get_scores(machine_summary, summary_2)[0]
    row["rouge-1-r"] = rouge_score['rouge-1']['r']
    row["rouge-1-p"] = rouge_score['rouge-1']['p']
    row["rouge-1-f"] = rouge_score['rouge-1']['f']
    row["rouge-2-r"] = rouge_score['rouge-2']['r']
    row["rouge-2-p"] = rouge_score['rouge-2']['p']
    row["rouge-2-f"] = rouge_score['rouge-2']['f']
    row["rouge-l-r"] = rouge_score['rouge-l']['r']
    row["rouge-l-p"] = rouge_score['rouge-l']['p']
    row["rouge-l-f"] = rouge_score['rouge-l']['f']
    print(rouge_score["rouge-1"]["f"], " ", rouge_score["rouge-2"]["f"], " ", rouge_score["rouge-l"]["f"])
    result_compilation.append(row)

    row = {}
    row["document"] = document
    row["summary"] = summary_3
    summary_array = lxr.get_summary(sentences, threshold=None)
    machine_summary = "। ".join(summary_array)
    row["machine-summary"] = machine_summary

    rouge_score = rouge.get_scores(machine_summary, summary_3)[0]
    row["rouge-1-r"] = rouge_score['rouge-1']['r']
    row["rouge-1-p"] = rouge_score['rouge-1']['p']
    row["rouge-1-f"] = rouge_score['rouge-1']['f']
    row["rouge-2-r"] = rouge_score['rouge-2']['r']
    row["rouge-2-p"] = rouge_score['rouge-2']['p']
    row["rouge-2-f"] = rouge_score['rouge-2']['f']
    row["rouge-l-r"] = rouge_score['rouge-l']['r']
    row["rouge-l-p"] = rouge_score['rouge-l']['p']
    row["rouge-l-f"] = rouge_score['rouge-l']['f']
    print(rouge_score["rouge-1"]["f"], " ", rouge_score["rouge-2"]["f"], " ", rouge_score["rouge-l"]["f"])
    result_compilation.append(row)




rouge = Rouge()

documents_summaries_1 = pd.read_csv("../evaluation_dataset_3/BNLPC_CSV_Dataset.csv", encoding='utf-8', delimiter=',')
# documents_summaries_2 = pd.read_csv("../evaluation_dataset_2/BusinessNewsData.csv", encoding='utf-8', delimiter=',')
# documents_summaries_3 = pd.read_csv("../evaluation_dataset_2/EntertainmentNewsData.csv", encoding='utf-8',
#                                     delimiter=',')
# documents_summaries_4 = pd.read_csv("../evaluation_dataset_2/OpinionNewsData.csv", encoding="utf-8", delimiter=",")
# documents_summaries_5 = pd.read_csv("../evaluation_dataset_2/PoliticsNewsData.csv", encoding="utf-8", delimiter=",")
# documents_summaries_6 = pd.read_csv("../evaluation_dataset_2/SportsNewsData.csv", encoding="utf-8", delimiter=",")
# documents_summaries_7 = pd.read_csv("../evaluation_dataset_2/WorldsNewsData.csv", encoding="utf-8", delimiter=",")

documents = []
documents_dir = Path('corpus')

for file_path in documents_dir.files('*.txt'):
    print(file_path.split(".txt")[0].split("file")[1])
    with file_path.open(mode='rt', encoding='utf-8') as fp:
        documents.append(fp.readlines())

lxr = LexRank(documents, stopwords=STOPWORDS["bn"])

result_file = []
serial_no=1
for row_index, row in documents_summaries_1.iterrows():
    try:
        dataset_testing(row["Document"], row["summary_1"], row["summary_2"], row["summary_3"], serial_no,result_file,rouge, lxr)
        serial_no += 3
    except Exception as e:
        pass
# for row_index, row in documents_summaries_2.iterrows():
#     try:
#         dataset_testing(row["Document"], row["summary-1"], row["summary-2"],serial_no,result_file,rouge, lxr)
#         serial_no += 2
#     except Exception as e:
#         pass
# for row_index, row in documents_summaries_3.iterrows():
#     try:
#         dataset_testing(row["Document"], row["summary-1"], row["summary-2"],serial_no,result_file,rouge, lxr)
#         serial_no += 2
#     except Exception as e:
#         pass
# for row_index, row in documents_summaries_4.iterrows():
#     try:
#         dataset_testing(row["Document"], row["summary-1"], row["summary-2"],serial_no,result_file,rouge, lxr)
#         serial_no += 2
#     except Exception as e:
#         pass
# for row_index, row in documents_summaries_5.iterrows():
#     try:
#         dataset_testing(row["Document"], row["summary-1"], row["summary-2"],serial_no,result_file,rouge, lxr)
#         serial_no += 2
#     except Exception as e:
#         pass
# for row_index, row in documents_summaries_6.iterrows():
#     try:
#         dataset_testing(row["Document"], row["summary-1"], row["summary-2"],serial_no,result_file,rouge, lxr)
#         serial_no += 2
#     except Exception as e:
#         pass
# for row_index, row in documents_summaries_7.iterrows():
#     try:
#         dataset_testing(row["Document"], row["summary-1"], row["summary-2"],serial_no,result_file,rouge, lxr)
#         serial_no += 2
#     except Exception as e:
#         pass

serial_no -= 1

sum_r1_p = 0
sum_r1_r = 0
sum_r1_f = 0
sum_r2_p = 0
sum_r2_r = 0
sum_r2_f = 0
sum_rl_p = 0
sum_rl_r = 0
sum_rl_f = 0

for row in result_file:
    sum_r1_p += row["rouge-1-p"]
    sum_r1_r += row["rouge-1-r"]
    sum_r1_f += row["rouge-1-f"]
    sum_r2_p += row["rouge-2-p"]
    sum_r2_r += row["rouge-2-r"]
    sum_r2_f += row["rouge-2-f"]
    sum_rl_p += row["rouge-l-p"]
    sum_rl_r += row["rouge-l-r"]
    sum_rl_f += row["rouge-l-f"]
length = len(result_file)
result_file.append(
    [sum_r1_r / length, sum_r1_p / length, sum_r1_f / length, sum_r2_r / length, sum_r2_p / length, sum_r2_f / length, sum_rl_r / length,
     sum_rl_p / length, sum_rl_f / length])

json.dump(result_file, open("lexRankResult_dataset_3.json", "w", encoding="utf-8"), ensure_ascii=False, indent=4)

