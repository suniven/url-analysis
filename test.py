import requests
from bs4 import BeautifulSoup
import pandas as pd
from lxml import etree
import re

list = []
csv_file_path = './notsure.csv'
url_df = pd.read_csv(csv_file_path, encoding='utf-8', engine='python')
# url_df = url_df.drop_duplicates()
headers = {
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36"
}
proxies = {
    'http': 'http://127.0.0.1:1080',
    'https': 'http://127.0.0.1:1080'
}
urls = url_df.iloc[:, 0]
for url in urls:
    url = "http://" + url
    print(url)
    res = requests.get(url, headers=headers, timeout=8, proxies=proxies)
    print("{0}: {1}".format(url, res.status_code))
    if res.status_code == "200":
        list.append(url)
df = pd.DataFrame(list, columns=['url'])
df.to_csv('./notsure_unique_visitable.csv', index=False)

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
