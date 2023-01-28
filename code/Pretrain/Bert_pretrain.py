print("import stuff")
from transformers import AutoTokenizer, LineByLineTextDataset,BertConfig, AutoModelForMaskedLM, DataCollatorForLanguageModeling,BertModel
import tokenizers 
import os
UsedModel = "/home/12518research/ck39Research/model/bert-p2000&chi/checkpoint-5000"
tokenizer = AutoTokenizer.from_pretrained("amine/bert-base-5lang-cased")
'''
special token
'''
print('begin')

os.environ["TOKENIZERS_PARALLELISM"] = "false"
#latex command
tokenizer.add_tokens(["frac","addcontentsline ", "addtocontents ", "addtocounter ", "address ", "addtolength ", "addvspace ", "alph ", "appendix ", "arabic ", "author ", "backslash ", "baselineskip ", "baselinestretch ", "bf ", "bibitem ", "bigskip ", "boldmath ", "cal ", "caption ", "cdots ", "centering ", "circle ", "cite ", "cleardoublepage ", "clearpage ", "cline ", "closing ", "cos","dashbox ", "date ", "ddots ", "dotfill ", "em ", "fbox ", "flushbottom ", "fnsymbol ", "footnote ", "footnotemark ", "footnotesize ", "footnotetext ", "frac ", "frame ", "framebox ", "frenchspacing ", "hfill ", "hline ", "hrulefill ", "hspace ", "huge ", "hyphenation ", "include ", "includeonly ", "indent ", "input ", "it ", "item ", "kill ", "label ", "large ", "LARGE (all caps) ", "ldots ", "left ", "lefteqn ", "line ", "linebreak ", "linethickness ", "linewidth ", "location ","log", "makebox ", "maketitle ", "mathcal ", "mathop ", "mbox ", "medskip ", "multicolumn ", "multiput ", "newcommand ", "newcounter ", "newenvironment ", "newfont ", "newlength ", "newline ", "newpage ", "newsavebox ", "newtheorem ", "nocite ", "noindent ", "nolinebreak ", "nopagebreak ", "not ", "onecolumn ", "opening ", "oval ", "overbrace ", "overline ", "pagebreak ", "pagenumbering ", "pageref ", "pagestyle ", "par ", "parbox ", "parindent ", "parskip ", "protect ", "put ", "raggedbottom ", "raggedleft ", "raggedright ", "raisebox ", "ref ", "renewcommand ", "right ", "rm ", "roman ", "rule ", "savebox ", "sbox ", "sc ", "scriptsize ", "setcounter ", "setlength ", "settowidth ", "sf ", "shortstack ", "signature ","sin", "sl ", "small ", "smallskip ", "sqrt ", "stackrel ", "tableofcontents ","tan", "telephone ", "textwidth ", "textheight ", "thanks ", "thispagestyle ", "tiny ", "title ", "today ", "tt ", "twocolumn ", "typeout ", "typein ", "underbrace ", "underline ", "unitlength ", "usebox ", "usecounter ", "value ", "vdots ", "vector ", "verb ", "vfill ", "vline ", "vphantom ", "vspace"])
# var list
for i in range(1,51):
    tokenizer.add_tokens(["[var{}]".format(i)])
# puncuation
tokenizer.add_tokens(["[Plmb]","[Prmb]","[Pspa]","[Pexp]","[Pplu]","[Pmin]","[Plsb]","[Prsb]","[Pdiv]","[Plbb]","[Prbb]","[Pbeg]","[Peql]","[Ples]","[Pbgr]","[Pcol]","[Pexc]","[Psub]","[Pcom]"])
output = "/home/12518research/ck39Research/model/bert-p2000&chi"
tokenizer.save_pretrained(output)
print('dataset start')
dataset = LineByLineTextDataset(
    tokenizer = tokenizer,
    file_path = r'/home/12518research/ck39Research/data/Data/pretrain/math&chinese.txt',
    block_size = 256 # maximum sequence length
)

print('dataset finish,model get start')

 
model = AutoModelForMaskedLM.from_pretrained(UsedModel)
print('model get end,resize token')
model.resize_token_embeddings(len(tokenizer))
print('resized token,start data_collator')
data_collator = DataCollatorForLanguageModeling(
    tokenizer=tokenizer, mlm=True, mlm_probability=0.15
)
print('data_collator finish')


from transformers import Trainer, TrainingArguments
print('training arg')

training_args = TrainingArguments(
    output_dir=output,
    overwrite_output_dir=True,
    logging_steps=20,
    learning_rate=5e-05,
    num_train_epochs= 1,
    per_device_train_batch_size=8,

)
print('traning arg done, trainer arg')
trainer = Trainer(
    model=model,
    args=training_args,
    data_collator=data_collator,
    train_dataset=dataset,
    #prediction_loss_only=True,
)
print('trainer arg done, start train')
trainer.train()
print('train done')
trainer.save_model(output)
tokenizer.save_pretrained(output)

