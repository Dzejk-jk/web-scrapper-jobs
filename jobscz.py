from bs4 import BeautifulSoup
import requests

MAX_RESULTS_ON_PAGE = 37

searching_job = str(input("Enter word for searching your job: "))

url = f"https://beta.www.jobs.cz/prace/?q%5B%5D={searching_job}"
page = requests.get(url).text
doc = BeautifulSoup(page, "html.parser")

page_text = doc.find(class_="Pagination")

# finding job offers
job_offers_found = doc.find("strong")
pages_int = int(job_offers_found.text.strip().replace("\xa0","")) 
pages_count = pages_int // MAX_RESULTS_ON_PAGE if pages_int % MAX_RESULTS_ON_PAGE == 0 \
              else pages_int // MAX_RESULTS_ON_PAGE + 1

jobs_found = {}

# scrapping pages
for page in range(1, pages_count + 1):
    url = f"https://beta.www.jobs.cz/prace/?q%5B%5D={searching_job}&page={page}"
    page = requests.get(url).text
    doc = BeautifulSoup(page, "html.parser")
    
    results = doc.find("div", class_="Container Container--cygnus pb-1300")
    jobs = results.find_all("article", class_="SearchResultCard")

    # scrapping search results
    for job in jobs:
        result = job.find("h2", class_="SearchResultCard__title")
        if searching_job in result.text.lower():
            job_result = result.text.strip()
            job_result_url = result.find_all("a")[0]["href"]
            job_result_location = job.find_all("li", class_="SearchResultCard__footerItem")[1].text.strip()
            
            jobs_found[job_result] = {"Link": job_result_url, "location": job_result_location} 

# writting jobs founded to the text file                    
with open("jobs.txt", "w", encoding="utf-8") as job_file:
    job_file.write("Jobs found:")                    
    for job, details in jobs_found.items():
        job_file.write("\n"*2)
        job_file.write(job)
        for detail, value in details.items():
            job_file.write("\n")
            job_file.write(f"\t{detail}: {value}")
    print("Done")