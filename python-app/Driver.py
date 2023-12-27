from exp_modules.expService import get_summary_unranked_sigma as get_akon_summary
from Service import getSummary as get_ksarkar_summary
from rouge import Rouge
from common_utils.FileReader import read_files
import json
from common_utils.Preprocessor import word_divider
from math import ceil
from random import shuffle
import numpy as np 



def random_summary(text):
    sentences,splited_sentences = word_divider(text)
    n = ceil(len(sentences)/4)
    indexlist=list(range(0,len(sentences)))
    shuffle(indexlist)
    nparray = np.array(indexlist)
    summary_indices = nparray[0:n].tolist()
    # picked.sort()
    
    for i in range(len(summary_indices)):
        for j in range(i+1,len(summary_indices)):
            if summary_indices[i]>summary_indices[j]:
                summary_indices[i],summary_indices[j] = summary_indices[j],summary_indices[i]

    summary = ''
    for indx in summary_indices:
        summary+=sentences[indx]+'। '
    
    return summary_indices,summary

    





rouge = Rouge()

#reading evaluation dataset
evaluation_dictionary = {}
with open('datasets/evaluation_dictionary.json','r',encoding='utf-8') as newsjson:
    evaluation_dictionary = json.load(newsjson)



results = {}


# for index in range(0,1000):
# for index in range(1000,2000):
# for index in range(2000,3000):
# for index in range(3000,4000):
for index in range(4000,len(evaluation_dictionary)):
    print(index)
    doc={}    
    document = evaluation_dictionary[f'{index}']["Description"]
    doc["document"]= document
    reference = evaluation_dictionary[f'{index}']['Meta-Summary']
    doc["human"]=reference
    akonsum_ind,akonsummary = get_akon_summary( document)
    doc["akon"]=akonsummary
    doc["akon_ind"]=akonsum_ind
    ksarkar_ind,ksarkarsummary=get_ksarkar_summary(document)
    doc['ksarkar']=ksarkarsummary
    doc['ksarkar_ind']=ksarkar_ind
    random_ind,randomsummary=random_summary(document)
    doc['rand_ind']=random_ind
    doc['random']=randomsummary

    if reference.strip() :
        score = rouge.get_scores(akonsummary,reference)[0]
        doc["akon_r1_r"]=score["rouge-1"]["r"]
        doc["akon_r1_p"]=score["rouge-1"]["p"]
        doc["akon_r1_f"]=score["rouge-1"]["f"]
        doc["akon_r2_r"]=score["rouge-2"]["r"]
        doc["akon_r2_p"]=score["rouge-2"]["p"]
        doc["akon_r2_f"]=score["rouge-2"]["f"]
        doc["akon_rlcs_r"]=score["rouge-l"]["r"]
        doc["akon_rlcs_p"]=score["rouge-l"]["p"]
        doc["akon_rlcs_f"]=score["rouge-l"]["f"]

        score = rouge.get_scores(ksarkarsummary,reference)[0]
        doc["ksarkar_r1_r"]=score["rouge-1"]["r"]
        doc["ksarkar_r1_p"]=score["rouge-1"]["p"]
        doc["ksarkar_r1_f"]=score["rouge-1"]["f"]
        doc["ksarkar_r2_r"]=score["rouge-2"]["r"]
        doc["ksarkar_r2_p"]=score["rouge-2"]["p"]
        doc["ksarkar_r2_f"]=score["rouge-2"]["f"]
        doc["ksarkar_rlcs_r"]=score["rouge-l"]["r"]
        doc["ksarkar_rlcs_p"]=score["rouge-l"]["p"]
        doc["ksarkar_rlcs_f"]=score["rouge-l"]["f"]

        score = rouge.get_scores(randomsummary,reference)[0]
        doc["random_r1_r"]=score["rouge-1"]["r"]
        doc["random_r1_p"]=score["rouge-1"]["p"]
        doc["random_r1_f"]=score["rouge-1"]["f"]
        doc["random_r2_r"]=score["rouge-2"]["r"]
        doc["random_r2_p"]=score["rouge-2"]["p"]
        doc["random_r2_f"]=score["rouge-2"]["f"]
        doc["random_rlcs_r"]=score["rouge-l"]["r"]
        doc["random_rlcs_p"]=score["rouge-l"]["p"]
        doc["random_rlcs_f"]=score["rouge-l"]["f"]

        results[index]=doc

with open(f'output/equalization_5.json', 'w') as filehandle:
    json.dump(results, filehandle)
