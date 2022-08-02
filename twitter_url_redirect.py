# Twitter评论中的URL大多数会被Twitter转化为短链接的形式
# 通过requests获取meta标签中的重定向URL

import pandas as pd
import os
import re
import sys
import requests
from bs4 import BeautifulSoup
from lxml import etree
from numpy import nan

headers = {
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36"
}
proxies = {
    'http': 'http://127.0.0.1:1080',
    'https': 'http://127.0.0.1:1080'
}


def find_all_files(base):
    for root, ds, fs in os.walk(base):
        for f in fs:
            if f.endswith(".csv"):
                fullname = os.path.join(root, f)
                yield fullname


def get_redirect_url(url):
    res = requests.get(url, headers=headers, timeout=8, proxies=proxies)
    html = etree.HTML(res.text)
    result = html.xpath('//meta[@http-equiv="refresh" and @content]/@content')
    redirect_url = re.search(r'[a-zA-z]+://[^\s]*', result[0])
    return redirect_url.group()


def main():
    csv_file_path = "./URL_unique_split/" + sys.argv[1] + ".csv"
    # save_file_path = sys.argv[1].split('/')[:-1] + "/" + sys.argv[1].split('/')[-1].split('.')[0] + "_redirect.csv"
    # save_file_path = "./URL_unique_split/" + sys.argv[1] + "_redirect.csv"
    url_df = pd.read_csv(csv_file_path, encoding='utf-8',
                         engine='python', na_values='null')
    # url_df = url_df.reindex(columns=url_df.columns.tolist() + ["redirect_url"])
    urls = url_df.iloc[:, 0].values
    for index, url in enumerate(urls, 0):
        try:
            # print(url_df.iloc[index, 1])
            if url_df.iloc[index, 1] != url_df.iloc[index, 1]:  # nan
                print("No.{0} Analysing URL: {1}".format(index, url))
                redirect_url = get_redirect_url(url)
                if redirect_url:
                    print("Get Redirect URL: ", redirect_url)
                    url_df.iloc[index, 1] = redirect_url
        except Exception as err:
            print("Error: ", err)
    url_df.to_csv(csv_file_path, index=False)


if __name__ == '__main__':
    main()
