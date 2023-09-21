from Service import getSummary
from rouge import Rouge
from FileReader import read_files
import json

rouge = Rouge()

evaluation_dictionary = read_files()
print(len(evaluation_dictionary['documents']))
print(len(evaluation_dictionary['summary']))

results = {}
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


