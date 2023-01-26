# -*- coding: utf-8 -*-
"""「SimpleT5.ipynb」的副本

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1-Yt_AuwedrhqPiiL6sPlXUGB9kLQyjVF
"""


# --> Dataset
import pandas as pd
from sklearn.model_selection import train_test_split

from google.colab import drive
drive.mount('/content/drive')
folder = "/content/drive/MyDrive/Colab Notebooks/saved/generator/"
path = folder+"traindata.csv"

#done

df = pd.read_csv(path,sep="\|\|,\|\|")
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

from simplet5 import SimpleT5

model = SimpleT5()

model.from_pretrained(model_type="t5", model_name="t5-base")

model.train(train_df=train_df[:200],
            eval_df=test_df[:100], 
            source_max_token_len=128, 
            target_max_token_len=50, 
            batch_size=16, max_epochs=5, use_gpu=True)

# let's load the trained model for inferencing:
model.load_model("t5","/content/outputs/simplet5-epoch-4-train-loss-0.9325-val-loss-1.0881", use_gpu=True)

top_5_to_latex=""
""" 
9減[var2]分之2[var1][SEP][Pbeg]frac[Plbb]2[Pmin][Plsb][var2][Pplu][var1][Prsb][Prbb][Plbb][Plbb]9[Prbb][Pexp][Plbb][var3][Prbb][Prbb] [SEP][Pbeg]frac[Plbb]2[var1][Prbb][Plbb]9[Pmin][var2][Prbb] [SEP][Pbeg]frac[Plbb][var1][Prbb][Plbb][Plbb]9[Prbb][Pexp][Plbb]1[Prbb][Prbb] [SEP]0[Pplu][Plsb][var1][Pbeg]frac[Plbb][Pbeg]log[Psub][Plbb][var4][Prbb][Plbb]9[Prbb][Pexp][Plbb][var2][Prbb][Prbb][Plbb][var3][Prbb][Prsb] [SEP][Plbb][var2][Prbb][Pexp][Plbb][Plbb][Pbeg]sqrt[Plbb]9[Prbb][Prbb][Pexp][Plbb][var1][Prbb][Prbb] [SEP]||,||[Pbeg]frac[Plbb]2[var1][Prbb][Plbb]9[Pmin][var2][Prbb] ||,||247

"""

model.predict(top_5_to_latex)