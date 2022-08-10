import requests
from bs4 import BeautifulSoup
import pandas as pd
from lxml import etree
import re
import os
import comm.logger as logger
from comm.model import Sample

# df = pd.DataFrame(columns=['redirect_url', 'landing_page', 'landing_page_domain'])
# df.to_csv('./urls_unique_landing_page.csv', index=False)

# _logger = logger.Logger('info')
# _logger.error('test error')

# 设置域名
df = pd.read_csv('./urls_todo.csv', encoding='utf-8', engine='python')
count = df.shape[0]
df = df.reindex(columns=df.columns.tolist() + ["domain"])
for i in range(count):
    if df.iloc[i, 1] == df.iloc[i, 1]:
        print(df.iloc[i, 1])
        df.iloc[i, 2] = '.'.join(df.iloc[i, 1].split('/')[2].split('.')[-2:])
df.to_csv('./urls_todo_domain.csv', index=False)

# # 合并URLcsv文件
#
#
# def find_all_files(base):
#     for root, ds, fs in os.walk(base):
#         for f in fs:
#             if f.endswith(".csv"):
#                 fullname = os.path.join(root, f)
#                 yield fullname
#
#
# def join():
#     new_df = pd.DataFrame()
#     for file in find_all_files('./URL_unique_split'):
#         df = pd.read_csv(file, encoding='utf-8', engine='python')
#         new_df = pd.concat([df, new_df], ignore_index=True)
#
#     new_df.to_csv('./urls_todo.csv', index=False)
#
#
# join()

# csv_file = pd.read_csv('./notsure_unique_visitable.csv',
#                        encoding='utf-8', engine='python')
# count = csv_file.shape[0]
# for index in range(count):
#     csv_file.iloc[index, 0] = csv_file.iloc[index,
#                                             0].replace('http', 'https')
# csv_file.to_csv('./notsure_unique_visitable.csv', index=False)

# list = []
# csv_file_path = './notsure_unique.csv'
# url_df = pd.read_csv(csv_file_path, encoding='utf-8', engine='python')
# # url_df = url_df.drop_duplicates()
# headers = {
#     "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36"
# }
# proxies = {
#     'http': 'http://127.0.0.1:1080',
#     'https': 'http://127.0.0.1:1080'
# }
# urls = url_df.iloc[:, 0]
# for url in urls:
#     try:
#         url = "http://" + url
#         print(url)
#         res = requests.get(url, headers=headers, timeout=8, proxies=proxies)
#         print("{0}: {1}".format(url, res.status_code))
#         if res.status_code == 200:
#             list.append(url)
#     except Exception as err:
#         print("Error: ", err)
# df = pd.DataFrame(list, columns=['url'])
# df.to_csv('./notsure_unique_visitable.csv', index=False)

# print(res.text)
# print(res.url)
# html = etree.HTML(res.text)
# result = html.xpath('//meta[@http-equiv="refresh" and @content]/@content')
# print(result[:])
# redirect_url = re.search(r'[a-zA-z]+://[^\s]*', result[0])
# print(redirect_url.group())
# url = 'http://www.awakenministries.netFac'
# urls = re.findall(
#     r'[a-zA-z]+://[^\s]*', url)
# print(urls[:])
