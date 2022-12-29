
from transformers import BertTokenizer, LineByLineTextDataset,BertConfig, BertForMaskedLM, DataCollatorForLanguageModeling,pipeline
# load the model checkpoint
model = BertForMaskedLM.from_pretrained("/home/12518research/ck39Research/code/Pretrain/model")
# load the tokenizer
tokenizer = BertTokenizer.from_pretrained("/home/12518research/ck39Research/code/Pretrain/model")

fill_mask = pipeline("fill-mask", model=model, tokenizer=tokenizer)

examples = [
  "[Plbb][var1][Prbb][MASK][Plbb][var2][Prbb]",
  "[Pbeg]frac[Plbb][var1][Prbb][MASK][var2][Prbb]",
  "[Pbeg][MASK][Plbb][var1][Prbb]",
  "[Pbeg][MASK][Plbb][var1][Prbb][Plbb][var2][Prbb]"
]
for example in examples:
  for prediction in fill_mask(example):
    print(f"{prediction['sequence']}, confidence: {prediction['score']}")
  print("="*50)