import json
from sys import argv, stdout
import urllib
import concurrent.futures as cf
import asyncio
from requests_html import HTMLSession, HTMLResponse


def makeItem(query, url, title, subtitle):
    '''
    Format for alfred json
    '''
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
    '''
    Organize list
    '''
    out = {'items': items}
    return out


def get_search_results(url: str):
    '''
    get search results by xpath
    '''
    session = HTMLSession()
    headers = {
        'User-Agent':
        'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.125 Mobile Safari/537.36'
    }
    r: HTMLResponse = session.get(url, headers=headers)
    results = r.html.xpath("//h3[@class='gs_rt']//a")
    titles = [item.text for item in results]
    links = r.html.xpath("//h3[@class='gs_rt']//a/@href")
    return titles, links


async def search(query):
    '''
    async function to gather search results in first 10 pages
    '''
    encoded_query = urllib.parse.quote(query)
    urls = [
        f"https://scholar.google.com.hk/scholar?&q={encoded_query}&start={page}"
        for page in range(0, 80, 10)
    ]
    with cf.ThreadPoolExecutor(max_workers=8) as executor:
        loop = asyncio.get_event_loop()
        futures = (loop.run_in_executor(executor, get_search_results, url)
                   for url in urls)
        async_results = await asyncio.gather(*futures)
        titles = [title for item in async_results for title in item[0]]
        titles = [f"{n}. {title}" for n, title in enumerate(titles)]
        links = [link for item in async_results for link in item[1]]
    return titles, links


def main():
    '''
    main functions
    '''
    arg_c = len(argv)
    if arg_c <= 1:
        return makeReturn([])
    query = argv[1]
    if not query:
        return makeReturn([])
    loop = asyncio.get_event_loop()
    titles, links = loop.run_until_complete(search(query))
    item = [
        makeItem(query, link, title, link)
        for title, link in zip(titles, links)
    ]
    out = makeReturn(item)
    return json.dumps(out, indent=4) + '\n'


if __name__ == "__main__":
    results = main()
    stdout.write(results)
