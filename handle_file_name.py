import os
import argparse
def parser_args():
    parser = argparse.ArgumentParser(description='This is the program to handle the file name.')
    parser.add_argument('file_path', help='input the markdown file')
    args = parser.parse_args()
    return args


def run():
    args = parser_args()
    file_path = args.file_path
    handle_file_name(file_path)

def handle_file_name(file_path):
    dirpath = os.path.abspath(os.path.dirname(file_path))
    filename = os.path.basename(file_path)
    absfilepath_read = dirpath + os.path.sep + filename
    basename = filename.split('.')[0]

    return dirpath, filename, absfilepath_read, basename

if __name__ == '__main__':
	run()
