
from transformers import BertTokenizer, LineByLineTextDataset,BertConfig, BertForMaskedLM, DataCollatorForLanguageModeling
import tokenizers

tokenizer = BertTokenizer.from_pretrained("amine/bert-base-5lang-cased")
'''
special token
'''
#latex command
tokenizer.add_tokens(["frac","addcontentsline ", "addtocontents ", "addtocounter ", "address ", "addtolength ", "addvspace ", "alph ", "appendix ", "arabic ", "author ", "backslash ", "baselineskip ", "baselinestretch ", "bf ", "bibitem ", "bigskip ", "boldmath ", "cal ", "caption ", "cdots ", "centering ", "circle ", "cite ", "cleardoublepage ", "clearpage ", "cline ", "closing ", "cos","dashbox ", "date ", "ddots ", "dotfill ", "em ", "fbox ", "flushbottom ", "fnsymbol ", "footnote ", "footnotemark ", "footnotesize ", "footnotetext ", "frac ", "frame ", "framebox ", "frenchspacing ", "hfill ", "hline ", "hrulefill ", "hspace ", "huge ", "hyphenation ", "include ", "includeonly ", "indent ", "input ", "it ", "item ", "kill ", "label ", "large ", "LARGE (all caps) ", "ldots ", "left ", "lefteqn ", "line ", "linebreak ", "linethickness ", "linewidth ", "location ","log", "makebox ", "maketitle ", "mathcal ", "mathop ", "mbox ", "medskip ", "multicolumn ", "multiput ", "newcommand ", "newcounter ", "newenvironment ", "newfont ", "newlength ", "newline ", "newpage ", "newsavebox ", "newtheorem ", "nocite ", "noindent ", "nolinebreak ", "nopagebreak ", "not ", "onecolumn ", "opening ", "oval ", "overbrace ", "overline ", "pagebreak ", "pagenumbering ", "pageref ", "pagestyle ", "par ", "parbox ", "parindent ", "parskip ", "protect ", "put ", "raggedbottom ", "raggedleft ", "raggedright ", "raisebox ", "ref ", "renewcommand ", "right ", "rm ", "roman ", "rule ", "savebox ", "sbox ", "sc ", "scriptsize ", "setcounter ", "setlength ", "settowidth ", "sf ", "shortstack ", "signature ","sin", "sl ", "small ", "smallskip ", "sqrt ", "stackrel ", "tableofcontents ","tan", "telephone ", "textwidth ", "textheight ", "thanks ", "thispagestyle ", "tiny ", "title ", "today ", "tt ", "twocolumn ", "typeout ", "typein ", "underbrace ", "underline ", "unitlength ", "usebox ", "usecounter ", "value ", "vdots ", "vector ", "verb ", "vfill ", "vline ", "vphantom ", "vspace"])
# var list
for i in range(1,51):
    tokenizer.add_tokens(["[var{}]".format(i)])
# puncuation
tokenizer.add_tokens(["[","[Plmb]","]","[Prmb]"," ","[Pspa]","^","[Pexp]","+","[Pplu]","-","[Pmin]","(","[Plsb]",")","[Prsb]","/","[Pdiv]",",","[Plbb]",",","[Prbb]","\\","[Pbeg]","=","[Peql]","<","[Ples]",">","[Pbgr]",",","[Pcol]","!","[Pexc]","_","[Psub]",",","[Pcom]"])
sentence = r'\frac{2}{3}'

encoded_input = tokenizer.tokenize(sentence)
print(encoded_input)

dataset = LineByLineTextDataset(
    tokenizer = tokenizer,
    file_path = '/home/12518research/ck39Research/data/Data/generator/processed.txt',
    block_size = 256 # maximum sequence length
)

testdata = LineByLineTextDataset(
    tokenizer = tokenizer,
    file_path = '/home/12518research/ck39Research/data/Data/generator/eval.txt',
    block_size = 256 # maximum sequence length
)


config = BertConfig(
    vocab_size=50000,
    hidden_size=768, 
    num_hidden_layers=6, 
    num_attention_heads=12,
    max_position_embeddings=512
)
 
model = BertForMaskedLM(config)

data_collator = DataCollatorForLanguageModeling(
    tokenizer=tokenizer, mlm=True, mlm_probability=0.15
)


from transformers import Trainer, TrainingArguments

training_args = TrainingArguments(
    output_dir='/home/12518research/ck39Research/code/Pretrain/model',
    overwrite_output_dir=True,
    num_train_epochs=2,
    per_device_train_batch_size=32,
    save_steps=10_00,
    save_total_limit=2,
)

trainer = Trainer(
    model=model,
    args=training_args,
    data_collator=data_collator,
    train_dataset=dataset,
    eval_dataset=testdata,
    #prediction_loss_only=True,
)
trainer.train()
trainer.save_model('/home/12518research/ck39Research/code/Pretrain/model/')
tokenizer.save_pretrained('/home/12518research/ck39Research/code/Pretrain/model/')
trainer.evaluate()
tokenizer.save_pretrained('/home/12518research/ck39Research/code/Pretrain/model/')


