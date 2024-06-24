from rouge import Rouge
import json
from ServiceNew import get_summary

documents_summaries = json.load(open("document_summaries.json", "r", encoding="utf-8"))
rouge = Rouge()
sigmas = [0.000000000001,0.0000000000025,0.000000000005,0.0000000000075,
          0.00000000001,0.000000000025,0.00000000005,0.000000000075,
          0.0000000001,0.00000000025,0.0000000005,0.00000000075,
          0.000000001,0.0000000025,0.000000005,0.0000000075,
          0.00000001,0.000000025,0.00000005,0.000000075,
          0.0000001,0.00000025,0.0000005,0.00000075,
          0.000001,0.0000025,0.000005,0.0000075,
          0.00001,0.000025,0.00005,0.000075,
          0.0001,0.00025,0.0005,0.00075,
          0.001,0.0025,0.005,0.0075,
          0.01,0.025,0.05,0.075,
          0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9,
          1.0,2.0,3.0,4.0,5.0,6.0,7.0,8.0,9.0,10.0]

resultComp = open("fahimAverageWordSimilarityResult/resultcomp.csv", "w+", encoding="utf-8")
resultComp.write("Sigma,rouge-1-r,rouge-1-p,rouge-1-f,rouge-2-r,rouge-2-p,rouge-2-f,rouge-l-r,rouge-l-p,rouge-l-f,tn-r1-f,tn-r2-f,tn-rl-f")
resultComp.close()
resultComp = open("fahimAverageWordSimilarityResult/resultcomp.csv", "a+", encoding="utf-8")

for sig in sigmas:
    fahim = []

    for serial_no in range(250):
        print("#######",sig,"->",serial_no,"#############")
        row = {}

        document = documents_summaries[serial_no]["document"]
        row["document"] = document
        row["summary"] = documents_summaries[serial_no]['summary-1']
        # print(document)

        _, machine_summary = get_summary(document, size=0.25, sigma=sig)
        row["machine-summary"] = machine_summary
        # print(machine_summary)
        # print(documents_summaries[serial_no]['summary-1'])

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
        fahim.append(row)

        row = {}
        row["document"] = document
        row["summary"] = documents_summaries[serial_no]['summary-2']
        _, machine_summary = get_summary(document, size=.25, sigma=sig)
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
        fahim.append(row)
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

    for row in fahim:
        sum_r1_p += row["rouge-1-p"]
        sum_r1_r += row["rouge-1-r"]
        sum_r1_f += row["rouge-1-f"]
        sum_r2_p += row["rouge-2-p"]
        sum_r2_r += row["rouge-2-r"]
        sum_r2_f += row["rouge-2-f"]
        sum_rl_p += row["rouge-l-p"]
        sum_rl_r += row["rouge-l-r"]
        sum_rl_f += row["rouge-l-f"]

    fahim.append(
        [sum_r1_r / 500, sum_r1_p / 500, sum_r1_f / 500, sum_r2_r / 500, sum_r2_p / 500, sum_r2_f / 500, sum_rl_r / 500,
         sum_rl_p / 500, sum_rl_f / 500])
    resultComp.write(str(sig) + "," + str(sum_r1_r / 500) + "," + str(sum_r1_p / 500) + "," + str(
        sum_r1_f / 500) + "," + str(sum_r2_r / 500) + "," + str(sum_r2_p / 500) + "," + str(
        sum_r2_f / 500) + "," + str(sum_rl_r / 500) + "," + str(sum_rl_p / 500) + "," + str(sum_rl_f / 500)+",0.490588947,0.381699937,0.445846941\n")
    json.dump(fahim, open("fahimAverageWordSimilarityResult/fahimResult" + str(sig) + ".json", "w", encoding="utf-8"), ensure_ascii=False, indent=4)

resultComp.close()
