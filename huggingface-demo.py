from transformers import pipeline, set_seed 
import torch
if torch.cuda.is_available():
    print(1);
generator = pipeline('text-generation', model='gpt2')
set_seed(42)
<<<<<<< HEAD
print(generator("i am going to", max_length=50, num_return_sequences=1)[0]['generated_text'])
=======
print(generator("What you have done is indeed too", max_length=50, num_return_sequences=1)[0]['generated_text'])
>>>>>>> e6ffbbcdbbb61d3879b80bbe769f95ab2dc54cbb
