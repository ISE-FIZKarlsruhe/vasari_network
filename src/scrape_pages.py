import requests
from bs4 import BeautifulSoup
import re
import csv

# Replace the URL with the webpage you want to scrape
url = "https://www.gutenberg.org/files/25759/25759-h/25759-h.htm"

# Send a GET request to the URL and get the HTML content
response = requests.get(url)
html_content = response.content

# Use BeautifulSoup to parse the HTML content
soup = BeautifulSoup(html_content, "html.parser")



paragraphs = soup.find_all('p')
filtered_paragraphs = []
for p in paragraphs:
    if not p.find_parents("div", class_="figcenter"):
        sibling_heading = p.find_previous_sibling(['h2'])
        if sibling_heading:
          p_string = sibling_heading.get_text() + ' ' + p.get_text()
          filtered_paragraphs.append(p_string)
        else:
          filtered_paragraphs.append(p.get_text())

page_id = None
output = []
for idx, text in enumerate(filtered_paragraphs):
  text = re.sub(r"\r\n"," ", text)
  page_num = re.findall(r"\[Pg ([0-9]+)\]", text)
  if len(page_num)>0:
    page_id = " ".join(page_num)
  text = re.sub(r"\[Pg [a-z0-9]+\]", "",text)
  if page_id!=None:
    output.append({"pages":page_id, "paragraph_id":idx, "text":text})
    print(output)

keyz = output[0].keys()
with open("pages_vol_2.csv", "w", encoding="utf-8") as f:
    csv_writer = csv.DictWriter(f, keyz)
    csv_writer.writeheader()
    csv_writer.writerows(output)