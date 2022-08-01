import pandas as pd
import numpy as np
import os
import re


def find_all_files(base):
    for root, ds, fs in os.walk(base):
        for f in fs:
            if f.endswith(".csv"):
                fullname = os.path.join(root, f)
                yield fullname, f


def main():
    csv_file_path = './Twitter/'
    output_path = './URL_data/'
    for file, name in find_all_files(csv_file_path):
        url_list = []
        print(file)
        # https://zhuanlan.zhihu.com/p/373482095
        # engine参数解决pandas.errors.ParserError: Error tokenizing data. C error: Buffer over
        csv_file = pd.read_csv(file, encoding='utf-8', engine='python')
        tweets = csv_file.iloc[:, 0].values
        for tweet in tweets:
            urls = re.findall(
                r'((?:(?:[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?\.)+[a-zA-Z]{2,6})+(?:(?:\/[=\w\?]+)*))+',
                tweet)
            for url in urls:
                # print(url)
                if url.startswith('t.co/'):
                    url_list.append("https://" + url[:15])
        url_df = pd.DataFrame(url_list, columns=['url'])
        url_df.to_csv(output_path + name, index=False)


# def find_all_files(base):
#     for root, ds, fs in os.walk(base):
#         for f in fs:
#             if f.endswith(".csv"):
#                 fullname = os.path.join(root, f)
#                 yield fullname
#
#
# def main():
#     csv_file_path = './Twitter/'
#     output_path = './urls.csv'
#     url_list = []
#     for file in find_all_files(csv_file_path):
#         print(file)
#         # https://zhuanlan.zhihu.com/p/373482095
#         # engine参数解决pandas.errors.ParserError: Error tokenizing data. C error: Buffer over
#         csv_file = pd.read_csv(file, encoding='utf-8', engine='python')
#         tweets = csv_file.iloc[:, 0].values
#         for tweet in tweets:
#             urls = re.findall(
#                 r'((?:(?:[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?\.)+[a-zA-Z]{2,6})+(?:(?:\/[=\w\?]+)*))+',
#                 tweet)
#             for url in urls:
#                 # print(url)
#                 if url.startswith('t.co/'):
#                     url_list.append(url[:15])
#     url_df = pd.DataFrame(url_list, columns=['url'])
#     url_df.to_csv(output_path, index=False)


if __name__ == '__main__':
    main()
