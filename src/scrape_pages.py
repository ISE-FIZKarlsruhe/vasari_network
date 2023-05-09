import requests
from bs4 import BeautifulSoup
import re
import csv

# Replace the URL with the webpage you want to scrape
url = "https://www.gutenberg.org/files/25326/25326-h/25326-h.htm"

# Send a GET request to the URL and get the HTML content
response = requests.get(url)
html_content = response.content

# Use BeautifulSoup to parse the HTML content
soup = BeautifulSoup(html_content, "html.parser")

# Find all the text elements and join them into a single string
text = ''.join(soup.find_all(text=True))

# Split the text based on the regular expression "[Pg \d+]"
texts = re.split(r"\[Pg \d+\]", text)

# Put the title of the biography at the beginning of each text.

texts_with_titles = []
title = ""
for text in texts[1:]:
# remove whitespace and unnecessary characters
    text = text.strip()
    text = re.sub("(\n|\r)+", " ", text)

# find title with regular expression
    match_lst = re.findall("(LIFE OF [A-Z]+(,?\s[A-Z]+(?![a-z]))*)", text)

# verify if we did not reach the last chapter of the book "Index of names"

    if "INDEX OF NAMES" in text:
        break
    else:
        if len(match_lst)>0:
            title = match_lst[0][0]
        if title != "":
            if len(match_lst)>0:
                texts_with_titles.append(text)
            else:
                texts_with_titles.append(title+" "+text)

# define the start page number, is different in every volume 
start_page = 3
output = zip(range(start_page, start_page+len(texts_with_titles)),texts_with_titles)

# store the output in csv 
with open("pages_vol_1.csv", "w", encoding="utf-8") as f:
    csv_writer = csv.writer(f)
    csv_writer.writerow(["pg_num", "text"])
    csv_writer.writerows(output)
