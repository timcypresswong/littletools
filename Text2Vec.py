#!/home/dunbo/miniforge3/envs/RAG_python/bin/python

from typing import List
from sentence_transformers import SentenceTransformer
import chromadb
import numpy as np

from sentence_transformers import CrossEncoder

import argparse

# from marker.converters.pdf import PdfConverter
# from marker.models import create_model_dict
# from marker.output import text_from_rendered

# file_path = "testPDF/Pharyngitis Approach to diagnosis and treatment.pdf"

def parser_args():
    parser = argparse.ArgumentParser(description='This is the program to encode a sentence of one-line file information into a vector.')
    parser.add_argument('filename', help='input oneline file')
    args = parser.parse_args()
    return args


def run():
    args = parser_args()
    filename = args.filename
    Str_to_Vec_standalone(filename)

def Str_to_Vec_standalone(filename):
    sep = ','
    with open(filename, 'r') as f:
        content1 = f.readline().strip().split(sep)
    vector = Str_to_Vec_api(content1)
    vector = np.array(vector)
    print(vector)
    print(vector.shape)

def Str_to_Vec_api(chunk: str) -> list:
    embedding_model = SentenceTransformer("shibing624/text2vec-base-chinese")
    vector = embed_chunk(chunk, embedding_model)
    return vector


def split_into_chunks_simple(doc_file: str) -> List[str]:
    '''
    The simplest way of chunking an md (converted by marker[pdf])
    '''
    with open(doc_file, 'r') as file:
        content = file.read()
    return [chunk for chunk in content.split("\n\n")]




def embed_chunk(chunk: str, embedding_model) -> List[float]:
    embedding = embedding_model.encode(chunk)
    return embedding.tolist()

'''
def save_embeddings(chunks: List[str], embeddings: List[List[float]]) -> None:
    ids = [str(i) for i in range(len(chunks))] # the ids of chunks required in adb
    chromadb_collection.add(
        documents = chunks,
        embeddings = embeddings,
        ids = ids
    )


def retrieve(query: str, embedding_model, top_k: int) -> List[str]:
    query_embedding = embed_chunk(query, embedding_model)
    results = chromadb_collection.query(
        query_embeddings = [query_embedding],
        n_results = top_k
    )
    return results['documents'][0]
'''

'''
# chunks = split_into_chunks_simple(file_path)

chunks = ["Hi, this way", "What is your name"]

for i, chunk in enumerate(chunks):
    print(f"[{i}] {chunk}\n")


# embedding_model = SentenceTransformer("shibing624/text2vec-base-chinese")
# embedding_model = SentenceTransformer('BAAI/bge-large-zh-v1.5')
embedding_model = SentenceTransformer('BAAI/bge-large-en-v1.5')

# test_embedding = embed_chunk("测试内容", embedding_model=embedding_model)
# print(len(test_embedding))
# print(test_embedding)


embeddings = [embed_chunk(chunk, embedding_model) for chunk in chunks]
print(len(embeddings))
print(embeddings)

chromadb_client = chromadb.EphemeralClient() # client in RAM
# chromadb_client = chromadb.PersistentClient("./chroma.db") # client on Disk
chromadb_collection = chromadb_client.get_or_create_collection(name='default')

save_embeddings(chunks=chunks, embeddings=embeddings)


query = "What is the topic of this article?"
retrieved_chunks = retrieve(query, embedding_model, 5)
for i, chunk in enumerate(retrieved_chunks):
    print(f"[{i}] {chunk}\n")
'''


if __name__ == '__main__':
	run()
