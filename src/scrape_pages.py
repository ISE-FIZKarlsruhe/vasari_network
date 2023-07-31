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
          sibling_heading = p.find_previous_sibling(['h2'])
          if sibling_heading:
            p_string = sibling_heading.get_text() + ' ' + p.get_text()
            filtered_paragraphs.append(p_string)
          else:
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
  with open("../data/volumes/pages_vol_"+str(vol_idx)+".csv", "w", encoding="utf-8") as f:
      csv_writer = csv.DictWriter(f, keyz)
      csv_writer.writeheader()
      csv_writer.writerows(output)

volumes = [(1, "https://www.gutenberg.org/files/25326/25326-h/25326-h.htm"),
(2, "https://www.gutenberg.org/files/25759/25759-h/25759-h.htm"), 
(3, "https://www.gutenberg.org/files/26860/26860-h/26860-h.htm"),
(4, "https://www.gutenberg.org/files/28420/28420-h/28420-h.htm"),
(5, "https://www.gutenberg.org/files/28421/28421-h/28421-h.htm"),
(6, "https://www.gutenberg.org/files/28422/28422-h/28422-h.htm"),
(7, "https://www.gutenberg.org/files/31845/31845-h/31845-h.htm"), 
(8, "https://www.gutenberg.org/files/31938/31938-h/31938-h.htm"),
(9, "https://www.gutenberg.org/files/32362/32362-h/32362-h.htm"), 
(10, "https://www.gutenberg.org/files/33203/33203-h/33203-h.htm")]

for idx, URL in volumes:
  scrape_page(URL=URL, vol_idx=idx)