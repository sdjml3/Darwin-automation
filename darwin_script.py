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
#https://rebithr.darwinbox.in/ms/candidate/careers
jobs_data = []
domain="rebithr"
top_d='in'

for page in range(1, 10):

    driver.get(f"https://{domain}.darwinbox.{top_d}/ms/candidateapi/job?page={page}&limit=10")
    time.sleep(3)

    page_source = driver.page_source

    start_index = page_source.find('<pre>') + len('<pre>')
    end_index = page_source.find('</pre>')
    json_data = page_source[start_index:end_index]

    try:
        data = json.loads(json_data)
        jobs = data["message"]["jobs"]

        for job in jobs:
            job_id = job["id"]
            title = job["title"]
            min_exp = job.get("experience_from_num", "N/A")
            max_exp = job.get("experience_to_num", "N/A")
            posted_date = job["created_on"]
            location = job.get("tool_tip_locations", "N/A")
            link = f"https://{domain}.darwinbox.{top_d}/ms/candidate/careers/{job_id}"

            driver.get(link)
            time.sleep(3)
            try:
                jd_element = driver.find_element(By.XPATH, '//div[@class="box p-24"]')
                jd_html = jd_element.get_attribute('innerHTML')

                # jd_clean_html = re.sub(r'[^\x00-\x7F]+', ' ', jd_html)
                # jd_clean_html = re.sub(r'\s+', ' ', jd_clean_html).strip()

            except Exception as e:
                print(f"Failed to get job description for job ID {job_id}: {e}")
                jd_html = "N/A"

            jobs_data.append({
                "jobCompanyId": "4571252",
                "jobPost": title,
                "jobComName": "Reserve Bank Information Technology Pvt. Ltd.",
                "jobDesc": jd_html,
                "jobCity": location,
                "jobMinExp": min_exp,
                "jobMaxExp": max_exp,
                "jobMinCtc": 0,
                "jobMaxCtc": 0,
                "jobWebsite": link,
                "jobRefNo": "",
                "jobPostedDate": posted_date,
                "Client Type": "new",
                "Client Type 1": "new"

            })

        print(page)

    except json.JSONDecodeError as e:
        print(f"Failed to parse JSON: {e}")

driver.quit()

df = pd.DataFrame(jobs_data)
df.to_excel(r'C:\Users\mohd.saad\OneDrive - Info Edge (India) Ltd\Desktop\darwin script jobs\Company__' +domain+ ".xlsx", index=False)

print("done")