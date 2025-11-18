#!/home/dunbo/miniforge3/envs/RAG_python/bin/python

import argparse


def parser_args():
    parser = argparse.ArgumentParser(description='This is the program to count the frequency of a noun occuring in a one-line file information.')
    parser.add_argument('filename', help='input oneline file')
    args = parser.parse_args()
    return args


def run():
    args = parser_args()
    filename = args.filename
    list_to_dict_standalone(filename)

def list_to_dict_standalone(filename):
    sep = ','
    with open(filename, 'r') as f:
        content1 = f.readline().strip().split(sep)


    content_count = list_to_dict_api(content1)
    print(content_count)

def list_to_dict_api(repeating_list: list) -> dict:
    counting_dict = {}
    for element in repeating_list:
        try:
            counting_dict[element] += 1
        except KeyError:
            counting_dict[element] = 1

    return counting_dict

def rank_dict(orignal_dict: dict) -> dict:
    sorted_dict_asc = dict(sorted(orignal_dict.items(), key=lambda x: x[1]))
    return sorted_dict_asc

if __name__ == '__main__':
	run()
