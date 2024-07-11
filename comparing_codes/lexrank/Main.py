import json
import math

import rouge
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





rouge = Rouge()
stop_words = open("stopwords.txt", "r", encoding="utf8").readlines()
stop_words = [stop_word.split('\n')[0] for stop_word in stop_words]
documents_summaries = json.load(open("document_summaries.json", "r", encoding="utf-8"))

documents = []
documents_dir = Path('corpus')

for file_path in documents_dir.files('*.txt'):
    print(file_path.split(".txt")[0].split("file")[1])
    with file_path.open(mode='rt', encoding='utf-8') as fp:
        documents.append(fp.readlines())

lxr = LexRank(documents, stopwords=stop_words)

results = []
for serial_no in range(250):
    print("#######",serial_no,"#############")
    row = {}

    document = documents_summaries[serial_no]["document"]
    row["document"] = document
    row["summary"] = documents_summaries[serial_no]['summary-1']

    sentence_dividers = ['।', '|', '!', '\n', '?', ":"]
    sentences = _custom_tokenizer(document, sentence_dividers)

    summary_array = lxr.get_summary(sentences, summary_size=math.ceil(len(sentences) * .25), threshold=.1)
    machine_summary="। ".join(summary_array)

    row["machine-summary"] = machine_summary

    rouge_score = rouge.get_scores(machine_summary, documents_summaries[serial_no]['summary-1'])[0]
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
    results.append(row)

    row = {}
    row["document"] = document
    row["summary"] = documents_summaries[serial_no]['summary-2']
    summary_array = lxr.get_summary(sentences, summary_size=math.ceil(len(sentences) * .25), threshold=.1)
    machine_summary = "। ".join(summary_array)
    row["machine-summary"] = machine_summary

    rouge_score = rouge.get_scores(machine_summary, documents_summaries[serial_no]['summary-2'])[0]
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
    results.append(row)
    # print(rouge_score)

sum_r1_p = 0
sum_r1_r = 0
sum_r1_f = 0
sum_r2_p = 0
sum_r2_r = 0
sum_r2_f = 0
sum_rl_p = 0
sum_rl_r = 0
sum_rl_f = 0

for row in results:
    sum_r1_p += row["rouge-1-p"]
    sum_r1_r += row["rouge-1-r"]
    sum_r1_f += row["rouge-1-f"]
    sum_r2_p += row["rouge-2-p"]
    sum_r2_r += row["rouge-2-r"]
    sum_r2_f += row["rouge-2-f"]
    sum_rl_p += row["rouge-l-p"]
    sum_rl_r += row["rouge-l-r"]
    sum_rl_f += row["rouge-l-f"]

results.append(
    [sum_r1_r / 500, sum_r1_p / 500, sum_r1_f / 500, sum_r2_r / 500, sum_r2_p / 500, sum_r2_f / 500, sum_rl_r / 500,
     sum_rl_p / 500, sum_rl_f / 500])

json.dump(results, open("LexRankResult.json", "w", encoding="utf-8"), ensure_ascii=False, indent=4)




#
# # get summary with classical LexRank algorithm
# summary = lxr.get_summary(sentences, summary_size=2, threshold=.1)
# print(summary)
#
# # ['Mr Osborne said the coalition government was planning to change the tax '
# #  'system "to make it fairer for people on low and middle incomes", and '
# #  'undertake "long-term structural reform" of the banking sector, education and '
# #  'the welfare state.',
# #  'The BBC understands that as chancellor, Mr Osborne, along with the Treasury '
# #  'will retain responsibility for overseeing banks and financial regulation.']
#
#
# # get summary with continuous LexRank
# summary_cont = lxr.get_summary(sentences, threshold=None)
# print(summary_cont)
#
# # ['The BBC understands that as chancellor, Mr Osborne, along with the Treasury '
# #  'will retain responsibility for overseeing banks and financial regulation.']
#
# # get LexRank scores for sentences
# # 'fast_power_method' speeds up the calculation, but requires more RAM
# scores_cont = lxr.rank_sentences(
#     sentences,
#     threshold=None,
#     fast_power_method=False,
# )
# print(scores_cont)
#
# #  [1.0896493024505858,
# #  0.9010711968859021,
# #  1.1139166497016315,
# #  0.8279523250808547,
# #  0.8112028559566362,
# #  1.185228912485382,
# #  1.0709787574388283]