
from transformers import BertTokenizer, LineByLineTextDataset,BertConfig, BertForMaskedLM, DataCollatorForLanguageModeling,pipeline
# load the model checkpoint
UsedModel = "/home/12518research/ck39Research/code/Pretrain/encoder"
model = BertForMaskedLM.from_pretrained(UsedModel)
# load the tokenizer
tokenizer = BertTokenizer.from_pretrained(UsedModel)

fill_mask = pipeline("fill-mask", model=model, tokenizer=tokenizer)

examples = [
  "[Pbeg][MASK][Plbb[[var1][Prbb]",
  "等腰[MASK]角形",
  "分[MASK]"
]
for example in examples:
  print(example)
  print(tokenizer.tokenize(example))
  for prediction in fill_mask(example):
    print(prediction)
  print("="*50)