summaryFile = open("results/alltexts.txt", "r", encoding="utf-8")
summaryLines = summaryFile.readlines()
summaries = []
for i in range(250):
    line = []
    summaries.append(line)

for line in summaryLines:
    line_divided = line.strip().split(" : ")
    document_lines = open("articles/doc_"+line_divided[0].strip()+".txt", "r", encoding="utf-8").readlines()
    document=""
    for document_line in document_lines:
        document = document + document_line.split("\n")[0].strip()

    summaries[int(line_divided[0].strip())-1].append(document)
    summaries[int(line_divided[0].strip())-1].append(line_divided[1].strip())

for line in summaries:
    print('"', line[0], '", "', line[1], '", "', line[3], '"')