import pandas as pd
import os
import re
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
    csv_file_path = './redirect_urls.csv'
    url_df = pd.read_csv(csv_file_path, encoding='utf-8', engine='python', na_values='null')
    # url_df = url_df.reindex(columns=url_df.columns.tolist() + ["redirect_url"])
    urls = url_df.iloc[0:5000, 0].values  # 并行
    # urls = url_df.iloc[5001:10000, 0].values  # 并行
    try:
        for index, url in enumerate(urls, 0):
            # print(url_df.iloc[index, 1])
            if url_df.iloc[index, 1] != url_df.iloc[index, 1]:  # nan
                print("No.{0} Analysing URL: {1}".format(index, url))
                redirect_url = get_redirect_url(url)
                if redirect_url:
                    print("Get Redirect URL: ", redirect_url)
                    url_df.iloc[index, 1] = redirect_url
        url_df.to_csv('./redirect_urls.csv', index=False)
    except Exception as err:
        print("Error: ", err)
    url_df.to_csv('./redirect_urls.csv', index=False)


if __name__ == '__main__':
    main()
