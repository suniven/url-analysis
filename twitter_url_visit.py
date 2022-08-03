# 访问之前从短链接中获得的重定向URL
# 通过模型判断是否为final page

import pandas as pd
import joblib
import os
import re
import time
import requests
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
import requests


def main():
    csv_file = './urls_unique_filter.csv'
    url_df = pd.read_csv(csv_file, encoding='utf-8', engine='python')


if __name__ == "__main__":
    main()
