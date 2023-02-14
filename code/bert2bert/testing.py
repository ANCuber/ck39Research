# -*- coding: utf-8 -*-

#-m !pip3 install datasets
#-m !pip3 install transformers

import os
os.environ['CUDA_VISIBLE_DEVICES']='2, 3'

print("Preparing...")
import datasets
import torch
import pandas as pd
from transformers import BertTokenizer, EncoderDecoderModel
from datasets import Dataset, DatasetDict

ModelFolder = '/home/12518research/ck39Research/model/bert2bert'
Checkpoint = '/checkpoint-8000'
DataFolder = "/home/12518research/ck39Research/data/Data/generator/"
filename = 'val_data.csv'

print("Loading tokenizer and model...")

tokenizer = BertTokenizer.from_pretrained(ModelFolder+Checkpoint)
tokenizer.sep_token = '[SEP]'
tokenizer.cls_token = '[CLS]'
model = EncoderDecoderModel.from_pretrained(ModelFolder+Checkpoint)
model.to("cuda")

#test dataset
print("Preparing data...")
df_test = pd.read_csv(DataFolder+filename,sep=",")
TestData = Dataset.from_pandas(df_test)
test_data = TestData
test_size = 3000

test_data = test_data.select(range(test_size))

batch_size = 4 # change to 64 for full evaluation

# map data correctly
def generate_summary(batch):
    # Tokenizer will automatically set [BOS] <text> [EOS]
    # cut off at BERT max length 512
    inputs = tokenizer(batch["retrieved"], padding="max_length", truncation=True, max_length=512, return_tensors="pt")
    input_ids = inputs.input_ids.to("cuda")
    attention_mask = inputs.attention_mask.to("cuda")

    outputs = model.generate(input_ids, attention_mask=attention_mask)

    # all special tokens including will be removed
    output_str = tokenizer.batch_decode(outputs, skip_special_tokens=True)

    batch["pred"] = output_str

    return batch

for_eval = test_data
print("Generating...")
results = test_data.map(generate_summary, batched=True, batch_size=batch_size, remove_columns=["retrieved"])

pred_str = results["pred"]
label_str = results["target"]

ending = '[var50]'
descarr = for_eval["retrieved"]
cnt = 0
print("Output:\n")
for i in range(test_size):
    print("No."+str(i+1)+":")
    desc = descarr[i].split('[SEP]')
    desc = desc[0].replace('[CLS]','')
    print("Description:"+desc,end = '\n\n')

    
    print("Tar:", end='')
    tar = label_str[i]
    tar = tar.replace('[CLS]','')
    tar = tar.replace('[SEP]','')
    tar = tar.replace('[var50]','')
    print(tar,end = '\n\n')
    

    print("Gen:",end = '')
    pred = pred_str[i].replace(' ','')
    pred = pred.split(ending)
    print(pred[0],end = '\n\n')
    if(tar==pred[0]):
        cnt+=1

print(cnt/test_size)

"""
rouge_output = rouge.compute(predictions=pred_str, references=label_str, rouge_types=["rouge2"])["rouge2"].mid

print(rouge_output)
"""
