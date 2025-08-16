import re
from re import findall


def extract_domain(domains):
    domains=str(domains)
    match=re.findall('(?s).?//([^.]+)',domains)
    if match:
        return match[0]
    else:
        return 0


def extract_top_domain(domains):
    domains=str(domains)
    match=re.findall('(?s)darwinbox.([^/]+)',domains)
    if match:
        return match[0]
    else:
        return None


#print(extract_domain("https://cmr-group.darwinbox.in/ms/candidate/careers")[0])
# print(extract_top_domain('https://cmr-group.darwinbox.in/ms/candidate/careers')[0])
def check_company_id(domains):
    domains=str(domains)
    match=findall('(?s).?candidate/([^/]+).?/careers',domains)
    if match:
        return match[0]
    else:
        return None

#print(check_company_id("https://hoh.darwinbox.in/ms/candidate/5c18bab232d5b/careers"))