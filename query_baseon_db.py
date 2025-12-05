import os
import argparse
import handle_file_name as hfn
from typing import List

from sentence_transformers import SentenceTransformer
import chromadb

from sentence_transformers import CrossEncoder

import ollama
from httpx import RequestError
import json
import time
import re


def parser_args():
    parser = argparse.ArgumentParser(description='This is the program to ask question to AI, it will answer based on the database.')
    parser.add_argument('dbname', help='input the name of the database')
    parser.add_argument('collection_name', help='input the name of the collection, basically, it is XX.md')
    parser.add_argument('question', help='input the question within a single line')
    args = parser.parse_args()
    return args

def embed_chunk(chunk: str, embedding_model) -> List[float]:
    embedding = embedding_model.encode(chunk)
    return embedding.tolist()

def retrieve(query: str, embedding_model, top_k: int, chromadb_collection) -> List[str]:
    query_embedding = embed_chunk(query, embedding_model)
    results = chromadb_collection.query(
        query_embeddings = [query_embedding],
        n_results = top_k
    )
    return results['documents'][0]


def rerank(query: str, retrieved_chunks: List[str], top_k: int) -> List[str]:
    cross_encoder = CrossEncoder('cross-encoder/mmarco-mMiniLMv2-L12-H384-v1')
    pairs = [ (query, chunk) for chunk in retrieved_chunks ]
    scores = cross_encoder.predict(pairs)
    chunk_with_score_list = [(chunk, score) for chunk, score in zip(retrieved_chunks, scores)]
    chunk_with_score_list.sort(key=lambda pair: pair[1], reverse=True)
    return [chunk for chunk, _ in chunk_with_score_list][:top_k]


def QandA(query: str, chunks: List[str], role = 'user', host='', model = 'qwq:latest',  max_retries=3):
    client = ollama.Client(host = host)
    for attempt in range(max_retries):
        try:
            response = client.chat(model=model,
                                   messages=[
                                    {
                                        'role': role,
                                        'content':f"""
                                        请根据用户的问题和下列片段生成准确的回答。简化思考过程, 精简回答, 不需要完整句子

                                        用户问题: {query}

                                        相关片段: {";".join(chunks)}

                                        请给予以上内容用中文作答, 不要编造信息。

                                       """
                                    },
                                   ])
            return response.message.content
        except json.JSONDecodeError:
            print(f"JSON 解析失败，重试 {attempt + 1}/{max_retries}")
            time.sleep(5)  # 延迟后重试
        except RequestError as e:
            print(f"请求失败: {e}")
            time.sleep(5)
    return "请求失败，请稍后再试。"

def post_AI_processed_answer(answer:str) -> str:
    """
    提取AI回答中的最终响应部分，去除<think>思考过程</think>
    """
    # 使用正则表达式替换<think>...</think>及其内容为空
    cleaned_text = re.sub(r'<think>.*?</think>', '', answer, flags=re.DOTALL)
    
    # 去除可能的多余空白字符
    cleaned_text = cleaned_text.strip()
    
    return cleaned_text

def run():
    args = parser_args()
    dbname = args.dbname
    collection_name = args.collection_name
    query = args.question

    query_baseon_db_single(dbname, collection_name, query)


def query_baseon_db_single(dbname, collection_name, query, rerank_times = 1) -> str:
    embedding_model = SentenceTransformer('BAAI/bge-large-en-v1.5')
    chromadb_client = chromadb.PersistentClient(dbname)
    dirpath, filename, absfilepath_read, basename = hfn.handle_file_name(collection_name)
    chromadb_collection = chromadb_client.get_collection(name=filename) 

    retrieved_chunks = retrieve(query, embedding_model, 5, chromadb_collection = chromadb_collection)
    reranked_chunks = rerank(query, retrieved_chunks, 1)
    # for i, chunk in enumerate(reranked_chunks):
    #     print(f"[{i}] {chunk}\n")

    answer = QandA(query, reranked_chunks)
    answer = post_AI_processed_answer(answer)
    # print(answer)
    return answer



if __name__ == '__main__':
	run()
