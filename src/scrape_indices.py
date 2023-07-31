import requests
from bs4 import BeautifulSoup
import re
import json


def scrape_index(url, vol_idx):

    #procedure for local file

    # Opening the html file
    HTMLFile = open("../data/html/"+url, "r")
    
    # # Reading the file
    index = HTMLFile.read()

    soup = BeautifulSoup(index, 'html.parser')
  
    # Send a GET request to the URL
    # response = requests.get(url)


    # # Parse the HTML content using Beautiful Soup
    # soup = BeautifulSoup(response.content, 'html.parser')

    #Find all unordered lists with class "none"
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
        text = re.sub("\n", " ", text)
        matches = parse_string(text)
        pages = []
        if len(matches)>0:
            matches = matches[0]
            if matches[0].endswith("Life"):
                name = matches[1][:-2]
            else:
                name = matches[0]
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


    with open("../data/indices/index_names_vol_"+str(vol_idx)+".json", "w", encoding="utf-8") as f:
        json.dump(output, f, indent=4, sort_keys=True, ensure_ascii=False)

# volumes = [(1, "https://www.gutenberg.org/files/25326/25326-h/25326-h.htm"),
# (2, "https://www.gutenberg.org/files/25759/25759-h/25759-h.htm"), 
# (3, "https://www.gutenberg.org/files/26860/26860-h/26860-h.htm"),
# (4, "https://www.gutenberg.org/files/28420/28420-h/28420-h.htm"),
# (5, "https://www.gutenberg.org/files/28421/28421-h/28421-h.htm"),
# (6, "https://www.gutenberg.org/files/28422/28422-h/28422-h.htm"),
# (7, "https://www.gutenberg.org/files/31845/31845-h/31845-h.htm"), 
# (8, "https://www.gutenberg.org/files/31938/31938-h/31938-h.htm"),
# (9, "https://www.gutenberg.org/files/32362/32362-h/32362-h.htm"),
# (10, "https://www.gutenberg.org/files/33203/33203-h/33203-h.htm")]


volumes = [
    (4, "28420-h.htm"),
    (5, "28421-h.htm"),
    (6, "28422-h.htm"),
    (7, "31845-h.htm"), 
    (8, "31938-h.htm"),
    (9, "32362-h.htm"),
    (10, "33203-h.htm")]

for idx, URL in volumes:
    scrape_index(url=URL, vol_idx=idx)