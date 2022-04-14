from transformers import pipeline, set_seed 
import torch
if torch.cuda.is_available():
    print(1);
generator = pipeline('text-generation', model='gpt2')
set_seed(42)
print(generator("How is the weather tomorrow?", max_length=50, num_return_sequences=1)[0]['generated_text'])
