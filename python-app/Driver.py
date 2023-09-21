from Service import getSummary
from rouge import Rouge
from FileReader import read_files
import json

rouge = Rouge()

evaluation_dictionary = read_files()
print(len(evaluation_dictionary['documents']))
print(len(evaluation_dictionary['summary']))

results = {}
results_for_excell={}
for index in range(len(evaluation_dictionary['documents'])):
    print(index)
    
    summary = getSummary(evaluation_dictionary['documents'][index])
    reference = evaluation_dictionary['summary'][2*index]
    score = rouge.get_scores(summary,reference)[0]
    results[f'doc_{index+1}_sum_1']=score
    

    summary = getSummary(evaluation_dictionary['documents'][index])
    reference = evaluation_dictionary['summary'][2*index+1]
    score = rouge.get_scores(summary,reference)[0]
    results[f'doc_{index+1}_sum_2']=score



with open('output.json', 'w') as filehandle:
    json.dump(results, filehandle)

avg_result = {
    "rouge-1":{
        "r": 0.0,
        "p": 0.0,
        "f": 0.0
    },
    "rouge-2": {
        "r": 0.0,
        "p": 0.0,
        "f": 0.0
    },
    "rouge-l": {
        "r": 0.0,
        "p": 0.0,
        "f": 0.0
    }
}
length = len(results.values())
for result in results.values():
    avg_result["rouge-1"]["r"] += (1/length) * result["rouge-1"]["r"]
    avg_result["rouge-1"]["p"] += (1/length) * result["rouge-1"]["p"]
    avg_result["rouge-1"]["f"] += (1/length) * result["rouge-1"]["f"]
    avg_result["rouge-2"]["r"] += (1/length) * result["rouge-2"]["r"]
    avg_result["rouge-2"]["p"] += (1/length) * result["rouge-2"]["p"]
    avg_result["rouge-2"]["f"] += (1/length) * result["rouge-2"]["f"]
    avg_result["rouge-l"]["r"] += (1/length) * result["rouge-l"]["r"]
    avg_result["rouge-l"]["p"] += (1/length) * result["rouge-l"]["p"]
    avg_result["rouge-l"]["f"] += (1/length) * result["rouge-l"]["f"]


with open('avg_output.json', 'w') as filehandle:
    json.dump(avg_result, filehandle)
