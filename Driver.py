from rouge import Rouge
import json
from Service import get_summary


documents_summaries = json.load(open("document_summaries.json", "r", encoding="utf-8"))
rouge = Rouge()
sigmas=[9.0,10.0]
resultComp=open("resultcomp.txt","a+",encoding="utf-8")

for sig in sigmas:
    fahim = []

    for serial_no in range(250):
        print(serial_no)
        row = {}

        document = documents_summaries[serial_no]["document"]
        row["document"]=document
        row["summary"]=documents_summaries[serial_no]['summary-1']
        # print(document)

        _,machine_summary = get_summary(document,size=0.25,sigma=sig)
        row["machine-summary"]=machine_summary
        # print(machine_summary)
        # print(documents_summaries[serial_no]['summary-1'])

        rouge_score = rouge.get_scores(machine_summary, documents_summaries[serial_no]['summary-1'])[0]
        row["rouge-1-r"]=rouge_score['rouge-1']['r']
        row["rouge-1-p"]=rouge_score['rouge-1']['p']
        row["rouge-1-f"]=rouge_score['rouge-1']['f']
        row["rouge-2-r"]=rouge_score['rouge-2']['r']
        row["rouge-2-p"]=rouge_score['rouge-2']['p']
        row["rouge-2-f"]=rouge_score['rouge-2']['f']
        row["rouge-l-r"]=rouge_score['rouge-l']['r']
        row["rouge-l-p"]=rouge_score['rouge-l']['p']
        row["rouge-l-f"]=rouge_score['rouge-l']['f']

        fahim.append(row)

        row = {}
        row["document"] = document
        row["summary"]=documents_summaries[serial_no]['summary-2']
        _,machine_summary = get_summary(document,size=.25,sigma=sig)
        row["machine-summary"]=machine_summary

        rouge_score = rouge.get_scores(machine_summary, documents_summaries[serial_no]['summary-2'])[0]
        row["rouge-1-r"]=rouge_score['rouge-1']['r']
        row["rouge-1-p"]=rouge_score['rouge-1']['p']
        row["rouge-1-f"]=rouge_score['rouge-1']['f']
        row["rouge-2-r"]=rouge_score['rouge-2']['r']
        row["rouge-2-p"]=rouge_score['rouge-2']['p']
        row["rouge-2-f"]=rouge_score['rouge-2']['f']
        row["rouge-l-r"]=rouge_score['rouge-l']['r']
        row["rouge-l-p"]=rouge_score['rouge-l']['p']
        row["rouge-l-f"]=rouge_score['rouge-l']['f']

        fahim.append(row)
        # print(rouge_score)

    sum_r1_p=0
    sum_r1_r = 0
    sum_r1_f=0
    sum_r2_p=0
    sum_r2_r = 0
    sum_r2_f=0
    sum_rl_p=0
    sum_rl_r = 0
    sum_rl_f=0

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

    fahim.append([sum_r1_r/500,sum_r1_p/500,sum_r1_f/500,sum_r2_r/500,sum_r2_p/500,sum_r2_f/500,sum_rl_r/500,sum_rl_p/500,sum_rl_f/500])
    resultComp.write(str(sig)+" : "+str(sum_r1_r/500)+" - "+str(sum_r1_p/500)+" - "+str(sum_r1_f/500)+" - "+str(sum_r2_r/500)+" - "+str(sum_r2_p/500)+" - "+str(sum_r2_f/500)+" - "+str(sum_rl_r/500)+" - "+str(sum_rl_p/500)+" - "+str(sum_rl_f/500))
    json.dump(fahim, open("fahimResult"+str(sig)+".json", "w", encoding="utf-8"), ensure_ascii=False, indent=4)

resultComp.close()