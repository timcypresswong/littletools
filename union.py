#!/home/dunbo/miniforge3/envs/RAG_python/bin/python

import argparse


def parser_args():
    parser = argparse.ArgumentParser(description='This is the program to union one-line file information.')
    parser.add_argument('filename1', help='input oneline file')
    parser.add_argument('filename2', help='input oneline file')
    args = parser.parse_args()
    return args


def run():
    args = parser_args()
    filename1 = args.filename1
    filename2 = args.filename2
    unioncontent(filename1, filename2)

def unioncontent(filename1, filename2):
    sep = ','
    with open(filename1, 'r') as f:
        content1 = f.readline().strip().split(sep)

    with open(filename2, 'r') as f:
        content2 = f.readline().strip().split(sep)

    content1 = set(content1)
    content2 = set(content2)

    union = set.union(content1, content2)
    union = list(union)
    print(len(union))
    print(','.join(union))


if __name__ == '__main__':
	run()
