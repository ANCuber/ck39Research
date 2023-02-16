print("loading...")
import sys

import os
cwd = os.getcwd()
sys.path.append(cwd+'/tools/')
sys.path.append(cwd+'/code/bm25')
import processing_func as pf
import mybm25 as retriver

from transformers import BertTokenizer, EncoderDecoderModel
modeldir =cwd+"/model/bert2bert"
tokenizer = BertTokenizer.from_pretrained(modeldir)
tokenizer.sep_token = '[SEP]'
tokenizer.cls_token = '[CLS]'
model = EncoderDecoderModel.from_pretrained(modeldir)
model.to("cuda")
def processed(s,type):
    if(type==5):
        s = s+'等於1'
    return pf.ReplaceVariableDes(s)

def retrived(s):
    return retriver.retrieve(s,5)

def generate(s,type):
    bat = (s)
    inputs = tokenizer(bat, padding="max_length", truncation=True, max_length=512, return_tensors="pt")
    input_ids = inputs.input_ids.to("cuda")
    attention_mask = inputs.attention_mask.to("cuda")
    print("generating...")
    outputs = model.generate(input_ids, attention_mask=attention_mask)
    outputs_str = tokenizer.batch_decode(outputs,skip_special_tokens=True)
    print("finished")
    # all special tokens including will be removed
    pred = outputs_str[0].replace(' ','')
    pred = pred.split('[var50]')
    pred = pred[0]

    if(type==5):
        pred = pred.split("[Peql]")
        pred = pred[0]
        pred = pred.split("[Ples]")
        pred = pred[0]
        pred = pred.split("[Pbgr]")
        pred = pred[0]
        pred = pred.split("[Pbeg]leq[Pspa]")
        pred = pred[0]
        pred = pred.split("[Pbeg]geq[Pspa]")
        pred = pred[0]
    return pred

def rev(st,s):
    st=pf.ReversePunc(st)
    lst = pf.get_varitoword(s)
    for pair in lst:
        st = st.replace("[var{}]".format(pair[0]),pair[1])
    return st