import requests
from bs4 import BeautifulSoup
import re
import csv
def scrape_page(URL, vol_idx):
  print(vol_idx)
  # Replace the URL with the webpage you want to scrape

  # Send a GET request to the URL and get the HTML content
  response = requests.get(URL)
  html_content = response.content

  # Use BeautifulSoup to parse the HTML content
  soup = BeautifulSoup(html_content, "html.parser")



  paragraphs = soup.find_all('p')
  filtered_paragraphs = []
  for p in paragraphs:
      if not p.find_parents("div", class_="figcenter"):
          filtered_paragraphs.append(p.get_text())

  page_id = None
  output = []
  for idx, text in enumerate(filtered_paragraphs):
    text = re.sub(r"(\r)?\n"," ", text)
    page_num = re.findall(r"\[Pg ([0-9]+)\]", text)
    if len(page_num)>0:
      page_id = " ".join(page_num)
    text = re.sub(r"\[Pg [a-z0-9]+\]", "",text)
    if page_id!=None:
      output.append({"pages":page_id, "paragraph_id":idx, "text":text})
  print(output[0])
  keyz = output[0].keys()
  with open("../data/volumes/"+str(vol_idx)+".csv", "w", encoding="utf-8") as f:
      csv_writer = csv.DictWriter(f, keyz)
      csv_writer.writeheader()
      csv_writer.writerows(output)

volumes = [
(4, "https://www.gutenberg.org/files/28420/28420-h/28420-h.htm")]

for idx, URL in volumes:
  scrape_page(URL=URL, vol_idx=idx)