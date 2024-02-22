import requests
from bs4 import BeautifulSoup

url = "https://pythonjobs.github.io/"
page = requests.get(url)

soup = BeautifulSoup(page.content, "html.parser")

results = soup.find(id="content")

job_elements = results.find_all("div", class_="job")

for job_element in job_elements:
    company = job_element.find_all("span", class_="info")[3]
    location = job_element.find_all("span", class_="info")[0]
    title = job_element.find("h1")
    detail = job_element.find("p", class_="detail")
    link_url = job_element.find_all("a", class_="go_button")[0]["href"]
    print(title.text.strip())
    print(company.text.strip())
    print(location.text.strip())
    print(f"Detail: {detail.text.strip()}")
    print("Apply here: pythonjobs.github.io"+link_url)
    print()