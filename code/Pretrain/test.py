
from transformers import BertTokenizer, LineByLineTextDataset,BertConfig, BertForMaskedLM, DataCollatorForLanguageModeling,pipeline
# load the model checkpoint
UsedModel = "/home/12518research/ck39Research/code/Pretrain/decoder"
model = BertForMaskedLM.from_pretrained(UsedModel)
# load the tokenizer
tokenizer = BertTokenizer.from_pretrained(UsedModel)

fill_mask = pipeline("fill-mask", model=model, tokenizer=tokenizer)

examples = [
  "[Plbb][var1][Prbb][MASK][Plbb][var2][Prbb]",
  "[Pbeg]frac[Plbb][var1][Prbb][MASK][var2][Prbb]",
  "[Pbeg][MASK][Plbb][var1][Prbb]",
  "[Pbeg][MASK]rt[Plbb]3[Prbb]",
]
for example in examples:
  print(example)
  for prediction in fill_mask(example):
    print(f"{prediction['sequence']}, confidence: {prediction['score']}")
  print("="*50)