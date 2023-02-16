import os
cwd = os.getcwd()
from transformers import T5Tokenizer, T5ForConditionalGeneration
Usedmodel =cwd+"/code/Pretrain/model"
tokenizer = T5Tokenizer.from_pretrained(Usedmodel)
model = T5ForConditionalGeneration.from_pretrained(Usedmodel)

# use different length sentences to test batching
sentences = ["hello world", ""]

inputs = tokenizer([sentence for sentence in sentences], return_tensors="pt", padding=True)

output_sequences = model.generate(
    input_ids=inputs["input_ids"],
    attention_mask=inputs["attention_mask"],
    do_sample=False,  # disable sampling to test if batching affects output
)

print(tokenizer.batch_decode(output_sequences, skip_special_tokens=True))