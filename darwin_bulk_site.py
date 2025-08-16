import pandas as pd
import json
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
from domain_darwin import extract_domain,extract_top_domain,check_company_id

driver = webdriver.Chrome()
jobs_data = []

my_files=pd.read_excel('Data_for_darwin.xlsx')
crawl_id=my_files['crawlerId']
company_name=my_files['companyName']
company_site=my_files['careerSiteUrl']


def fetch_details(crawl_id,company_name,company_site):

    domain=extract_domain(company_site)
    top_d = extract_top_domain(company_site)
    for page in range(1, 1000):
        company_id=check_company_id(company_site)
        if company_id is None:
            driver.get(f"https://{domain}.darwinbox.{top_d}/ms/candidateapi/job?page={page}&limit=10")
        else:
            driver.get(f"https://{domain}.darwinbox.{top_d}/ms/candidateapi/job?page={page}&limit=10&companyId={company_id}")
        time.sleep(3)

        page_source = driver.page_source

        start_index = page_source.find('<pre>') + len('<pre>')
        end_index = page_source.find('</pre>')
        json_data = page_source[start_index:end_index]


        data = json.loads(json_data)
        jobs = data["message"]["jobs"]


        for job in jobs:
            job_id = job["id"]
            title = job["title"]
            min_exp = job.get("experience_from_num", "N/A")
            max_exp = job.get("experience_to_num", "N/A")
            posted_date = job["created_on"]
            location = job.get("tool_tip_locations", "N/A")

            if company_id is None:
                link=f"https://{domain}.darwinbox.{top_d}/ms/candidate/careers/{job_id}"
            else:
                link = f"https://{domain}.darwinbox.{top_d}/ms/candidate/{company_id}/careers/{job_id}"
            driver.get(link)
            time.sleep(3)

            try:
                jd_element = driver.find_element(By.XPATH, '//div[@class="box p-24"]')
                jd_html = jd_element.get_attribute('innerHTML')
                time.sleep(2)

                # jd_clean_html = re.sub(r'[^\x00-\x7F]+', ' ', jd_html)
                # jd_clean_html = re.sub(r'\s+', ' ', jd_clean_html).strip()

            except Exception as e:
                print(f"Failed to get job description for job ID {job_id}: {e}")
                jd_html = "N/A"

            jobs_data.append({
                "jobCompanyId": int(crawl_id),
                "jobPost": title,
                "jobComName": company_name,
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
        if page==1:
            print('jobCompanyId:',crawl_id,', jobComName:'+company_name)

        print("No. of Pages Done: ",page)
        hold = data['message']['jobscount']
        if hold == 0:
            break



        #except json.JSONDecodeError as e:
         #   print(f"Failed to parse JSON: {e}")


for cid,name,site in zip(crawl_id,company_name,company_site):
    try:
        fetch_details(cid,name,site)
    except:
        pass
driver.quit()

df = pd.DataFrame(jobs_data)
df.to_excel(r'C:\Users\mohd.saad\OneDrive - Info Edge (India) Ltd\Desktop\darwin script jobs\Darwin_Automated_File\Company__'+'DARWIN_ALL_JOBS'+ ".xlsx", index=False)
print("done")

