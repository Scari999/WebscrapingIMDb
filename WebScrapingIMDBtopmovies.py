from bs4 import BeautifulSoup
import requests
import pandas as pd
import numpy as np
import time
import re
from requests.exceptions import HTTPError
from urllib.request import urlopen

content = None

# Added headers with a User-Agent string to bypass 403 Client Error: Forbidden
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36'
    }


def crawl_website(url: str, headers: str) -> str:
    try:
        source = requests.get(url, headers=headers)
        source.raise_for_status()

    except HTTPError as exc:
        print(exc)

    else:
        return source.text


URL = 'https://www.imdb.com/chart/top/'
content = crawl_website(url=URL, headers=headers)


#Using BeautifulSoup to get the page in HTML
page = BeautifulSoup(content, 'html.parser')

# Variables where we place the final data and some for temporary storage
content_extract = []
year=[""]
ranking=[""]
title=[""]
rating=[""]

table = page.find('div', {'data-testid': 'chart-layout-main-column'})

movies = table.find("ul")

for film in movies.find_all('li'):

  film = film.get_text(";").strip().split(";")

  year.append(film[1])
  ranking.append(film[0].split(".")[0])
  title.append(film[0].split(".")[1])
  rating.append(film[4])

year.pop(0)
print(year)

ranking.pop(0)
print(ranking)

title.pop(0)
print(title)

rating.pop(0)
print(rating)

data = {'Ranking' : ranking, 'Title' : title, 'Year' : year, 'Rating' : rating}

print(data)

content_extract = pd.DataFrame(data=data)

print(content_extract)

# Save the DataFrame to a CSV file
# encoding = 'utf-8' for compatitbility (symbols, languages other than english)
output_file = 'imdb_top_movies.csv'
content_extract.to_csv(output_file, index=False, encoding='utf-8')

print(f"Data has been saved to {output_file}")