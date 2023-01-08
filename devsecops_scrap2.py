import requests
from bs4 import BeautifulSoup
import pandas as pd
import time

# USER_AGENT = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; rv:91.0) Gecko/20100101 Firefox/91.0'}

USER_AGENT = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:10.0) AppleWebKit/537.36 (KHTML, like Gecko) '
                            'Chrome/61.0.3163.100 Safari/537.36'}


def csv_dump(data, name):
    print(data, name)
    df = pd.DataFrame(data)
    df.index += 1
    df.to_csv(name + ".csv")


def parse_results(raw_response):
    soup = BeautifulSoup(raw_response, 'html.parser')
    results = soup.find_all('div', attrs={'class': 'g'})
    for result in results:
        url = result.find('a', href=True)
        title = result.find('h3')
        if url and title:
            yield {'URL': url['href'], 'Title': title.text.strip()}


def scrape_google(keyword, num_pages):
    results = []
    # Scrape the specified number of pages
    escaped_query = keyword.replace(' ', '+')
    for page in range(1, num_pages + 1):
        google_url = 'https://www.google.com/search?q={}&num={}&start={}&hl={}'.format(escaped_query, num_pages + 1,
                                                                                       page, "en")
        print(google_url)
        # Make a request to Google with the given keyword and page number
        response = requests.request("GET", google_url, headers=USER_AGENT)

        # If rate limited exceed, sleep
        if response.status_code == 429:
            print(response.raise_for_status())
            print(response.headers)
            time.sleep(5)

        # Parse the HTML content of the page
        results += parse_results(response.text)

    return results


# Scrape the first ten pages of Google for the query
if __name__ == '__main__':
    query = '(SecDevOps OR DevSecOps) AND (practices OR capabilities OR tools)'
    # query = 'DevSecOps'
    articles = scrape_google(query, 10)
    print(articles)
    csv_dump(articles, "DevSecOps Google Scrap 2")
