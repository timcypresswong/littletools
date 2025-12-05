import requests
from bs4 import BeautifulSoup
import urllib.parse

import argparse



def parser_args():
    parser = argparse.ArgumentParser(description='If you input a url in a browser, it shows you a pdf. Then input the same url here, this tool automatically download the pdf for you.')
    parser.add_argument('url', help='input a url')
    args = parser.parse_args()
    return args


def run():
    args = parser_args()
    url = args.url
    download_paper_standalone(url)

# pdf_url_input = "https://meetings-api.hematology.org/api/abstract/vmpreview/296134"


def download_paper_standalone(pdf_url_input):
    headers = {
          'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    }


    max_tries = 5
    # 下载PDF
    fail_file = open("failed_to_download.txt", 'a')
    success_flag = True
    for i in range(max_tries):
        try:
            print(pdf_url_input)
            response = requests.get(pdf_url_input)
            response.raise_for_status()
            pdf_response = requests.get(pdf_url_input, headers=headers)
            pdf_response.raise_for_status()
            break
        except Exception as e:
            print("attempt trial", i + 1, "failed")
            if i >= max_tries - 1:
                print("failed to download:", pdf_url_input, file = fail_file)
                success_flag = False

          


    # 保存PDF文件
    if success_flag:
        filename = pdf_url_input.replace( "https://", "" )
        filename = filename.replace( "/", "_" )
        filename = filename.replace( " ", "_" )
        
        filename = filename + '_downloaded.pdf'
        # filename = pdf_url_input.split('/')[-1] 
        # if filename is not None:
        #     filename = filename + '_downloaded.pdf'
        # else:
        #     filename = pdf_url_input.split('/')[-2] 
        with open(filename, 'wb') as f:
            f.write(response.content)
        
        print(f"PDF下载完成: {filename}")
        return filename
    else:
        print(f"PDF下载失败: {pdf_url_input}")
        return None


if __name__ == '__main__':
	run()
