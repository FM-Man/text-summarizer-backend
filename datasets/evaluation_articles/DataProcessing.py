file = open("results/alltexts.txt","r", encoding="utf8")
lines=file.readlines()
lines_to_actually_work=[]
for line in lines:
    if not line.startswith("#") and line.strip():
        cut_lines = line.split("\n")[0].split(":")
        line_data={}
        line_data["doc"] = cut_lines[0]
        line_data["sentences"] = cut_lines[1].split(",")
        lines_to_actually_work.append(line_data)

articles_after_work = []
for article in lines_to_actually_work:
    doc = open("articles/doc_"+article["doc"]+".txt","r", encoding="utf8")
    sentences=doc.readlines()
    sentences_to_pick_index = article["sentences"]
    sentences_picked=[]
    for sentence_index in sentences_to_pick_index:
        sentences_picked.append(sentences[int(sentence_index)-1])
    same_line_summary=""
    for sentence in sentences_picked:
        same_line_summary=same_line_summary + sentence.split("\n")[0].strip()+" "
    print(article["doc"],":",same_line_summary)

# print(lines_to_actually_work)