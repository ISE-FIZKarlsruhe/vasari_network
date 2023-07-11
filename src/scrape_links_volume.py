import requests
from bs4 import BeautifulSoup
import re
import json



# URL of the page to scrape
url = "https://www.gutenberg.org/files/25759/25759-h/25759-h.htm"

# Send a GET request to the URL
response = requests.get(url)


# Parse the HTML content using Beautiful Soup
soup = BeautifulSoup(response.content, 'html.parser')

# Find all unordered lists with class "none"
ulst = soup.find('ul', {'class': 'none'})


# Initialize an empty list to store the results
results = []


def parse_string(input_string):
    regex_name = "(([A-Z]\w+(\s\w+)*(\s\(.*?\))?,\s)?[A-Z]\w+(\s\w+)*(\s\(.*?\))?)(,\sLife)?,\s(.*?)$"
    groups = re.findall(regex_name, input_string)
    if len(groups)==0:
        if input_string.startswith("as a"):
            groups = [("Vasari, Giorgio", input_string)]
    return groups

output = {}
# Loop through each unordered list
for li in ulst.find_all('li'):
    hrefs = []
    # Get the text of the list item
    text = li.get_text().strip()
    results.append(text)
for text in results:
    matches = parse_string(text)
    pages = []
    if len(matches)>0:
        matches = matches[0]
        if matches[0].endswith("Life"):
            name = matches[1][:-2]
        else:
            name = matches[0]
        print(name)
        page_nums = re.findall("(\d+(?:\-\d+)?)",matches[-1])
        if len(page_nums)>0:
            for num in page_nums:
                if "-" in num:
                    page_range= num.split("-")
                    start = int(page_range[0])
                    end = int(page_range[1])
                    pages.extend(range(start, end+1))
                else:
                    pages.append(int(num))
        if name in output.keys():
            output[name].extend([page for page in pages if page not in output[name]])
        else:
            output[name]=pages


with open("index_names_vol2.json", "w", encoding="utf-8") as f:
    json.dump(output, f, indent=4, sort_keys=True, ensure_ascii=False)