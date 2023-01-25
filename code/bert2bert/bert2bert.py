# -*- coding: utf-8 -*-



import datasets
import transformers

import torch
torch.cuda.empty_cache()


from transformers import BertTokenizer
import pandas as pd
import datasets
from datasets import Dataset, DatasetDict

UsedModel = '/home/12518research/ck39Research/code/Pretrain/encoder'
tokenizer = BertTokenizer.from_pretrained(UsedModel)
tokenizer.sep_token = '[SEP]'
tokenizer.cls_token = '[CLS]'

DataFolder = "/home/12518research/ck39Research/code/bert2bert"
df_train = pd.read_csv(DataFolder+'traindata.csv',sep="\|\|,\|\|")
df_val = pd.read_csv(DataFolder+'valdata.csv',sep="\|\|,\|\|")

TrainData = Dataset.from_pandas(df_train)
ValData = Dataset.from_pandas(df_val)

train_data = TrainData
val_data = ValData

batch_size = 2
encoder_max_length = 512
decoder_max_length = 256

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

train_data = train_data.map(
    process_data_to_model_inputs, 
    batched=True, 
    batch_size=batch_size, 
    remove_columns=["retrieved", "target", "id"]
)
train_data.set_format(
    type="torch", columns=["input_ids", "attention_mask", "decoder_input_ids", "decoder_attention_mask", "labels"],
)

val_data = val_data.map(
    process_data_to_model_inputs, 
    batched=True, 
    batch_size=batch_size, 
    remove_columns=["retrieved", "target", "id"]
)
val_data.set_format(
    type="torch", columns=["input_ids", "attention_mask", "decoder_input_ids", "decoder_attention_mask", "labels"],
)

"""### **Warm-starting the Encoder-Decoder Model**"""

from transformers import EncoderDecoderModel

bert2bert = EncoderDecoderModel.from_encoder_decoder_pretrained(UsedModel,UsedModel)

#set special token
bert2bert.config.decoder_start_token_id = tokenizer.cls_token_id
bert2bert.config.pad_token_id = tokenizer.pad_token_id
bert2bert.config.vocab_size = bert2bert.config.decoder.vocab_size

# sensible parameters for beam search
bert2bert.config.max_length = 142
bert2bert.config.min_length = 56
bert2bert.config.no_repeat_ngram_size = 3
bert2bert.config.early_stopping = True
bert2bert.config.length_penalty = 2.0
bert2bert.config.num_beams = 4

"""### **Fine-Tuning Warm-Started Encoder-Decoder Models**

For the `EncoderDecoderModel` framework, we will use the `Seq2SeqTrainingArguments` and the `Seq2SeqTrainer`. Let's import them.
"""

from transformers import Seq2SeqTrainingArguments, Seq2SeqTrainer

"""Also, we need to define a function to correctly compute the ROUGE score during validation. ROUGE is a much better metric to track during training than only language modeling loss."""

# load rouge for validation
"""
rouge = datasets.load_metric("rouge")

def compute_metrics(pred):
    labels_ids = pred.label_ids
    pred_ids = pred.predictions

    # all unnecessary tokens are removed
    pred_str = tokenizer.batch_decode(pred_ids, skip_special_tokens=True)
    labels_ids[labels_ids == -100] = tokenizer.pad_token_id
    label_str = tokenizer.batch_decode(labels_ids, skip_special_tokens=True)

    rouge_output = rouge.compute(predictions=pred_str, references=label_str, rouge_types=["rouge2"])["rouge2"].mid

    return {
        "rouge2_precision": round(rouge_output.precision, 4),
        "rouge2_recall": round(rouge_output.recall, 4),
        "rouge2_fmeasure": round(rouge_output.fmeasure, 4),
    }
"""

"""Cool! Finally, we start training."""

import torch.optim as optim
from transformers import AdamW

# Define the optimizers for the encoder and decoder with separate learning rates
encoder_optimizer = optim.Adam(bert2bert.encoder.parameters(), lr=0.0001)
decoder_optimizer = optim.Adam(bert2bert.decoder.parameters(), lr=0.005)

# set training arguments - these params are not really tuned, feel free to change
training_args = Seq2SeqTrainingArguments(
    output_dir="./",
    evaluation_strategy="steps",
    per_device_train_batch_size=batch_size,
    per_device_eval_batch_size=batch_size,
    predict_with_generate=True,
    logging_steps=5,  # set to 1000 for full training
    save_steps=10,  # set to 500 for full training
    eval_steps=4,# set to 8000 for full training
    warmup_steps=10,  # set to 2000 for full trainingn #orig:1
    overwrite_output_dir=True,
    save_total_limit=3,
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
    #compute_metrics=compute_metrics,
    train_dataset=train_data,
    eval_dataset=val_data,
)

trainer.train()

"""### **Evaluation**

Awesome, we finished training our dummy model. Let's now evaluated the model on the test data. We make use of the dataset's handy `.map()` function to generate a summary of each sample of the test data.
"""

trainer.save_model('/content/drive/MyDrive/Colab Notebooks/saved/generator/model')
#trainer.evaluate()

import datasets
from transformers import BertTokenizer, EncoderDecoderModel

tokenizer = BertTokenizer.from_pretrained('/content/drive/MyDrive/Colab Notebooks/saved/generator/model')
tokenizer.sep_token = '[SEP]'
tokenizer.cls_token = '[CLS]'
model = EncoderDecoderModel.from_pretrained('/content/drive/MyDrive/Colab Notebooks/saved/generator/model')
model.to("cuda")

#test dataset
df_test = pd.read_csv(DataFolder+'testdata.csv',sep="\|\|,\|\|")
TestData = Dataset.from_pandas(df_test)
test_data = TestData
test_size = 10

batch_size = 4  # change to 64 for full evaluation

# map data correctly
def generate_summary(batch):
    # Tokenizer will automatically set [BOS] <text> [EOS]
    # cut off at BERT max length 512
    inputs = tokenizer(batch["retrieved"], padding="max_length", truncation=True, max_length=512, return_tensors="pt")
    input_ids = inputs.input_ids.to("cuda")
    attention_mask = inputs.attention_mask.to("cuda")

    outputs = model.generate(input_ids, attention_mask=attention_mask)

    # all special tokens including will be removed
    output_str = tokenizer.batch_decode(outputs, skip_special_tokens=True)

    batch["pred"] = output_str

    return batch

results = test_data.map(generate_summary, batched=True, batch_size=batch_size, remove_columns=["retrieved"])

pred_str = results["pred"]
label_str = results["target"]

for i in range(test_size):
    print("Gen:",end = '')
    pred = pred_str[i].replace(' ','')
    print(pred_str[i])
    print("Tar:",end = '')
    label = label_str[i].replace('[CLS]','')
    label = label.replace('[SEP]','')
    print(label)

"""
rouge_output = rouge.compute(predictions=pred_str, references=label_str, rouge_types=["rouge2"])["rouge2"].mid

print(rouge_output)
"""

"""The fully trained *BERT2BERT* model is uploaded to the 🤗model hub under [patrickvonplaten/bert2bert_cnn_daily_mail](https://huggingface.co/patrickvonplaten/bert2bert_cnn_daily_mail). 

The model achieves a ROUGE-2 score of **18.22**, which is even a little better than reported in the paper.

For some summarization examples, the reader is advised to use the online inference API of the model, [here](https://huggingface.co/patrickvonplaten/bert2bert_cnn_daily_mail).
"""