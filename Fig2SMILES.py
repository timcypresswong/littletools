#!/home/dunbo/miniforge3/envs/DECIMER/bin/python

import argparse
import contextlib
import io
import sys
import logging

logging.basicConfig(level=logging.CRITICAL)


def parser_args():
    parser = argparse.ArgumentParser(description='This is to decode figure to a smiles string. Please use it under WSL system')
    parser.add_argument('filename', help='input the path of a figure')
    args = parser.parse_args()
    return args


@contextlib.contextmanager
def suppress_output():
    # 创建 StringIO 对象来捕获输出
    stdout = io.StringIO()
    stderr = io.StringIO()
    
    # 保存当前的标准输出和错误输出
    old_stdout = sys.stdout
    old_stderr = sys.stderr
    
    try:
        # 重定向标准输出和错误输出
        sys.stdout = stdout
        sys.stderr = stderr
        yield
    finally:
        # 恢复标准输出和错误输出
        sys.stdout = old_stdout
        sys.stderr = old_stderr


with suppress_output():
    from DECIMER import predict_SMILES

def run():
    args = parser_args()
    file_path = args.filename
    Fig2SMILES(file_path)

def Fig2SMILES(file_path):
	SMILES = predict_SMILES(file_path)
	print(f"File path: {file_path} 🎉 Decoded SMILES: {SMILES}")
	

if __name__ == '__main__':
	run()