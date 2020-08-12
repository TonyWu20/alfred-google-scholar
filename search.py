import re
import json
import os
from sys import argv, stdout
import urllib
from requests_html import HTMLSession, HTMLResponse


def makeItem(query, url, title, subtitle):
    icon = "0D5BF8C7-11D4-4FF7-A08D-2FAF954E3A43.png"
    item = {
        'uid': url,
        'title': title,
        'subtitle': subtitle,
        'arg': url,
        'autocomplete': query,
        'icon': {
            'path': icon
        }
    }
    return item


def makeReturn(items):
    out = {'items': items}
    return out


def get_search_results(url: str):
    session = HTMLSession()
    r: HTMLResponse = session.get(url)
    results = r.html.xpath("//h3[@class='gs_rt']//a")
    titles = [item.text for item in results]
    links = r.html.xpath("//h3[@class='gs_rt']//a/@href")
    return titles, links


def main():
    arg_c = len(argv)
    if arg_c <= 1:
        return makeReturn([])
    query = argv[1]
    if not query:
        return makeReturn([])
    encoded_query = urllib.parse.quote(query)
    url = f"https://scholar.google.com.hk/scholar?hl=zh-CN&as_sdt=0%2C5&q={encoded_query}"
    titles, links = get_search_results(url)
    item = [
        makeItem(query, link, title, link)
        for title, link in zip(titles, links)
    ]
    out = makeReturn(item)
    return json.dumps(out, indent=4) + '\n'


if __name__ == "__main__":
    results = main()
    stdout.write(results)
