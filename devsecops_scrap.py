import requests
import urllib
import pandas as pd
from requests_html import HTML
from requests_html import HTMLSession


def get_source(url):
    """Return the source code for the provided URL.

    Argso
        url (string): URL of the page to scrape.

    Returns:
        response (object): HTTP response object from requests_html.
    """

    try:
        session = HTMLSession()
        response = session.get(url)
        return response

    except requests.exceptions.RequestException as e:
        print(e)


def csv_dump(data, name):
    print(data, name)
    df = pd.DataFrame(data)
    df.index += 1
    df.to_csv(name + ".csv")


def get_results(query):
    query = urllib.parse.quote_plus(query)
    response = get_source("https://www.google.com/search?q=" + query + f"start={(1-1)*10}")
    # response = requests.get(f"https://www.google.com/search?q={query}&start={(1 - 1) * 10}")
    return response


def parse_results(response):
    css_identifier_result = ".tF2Cxc"
    css_identifier_title = "h3"
    css_identifier_link = ".yuRUbf a"
    css_identifier_text = ".VwiC3b"

    results = response.html.find(css_identifier_result)

    output = []

    for result in results:
        item = {
            'title': result.find(css_identifier_title, first=True).text,
            'link': result.find(css_identifier_link, first=True).attrs['href'],
            'text': result.find(css_identifier_text, first=True).text
        }

        output.append(item)

    return output


def google_search(query):
    response = get_results(query)
    return parse_results(response)


results = google_search("DevSecOps")
csv_dump(results, "DevSecOps Scraping")
