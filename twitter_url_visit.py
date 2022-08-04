# 访问之前从短链接中获得的重定向URL
# 通过LR模型判断是否为final page

import pandas as pd
import numpy as np
import joblib
import os
import re
import time
import lxml
from bs4 import BeautifulSoup
import requests
import comm.logger as logger
from comm.model import Sample
from sklearn.preprocessing import MinMaxScaler, StandardScaler
from sklearn.linear_model import LogisticRegression

headers = {
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36"
}
proxies = {
    'http': 'http://127.0.0.1:1080',
    'https': 'http://127.0.0.1:1080'
}
_logger = logger.Logger('info')
model_path = './lr.pkl'
lr_model = joblib.load(model_path)
white_list = ['twitter.com', 'google.com', 'facebook.com',
              'gmail.com', 'instagram.com', 'youtube.com', 'youtu.be']
MAX_DEPTH = 3


def predict_url(html, landing_page):
    print("Extracting features from landing page...")
    sample = Sample()
    bs = BeautifulSoup(html, "html.parser")
    current_domain = landing_page.split('/')[2]
    a_tags = bs.find_all("a")
    sample.a_count = len(a_tags)
    if sample.a_count > 0:
        a_http = 0
        a_https = 0
        a_hashtag = 0
        a_diff = 0
        for a_tag in a_tags:
            href = a_tag.get("href")
            if href:
                if href == "#":
                    a_hashtag += 1
                elif "javascript:void" in href:
                    a_hashtag += 1
                elif href.startswith('/'):
                    # print(href)
                    if "https" in landing_page:
                        a_https += 1
                    else:
                        a_http += 1
                elif href.startswith('http'):
                    if href.split('/')[2] != current_domain:
                        a_diff += 1
                    if "https" in href:
                        a_https += 1
                    else:
                        a_http += 1
            else:
                a_hashtag += 1
        sample.a_http = a_http / sample.a_count if a_http > 0 else 0
        sample.a_https = a_https / sample.a_count if a_https > 0 else 0
        sample.a_hashtag = a_hashtag / sample.a_count if a_hashtag > 0 else 0
        sample.a_diff = a_diff / sample.a_count if a_diff > 0 else 0

    link_tags = bs.find_all("link")
    sample.link_count = len(link_tags)
    if sample.link_count > 0:
        link_http = 0
        link_https = 0
        link_hashtag = 0
        link_diff = 0
        for link_tag in link_tags:
            href = link_tag.get("href")
            if href:
                if href == "#":
                    link_hashtag += 1
                elif "javascript:void" in href:
                    link_hashtag += 1
                elif href.startswith('/'):
                    if "https" in landing_page:
                        link_https += 1
                    else:
                        link_http += 1
                elif "http" in href:
                    if href.split('/')[2] != current_domain:
                        link_diff += 1
                    if "https://" in href:
                        link_https += 1
                    else:
                        link_http += 1
            else:
                link_hashtag += 1
        sample.link_http = link_http / sample.link_count if link_http > 0 else 0
        sample.link_https = link_https / sample.link_count if link_https > 0 else 0
        sample.link_hashtag = link_hashtag / sample.link_count if link_hashtag > 0 else 0
        sample.link_diff = link_diff / sample.link_count if link_diff > 0 else 0

    sample.img_count = len(bs.find_all("img"))
    sample.button_count = len(bs.find_all("button"))
    sample.div_count = len(bs.find_all("div"))
    sample.iframe_count = len(bs.find_all("iframe"))
    sample.js_count = len(bs.find_all("script"))

    sample.words_count = len(re.sub(r"[\s\r\n\t]", "", bs.get_text()))

    classes = re.findall(r'class=\"[-_\s\w]+\"', str(html))
    classes = list(set(classes))
    sample.class_count = len(classes)

    test = pd.DataFrame([[sample.a_count, sample.img_count, sample.iframe_count, sample.button_count, sample.div_count,
                          sample.class_count, sample.words_count, sample.js_count, sample.link_count, sample.a_http,
                          sample.a_https, sample.link_http, sample.link_https, sample.a_diff, sample.link_diff, sample.a_hashtag, sample.link_hashtag
                          ]])
    test = test.iloc[:, :].to_numpy()
    stdsc = StandardScaler()
    test_std = stdsc.fit_transform(test)
    tag = lr_model.predict(test_std)
    # print("predict: ", tag)
    return tag[0]


def find_final_page(current_url, html, depth):
    if depth == 0:
        return None
    current_domain = current_url.split('/')[2]
    bs = BeautifulSoup(html, "html.parser")
    a_tags = bs.find_all("a")
    for a_tag in a_tags:
        href = a_tag.get("href")
        if not href.startswith('http'):
            continue
        else:
            res = requests.get(href, headers=headers,
                               proxies=proxies, timeout=10)
            if res.url.split('/')[2] == current_domain:
                continue
            else:
                if predict_url(res.html, res.url):
                    return res.url
                else:
                    return find_final_page(res.url, res.html, depth-1)
    return None


def visit_url(url):
    res = requests.get(url, headers=headers, proxies=proxies, timeout=10)
    html = res.text
    landing_page = res.url
    tag = predict_url(html, landing_page)
    if tag == 1:
        return landing_page
    else:
        return find_final_page(landing_page, html, MAX_DEPTH)


def main():
    try:
        url_df = pd.read_csv('./urls_unique_filter.csv',
                             encoding='utf-8', engine='python')
        landing_page_df = pd.read_csv(
            './urls_unique_landing_page.csv', encoding='utf-8', engine='python')
        visited = landing_page_df.iloc[:, 0]
        for url in url_df.iloc[:, 0]:
            if url in visited:
                continue
            print("visiting: ", url)
            landing_page = visit_url(url)
            if landing_page:
                landing_page_domain = '.'.join(
                    landing_page.split('/')[2].split('.')[-2:])
                landing_page_df.loc[len(landing_page_df), :] = [
                    url, landing_page, landing_page_domain]
            else:
                landing_page_df.loc[len(landing_page_df), 0] = [url]
    except Exception as error:
        _logger.error(error)
    finally:
        landing_page_df.to_csv('./urls_unique_landing_page.csv', index=False)


if __name__ == "__main__":
    main()
