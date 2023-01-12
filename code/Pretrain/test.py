
from transformers import BertTokenizer, LineByLineTextDataset,BertConfig, BertForMaskedLM, DataCollatorForLanguageModeling,pipeline
# load the model checkpoint
UsedModel = "/home/12518research/ck39Research/code/Pretrain/model"
model = BertForMaskedLM.from_pretrained(UsedModel)
# load the tokenizer
tokenizer = BertTokenizer.from_pretrained(UsedModel)

fill_mask = pipeline("fill-mask", model=model, tokenizer=tokenizer)

examples = [
  "[Plbb][var1][Prbb][MASK][Plbb][var2][Prbb]",
  "[Pbeg]frac[Plbb][var1][Prbb][MASK][var2][Prbb]",
  "[Pbeg][MASK][Plbb][var1][Prbb]",
  "[Pbeg][MASK][Plbb][var1][Prbb][Plbb][var2][Prbb]",
  "the weather today is very [MASK].",
  "今天天氣真[MASK]。",
  "根號[MASK]。",
  "[MASK]號1",
  "有[MASK]數有稠密性"
]
for example in examples:
  print(example)
  for prediction in fill_mask(example):
    print(f"{prediction['sequence']}, confidence: {prediction['score']}")
  print("="*50)