import json
summaryFile = open("document_summaries.csv", "r", encoding="utf-8")
summaryLines = summaryFile.readlines()
summaries = []

for line in summaryLines:
    line_divided = line.strip().split("</s>")
    line_filtered = []
    for element in line_divided:
        if element != "" and element != ',':
            line_filtered.append(element)
    print(len(line_filtered))
    summaries.append({"document": line_filtered[0], "summary-1": line_filtered[1], "summary-2": line_filtered[2]})

json.dump(summaries, open("document_summaries.json", "w", encoding="utf-8"), ensure_ascii=False, indent=4)