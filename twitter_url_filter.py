# 在twitter_url_visit.py之前先对数据过滤
# 去掉我们不需要的URL

import pandas as pd
import os

white_list = ['twitter.com', 'google.com', 'facebook.com', 'instagram.com', 'youtube.com', 'youtu.be']


def main():
    url_df = pd.read_csv('./urls_unique.csv', encoding='utf-8', engine='python')
    filter_df = url_df[~url_df['domain'].isin(white_list)]
    filter_df.to_csv('./urls_unique_filter.csv', index=False)


if __name__ == '__main__':
    main()
