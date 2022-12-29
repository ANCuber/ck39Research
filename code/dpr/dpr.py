# -*- coding: UTF-8 -*-
from haystack.nodes import DensePassageRetriever
from haystack.utils import fetch_archive_from_http
from haystack.document_stores import InMemoryDocumentStore
import json
data_dir = "/content/drive/MyDrive/Colab Notebooks/"
train_filename = "data_dpr.json"
doc_filename = 'doc_store.json'
#dev_filename = "dev/biencoder-nq-dev.json"

query_model = "/content/drive/MyDrive/Colab Notebooks/Latex_pretrained/"
passage_model = query_model
document_store = InMemoryDocumentStore()

save_dir = "/content/drive/MyDrive/Colab Notebooks/saved/dpr"
f = open(data_dir+doc_filename)
doc = json.load(f)
print(type(doc))
print(doc)
document_store.write_documents(documents= doc)

retriever = DensePassageRetriever(
    document_store=document_store,
    query_embedding_model=query_model,
    passage_embedding_model=passage_model,
    max_seq_len_query=64,
    max_seq_len_passage=256,
)

retriever.train(
    data_dir = data_dir,
    train_filename=train_filename,
    n_epochs=5,
    batch_size=16,
    grad_acc_steps=8,
    save_dir=save_dir,
    evaluate_every=3000,
    embed_title=True,
    num_positives=1,
    num_hard_negatives=0
)


document_store.update_embeddings(retriever)
retriever.retrieve('[var1]分之[var2]')
reloaded_retriever = DensePassageRetriever.load(load_dir=save_dir,document_store=document_store)
result = reloaded_retriever.retrieve("根號[var1]",top_k=5)
for i in result:
  print(i.content)