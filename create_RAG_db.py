#!/home/dunbo/miniforge3/envs/RAG_python/bin/python

import argparse
from typing import List
from sentence_transformers import SentenceTransformer
import chromadb

from sentence_transformers import CrossEncoder

import ollama
from httpx import RequestError
import json
import time
import handle_file_name as hfn

def parser_args():
    parser = argparse.ArgumentParser(description='This is the program to create a chromadb file on a disk to save files chunk into it.')
    parser.add_argument('filename', help='input the markdown file')
    parser.add_argument('dbname', help='input name for output db')
    args = parser.parse_args()
    return args

def split_into_chunks_simple(doc_file: str) -> List[str]:
    '''
    The simplest way of chunking an md (converted by marker[pdf])
    '''
    with open(doc_file, 'r') as file:
        content = file.read()
    return [chunk for chunk in content.split("\n\n")]

def fuse_chunk_to_larger_content(chunks: List[str]) -> List[str]:
    ContentList = []
    for i, chunk in enumerate(chunks):
        if chunk.find("#") != -1:
            content = chunk
            for j in range(i + 1, len(chunks)):
                
                if chunks[j].find("#") == -1:
                    content = content + chunks[j]
                elif chunks[j].find("#") != -1:
                    content = content + chunks[j]
                else:
                    break
            ContentList.append( content )
    return ContentList

def filter_chunks_nonsence_by_rule(chunks: List[str]) -> List[str]:
        # 1. 使用规则过滤明显噪声
    noise_patterns = [
        r'Received.*?\d{4}.*?accepted.*?\d{4}',
        r'Journal of.*?\d{4}.*?\d+:\d+–\d+',
        r'conflicts of interest.*',
        r'©.*\d{4}',
        r'https?://\S+',  # URL
    ]

def embed_chunk(chunk: str, embedding_model) -> List[float]:
    embedding = embedding_model.encode(chunk)
    return embedding.tolist()


def save_embeddings(chunks: List[str], embeddings: List[List[float]], chromadb_collection) -> None:
    ids = [str(i) for i in range(len(chunks))] # the ids of chunks required in adb
    chromadb_collection.add(
        documents = chunks,
        embeddings = embeddings,
        ids = ids
    )

def create_or_add_db(filename, dbname):
    chunks = split_into_chunks_simple(filename)
    chunks = fuse_chunk_to_larger_content(chunks)
    # embedding_model = SentenceTransformer("shibing624/text2vec-base-chinese")
    # embedding_model = SentenceTransformer('BAAI/bge-large-zh-v1.5')
    embedding_model = SentenceTransformer('BAAI/bge-large-en-v1.5')
    embeddings = [embed_chunk(chunk, embedding_model) for chunk in chunks]
    chromadb_client = chromadb.PersistentClient(dbname)

    dirpath, filename, absfilepath_read, basename = hfn.handle_file_name(filename)
    chromadb_collection = chromadb_client.get_or_create_collection(name=filename) 
    save_embeddings(chunks=chunks, embeddings=embeddings, chromadb_collection = chromadb_collection)


def run():
    args = parser_args()
    filename = args.filename
    dbname = args.dbname
    create_or_add_db(filename, dbname)


if __name__ == '__main__':
	run()
