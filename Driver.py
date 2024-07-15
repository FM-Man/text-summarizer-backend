from rouge import Rouge
import json
from Service_firstrank_e_a_m2__2s2_ import get_summary
import pandas as pd


def dataset_testing(document, summary_1, summary_2, sigma, serial_no, rouge, result_file):
    print("#######", sigma, "->", serial_no, "#############")
    row = {}

    row["document"] = document
    row["summary"] = summary_1

    _, machine_summary = get_summary(document, size=0.20, sigma=sig)
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
    result_file.append(row)

    row = {}
    row["document"] = document
    row["summary"] = summary_2
    _, machine_summary = get_summary(document, size=.20, sigma=sig)
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
    result_file.append(row)

    # row = {}
    # row["document"] = document
    # row["summary"] = summary_3
    # _, machine_summary = get_summary(document, size=.20, sigma=sig)
    # row["machine-summary"] = machine_summary

    # rouge_score = rouge.get_scores(machine_summary, summary_3)[0]
    # row["rouge-1-r"] = rouge_score['rouge-1']['r']
    # row["rouge-1-p"] = rouge_score['rouge-1']['p']
    # row["rouge-1-f"] = rouge_score['rouge-1']['f']
    # row["rouge-2-r"] = rouge_score['rouge-2']['r']
    # row["rouge-2-p"] = rouge_score['rouge-2']['p']
    # row["rouge-2-f"] = rouge_score['rouge-2']['f']
    # row["rouge-l-r"] = rouge_score['rouge-l']['r']
    # row["rouge-l-p"] = rouge_score['rouge-l']['p']
    # row["rouge-l-f"] = rouge_score['rouge-l']['f']
    # print(rouge_score["rouge-1"]["f"], " ", rouge_score["rouge-2"]["f"], " ", rouge_score["rouge-l"]["f"])
    # result_file.append(row)


sigmas = [
    5e-11
]

# documents_summaries_1 = pd.read_csv("comparing_codes/evaluation_dataset_2/BangladeshNewsData.csv", encoding='utf-8', delimiter=',')
# documents_summaries_2 = pd.read_csv("comparing_codes/evaluation_dataset_2/BusinessNewsData.csv", encoding='utf-8', delimiter=',')
# documents_summaries_3 = pd.read_csv("comparing_codes/evaluation_dataset_2/EntertainmentNewsData.csv", encoding='utf-8', delimiter=',')
# documents_summaries_4 = pd.read_csv("comparing_codes/evaluation_dataset_2/OpinionNewsData.csv", encoding="utf-8", delimiter=",")
# documents_summaries_5 = pd.read_csv("comparing_codes/evaluation_dataset_2/PoliticsNewsData.csv", encoding="utf-8", delimiter=",")
# documents_summaries_6 = pd.read_csv("comparing_codes/evaluation_dataset_2/SportsNewsData.csv", encoding="utf-8", delimiter=",")
# documents_summaries_7 = pd.read_csv("comparing_codes/evaluation_dataset_2/WorldsNewsData.csv", encoding="utf-8", delimiter=",")

# document_summaries = json.load(open("dataset_1_document_summaries.json",encoding="utf-8"))

# document_summaries = pd.read_csv("comparing_codes/evaluation_dataset_3/BNLPC_CSV_Dataset.csv",encoding="utf-8",delimiter=",")

document_summaries = pd.read_csv("comparing_codes/evaluation_dataset_4/Evaluation_Dataset_4.csv",encoding="utf-8",delimiter=",")
rouge = Rouge()

resultComp = open("fahim_firstrank_e(a(m2)_2s2)/ex1_ds4/resultcomp.csv", "w+", encoding="utf-8")
resultComp.write("Sigma,rouge-1-r,rouge-1-p,rouge-1-f,rouge-2-r,rouge-2-p,rouge-2-f,rouge-l-r,rouge-l-p,rouge-l-f\n")
resultComp.close()
result_compilation = []

for sig in sigmas:
    serial_no = 1
    # for row_index, row in documents_summaries_1.iterrows():
    #     try:
    #         dataset_testing(row["Document"], row["summary-1"], row["summary-2"], sig, serial_no)
    #         serial_no += 2
    #     except:
    #         pass
    # for row_index, row in documents_summaries_2.iterrows():
    #     try:
    #         dataset_testing(row["Document"], row["summary-1"], row["summary-2"], sig, serial_no)
    #         serial_no += 2
    #     except:
    #         pass
    # for row_index, row in documents_summaries_3.iterrows():
    #     try:
    #         dataset_testing(row["Document"], row["summary-1"], row["summary-2"], sig, serial_no)
    #         serial_no += 2
    #     except:
    #         pass
    # for row_index, row in documents_summaries_4.iterrows():
    #     try:
    #         dataset_testing(row["Document"], row["summary-1"], row["summary-2"], sig, serial_no)
    #         serial_no += 2
    #     except:
    #         pass
    # for row_index, row in documents_summaries_5.iterrows():
    #     try:
    #         dataset_testing(row["Document"], row["summary-1"], row["summary-2"], sig, serial_no)
    #         serial_no += 2
    #     except:
    #         pass
    # for row_index, row in documents_summaries_6.iterrows():
    #     try:
    #         dataset_testing(row["Document"], row["summary-1"], row["summary-2"], sig, serial_no)
    #         serial_no += 2
    #     except:
    #         pass
    # for row_index, row in documents_summaries_7.iterrows():
    #     try:
    #         dataset_testing(row["Document"], row["summary-1"], row["summary-2"], sig, serial_no)
    #         serial_no += 2
    #     except:
    #         pass
    for row_index,row in document_summaries.iterrows():
        try: 
            dataset_testing(row["Document"],row["summary_1"],row["summary_2"],sig,serial_no,rouge,result_compilation)
            serial_no+=3
        except: pass

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

    for row in result_compilation:
        sum_r1_p += row["rouge-1-p"]
        sum_r1_r += row["rouge-1-r"]
        sum_r1_f += row["rouge-1-f"]
        sum_r2_p += row["rouge-2-p"]
        sum_r2_r += row["rouge-2-r"]
        sum_r2_f += row["rouge-2-f"]
        sum_rl_p += row["rouge-l-p"]
        sum_rl_r += row["rouge-l-r"]
        sum_rl_f += row["rouge-l-f"]

    length = len (result_compilation)
    result_compilation.append(
        [sum_r1_r / length, sum_r1_p / length, sum_r1_f / length, sum_r2_r / length, sum_r2_p / length,
         sum_r2_f / length, sum_rl_r / length,
         sum_rl_p / length, sum_rl_f / length])
    resultComp = open("fahim_firstrank_e(a(m2)_2s2)/ex1_ds4/resultcomp.csv", "a+", encoding="utf-8")
    resultComp.write(str(sig) + "," + str(sum_r1_r / length) + "," + str(sum_r1_p / length) + "," + str(
        sum_r1_f / length) + "," + str(sum_r2_r / length) + "," + str(sum_r2_p / length) + "," + str(
        sum_r2_f / length) + "," + str(sum_rl_r / length) + "," + str(sum_rl_p / length) + "," + str(
        sum_rl_f / length) + "\n")
    resultComp.close()
    json.dump(result_compilation,
              open("fahim_firstrank_e(a(m2)_2s2)/ex1_ds4/fahim_dataset_4_" + str(sig) + ".json", "w",
                   encoding="utf-8"), ensure_ascii=False, indent=4)
