import torch
from transformers import BertForQuestionAnswering
from transformers import BertTokenizer

UsedModel = '/home/12528research/ck39Research/code/Pretrain/model'

#Model
model = BertForQuestionAnswering.from_pretrained(UsedModel)

#Tokenizer
tokenizer = BertTokenizer.from_pretrained(UsedModel)

question = ''' '''

retrieved_commands = ''' '''

encoding = tokenizer.encode_plus(text=question,text_pair=retrieved_commands)

inputs = encoding['input_ids']  #Token embeddings
sentence_embedding = encoding['token_type_ids']  #Segment embeddings
tokens = tokenizer.convert_ids_to_tokens(inputs) #input tokens

start_scores, end_scores = model(input_ids=torch.tensor([inputs]), token_type_ids=torch.tensor([sentence_embedding]))


start_index = torch.argmax(start_scores)

end_index = torch.argmax(end_scores)

answer = ' '.join(tokens[start_index:end_index+1])

corrected_answer = ''

for word in answer.split():
    
    #If it's a subword token
    if word[0:2] == '##':
        corrected_answer += word[2:]
    else:
        corrected_answer += ' ' + word

print(corrected_answer)

