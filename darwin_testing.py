import requests
import pandas as pd
import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import time
import re
from domain_darwin import extract_domain,extract_top_domain

driver = webdriver.Chrome()

jobs_data = []

domain=extract_domain("https://mpl.darwinbox.in/ms/candidateapi/job?page=5&limit=10")
top_d='in'
page=9
url=f"https://{domain}.darwinbox.{top_d}/ms/candidateapi/job?page={page}&limit=10"

driver.get(url)
time.sleep(4)
page_source=driver.page_source
start_index = page_source.find('<pre>') + len('<pre>')
end_index = page_source.find('</pre>')
json_data = page_source[start_index:end_index]
data=json.loads(json_data)
data_type=data['message']['jobs']
if data_type==[]:
    print('yes')
driver.quit()
