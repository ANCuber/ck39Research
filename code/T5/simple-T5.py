# -*- coding: utf-8 -*-


# --> Dataset
import pandas as pd
from sklearn.model_selection import train_test_split

folder = "/home/12518research/ck39Research/data/Data/generator/"
path = folder+"train_data.csv"

#done
print("Preparing data...")

df = pd.read_csv(path,sep=",")
df.head()

# simpleT5 expects dataframe to have 2 columns: "source_text" and "target_text"
df = df.rename(columns={"target":"target_text", "retrieved":"source_text"})
print(df)
df = df[['source_text', 'target_text']]

#add prefix
df['source_text' ] = "" + df['source_text']
#print(df)

train_df, test_df = train_test_split(df, test_size=0.2)
train_df.shape, test_df.shape

print("Preparing model...")

from simplet5 import SimpleT5

model = SimpleT5()

model.from_pretrained(model_type="t5", model_name="t5-base")

model.train(train_df=train_df[:200],
            eval_df=test_df[:100], 
            source_max_token_len=128, 
            target_max_token_len=50, 
            batch_size=16,
            max_epochs=5, 
            use_gpu=True
            )

# let's load the trained model for inferencing:
model_path = '/home/12518research/ck39Research/outputs/simplet5-epoch-4-train-loss-0.4341-val-loss-0.4499'
model.load_model("t5",model_path, use_gpu=True)

top_5_to_latex=""
""" 
[var2]分之[var1][CLS][Plbb][var1][Prbb][Pexp][Plbb][var2][Prbb][Peql][Pbeg]frac[Plbb][var2][Prbb][Plbb][var1][Prbb][SEP][var1]分之[var2]等於[var1]分之[var2][CLS][Plbb][var1][Prbb][Pexp][Plbb][var2][Prbb][Peql][Pbeg]frac[Plbb][var2][Prbb][Plbb][var1][Prbb][SEP][var1]分之[var2]等於[var1]分之[var2][CLS][Plbb][var1][Prbb][Pexp][Plbb][var2][Prbb][Peql][Pbeg]frac[Plbb][var2][Prbb][Plbb][var1][Prbb][SEP][var1]分之[var2]等於[var1]分之[var2][CLS][Pbeg]frac[Plbb][var2][Prbb][Plbb][var1][Prbb][Peql][Pbeg]frac[Plbb][Pbeg]frac[Plbb]5[var3][Prbb][Plbb][var1][Prbb][Prbb][Plbb][var2][Prbb][SEP][var1]分之[var2]等於[var2]分之[Pspa][var1]分之5[var3][CLS][Pbeg]frac[Plbb][Pbeg]frac[Plbb]5[var3][Prbb][Plbb][var2][Prbb][Prbb][Plbb][var1][Prbb][Peql][var2][Pmin][Pbeg]frac[Plbb]6[Prbb][Plbb][var1][Prbb][SEP][var1]分之[var2]分之5[var3]等於[var2]減[var1]分之6[SEP],[var2]分之[var1] ,3

"""

model.predict(top_5_to_latex)