print("loading...")
import sys
sys.path.append('/home/12518research/ck39Research/tools/')
sys.path.append('/home/12518research/ck39Research/code/bm25')
import processing_func as pf
import mybm25 as retriver

from transformers import BertTokenizer, EncoderDecoderModel
modeldir =  "/home/12518research/ck39Research/model/bert2bert"
tokenizer = BertTokenizer.from_pretrained(modeldir)
tokenizer.sep_token = '[SEP]'
tokenizer.cls_token = '[CLS]'
model = EncoderDecoderModel.from_pretrained(modeldir)
model.to("cuda")
def processed(s):
    return pf.ReplaceVariableDes(s)

def retrived(s):
    return retriver.retrieve(s,5)

def generate(s):
    bat = (s)
    inputs = tokenizer(bat, padding="max_length", truncation=True, max_length=512, return_tensors="pt")
    input_ids = inputs.input_ids.to("cuda")
    attention_mask = inputs.attention_mask.to("cuda")
    print("generating...")
    outputs = model.generate(input_ids, attention_mask=attention_mask)
    print("finished")
    # all special tokens including will be removed
    output_str = tokenizer.batch_decode(outputs, skip_special_tokens=True)
    return output_str

def rev(st,s):
    st=pf.ReversePunc(st)
    lst = pf.get_varitoword(s)
    for pair in lst:
        st = st.replace("[var{}]".format(pair[0]),pair[1])
    return st

