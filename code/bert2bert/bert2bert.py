# -*- coding: utf-8 -*-

#-m !pip3 install datasets
#-m !pip3 install transformers

import os
os.environ['CUDA_VISIBLE_DEVICES']='2, 3'

import transformers

import torch

from transformers import BertTokenizer, BertConfig, BertModel
import pandas as pd
import datasets
from datasets import Dataset, DatasetDict

#setting gpu
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
print('Using device:', device)

print("Loading tokenizer and models...")

UsedTokenizer = '/home/12518research/ck39Research/model/bert-p2000&chi'
UsedEncoder = '/home/12518research/ck39Research/model/bert-p2000&chi'

UsedDecoder = '/home/12518research/ck39Research/model/bert-p20000'

output = '/home/12518research/ck39Research/model/bert2bert_2'

tokenizer = BertTokenizer.from_pretrained(UsedTokenizer)
tokenizer.sep_token = '[SEP]'
tokenizer.cls_token = '[CLS]'
tokenizer.bos_token = tokenizer.cls_token
tokenizer.eos_token = tokenizer.sep_token


print("Done!")
print("Processing Datasets...")

DataFolder = "/home/12518research/ck39Research/data/Data/generator/"
df_train = pd.read_csv(DataFolder+'train_data.csv',sep=",")
df_val = pd.read_csv(DataFolder+'val_data.csv',sep=",")

TrainData = Dataset.from_pandas(df_train)
ValData = Dataset.from_pandas(df_val)

train_data = TrainData
val_data = ValData

batch_size = 4
encoder_max_length = 512
decoder_max_length = 128

def process_data_to_model_inputs(batch):
    # tokenize the inputs and labels
    inputs = tokenizer(batch["retrieved"], padding="max_length", truncation=True, max_length=encoder_max_length)
    outputs = tokenizer(batch["target"], padding="max_length", truncation=True, max_length=decoder_max_length)
    

    batch["input_ids"] = inputs.input_ids
    batch["attention_mask"] = inputs.attention_mask
    batch["decoder_input_ids"] = outputs.input_ids
    batch["decoder_attention_mask"] = outputs.attention_mask
    batch["labels"] = outputs.input_ids.copy()

    # because BERT automatically shifts the labels, the labels correspond exactly to `decoder_input_ids`. 
    # We have to make sure that the PAD token is ignored
    batch["labels"] = [[-100 if token == tokenizer.pad_token_id else token for token in labels] for labels in batch["labels"]]

    return batch

#train_data = train_data.select(range(8000))#delete for full training

train_data = train_data.map(
    process_data_to_model_inputs, 
    batched=True, 
    batch_size=batch_size, 
    remove_columns=["retrieved", "target", "id"]
)
train_data.set_format(
    type="torch", columns=["input_ids", "attention_mask", "decoder_input_ids", "decoder_attention_mask", "labels"],
)

#val_data = val_data.select(range(1000))#delete for full training

val_data = val_data.map(
    process_data_to_model_inputs, 
    batched=True, 
    batch_size=batch_size, 
    remove_columns=["retrieved", "target", "id"]
)
val_data.set_format(
    type="torch", columns=["input_ids", "attention_mask", "decoder_input_ids", "decoder_attention_mask", "labels"],
)

print("Data processed")

"""### **Warm-starting the Encoder-Decoder Model**"""



print("Setting EncoderDecoderModel...")

from transformers import EncoderDecoderModel, EncoderDecoderConfig

import gc

#config = EncoderDecoderConfig.from_encoder_decoder_configs(EnConf,DeConf)

gc.collect()
torch.cuda.empty_cache()
bert2bert = EncoderDecoderModel.from_encoder_decoder_pretrained(UsedEncoder,UsedDecoder)
bert2bert.to('cuda:0')

print("Preparing for training")
#set special token
bert2bert.config.hidden_dropout_prob = 0.3
bert2bert.config.attention_probs_Dropout_prob = 0.3
bert2bert.config.classifier_dropout = 0.3
bert2bert.config.decoder_start_token_id = tokenizer.bos_token_id
bert2bert.config.eos_token_id = tokenizer.eos_token_id
bert2bert.config.pad_token_id = tokenizer.pad_token_id
bert2bert.config.vocab_size = bert2bert.config.decoder.vocab_size

# sensible parameters for beam search
bert2bert.config.max_length = 40
bert2bert.config.min_length = 5
bert2bert.config.no_repeat_ngram_size = 3
bert2bert.config.early_stopping = True
bert2bert.config.length_penalty = 2.0
bert2bert.config.num_beams = 4

"""### **Fine-Tuning Warm-Started Encoder-Decoder Models**"""

from transformers import Seq2SeqTrainingArguments, Seq2SeqTrainer

"""Training"""

# Define the optimizers for the encoder and decoder with separate learning rates
import torch.optim as optim
from transformers import AdamW


# set training arguments - these params are not really tuned, feel free to change
training_args = Seq2SeqTrainingArguments(
    output_dir=output,
    num_train_epochs=3.0,
    evaluation_strategy="steps",
    per_device_train_batch_size=batch_size,
    per_device_eval_batch_size=batch_size,
    predict_with_generate=True,
    logging_steps=60,# set to 1000 for full training
    save_steps=800,  # set to 500 for full training
    eval_steps=500,# set to 8000 for full training
    warmup_steps=120,  # set to 2000 for full trainingn #orig:1
    overwrite_output_dir=True,
    save_total_limit=100,
    learning_rate=1e-5,
    weight_decay =2e-3,
    fp16=True, 
)

from transformers import DataCollatorForSeq2Seq

seq2seq_data_collator = DataCollatorForSeq2Seq(tokenizer, model=bert2bert)


# instantiate trainer
trainer = Seq2SeqTrainer(
    model=bert2bert,
    tokenizer=tokenizer,
    args=training_args,
    data_collator=seq2seq_data_collator,
    train_dataset=train_data,
    eval_dataset=val_data,
)

print("Start training...")
trainer.train()

"""### **Evaluation**"""

trainer.save_model(output)
tokenizer.save_pretrained(output)
#trainer.evaluate()