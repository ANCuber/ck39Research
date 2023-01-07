import csv
import json

  
# 開啟 CSV 檔案
filename = input("input the file you want to process:")
dir = input("give directory:")
filenamewrite = dir+'/data_dpr.json'
doc_store = dir+'/doc_store.json'
# for the main dpr
with open(filenamewrite,'w',encoding='utf-8') as out:
  with open(filename, newline='',encoding='utf-8') as csvfile:
    lines = csv.reader(csvfile)
    i = 0
    for line in lines:
        dictionary = {
        "dataset": "text2latex",
        "question": line[1],
        "answers": line[0],
        "positive_ctxs": [{'title': line[0] , 'text': line[0], 'score': 1000, 'title_score': 1000, 'passage_id': i}],
        "negative_ctxs":  [],
        "hard_negative_ctxs":  [],
        }
        json_obj = json.dumps(dictionary,indent=4,ensure_ascii=False).encode('utf-8') 
        i+=1
        out.write(json_obj.decode())     
        out.write(',')
# for dpr document store
with open(filename, newline='',encoding='utf-8') as csvfile:
  with open(doc_store,'w',encoding='utf-8') as doc:
    lines = csv.reader(csvfile)
    for line in lines:
      dictionary={
        'content':[]
      }
      dictionary['content']=line[0]
      json_obj = json.dumps(dictionary,indent=4,ensure_ascii=False).encode('utf-8')
      doc.write(json_obj.decode())
      doc.write(',')










