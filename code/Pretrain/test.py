
from transformers import BertTokenizer, LineByLineTextDataset,BertConfig, BertForMaskedLM, DataCollatorForLanguageModeling,pipeline
# load the model checkpoint
import os
cwd = os.getcwd()
UsedModel = cwd+"/model/bert-p20000"
model = BertForMaskedLM.from_pretrained(UsedModel)
# load the tokenizer
tokenizer = BertTokenizer.from_pretrained(UsedModel)

fill_mask = pipeline("fill-mask", model=model, tokenizer=tokenizer)

examples = [
  "[Pbeg][MASK][Plbb][var1][Prbb]",
  "[var1][MASK]之[var2]",
  "3[MASK][var1]分之[var2]"
]
for example in examples:
  print(example)
  print(tokenizer.tokenize(example))
  for prediction in fill_mask(example):
    print(prediction)
  print("="*50)