import json
from sys import argv, stdout
import urllib
import concurrent.futures as cf
import asyncio
from requests_html import HTMLSession, HTMLResponse


def makeItem(query, url, title, subtitle):
    """
    Format for alfred json
    """
    icon = "0D5BF8C7-11D4-4FF7-A08D-2FAF954E3A43.png"
    true_url = complete_scholar_profile(url)
    item = {
        "uid": true_url,
        "title": title,
        "subtitle": subtitle,
        "arg": true_url,
        "autocomplete": query,
        "icon": {"path": icon},
    }
    return item


def makeReturn(items):
    """
    Organize list
    """
    out = {"items": items}
    return out


def get_search_results(url: str):
    """
    get search results by xpath
    """
    session = HTMLSession()
    headers = {
        "User-Agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.125 Mobile Safari/537.36"
    }
    r: HTMLResponse = session.get(url, headers=headers)
    results = r.html.xpath("//h3[@class='gs_rt']//a")
    titles = [item.text for item in results]
    links = r.html.xpath("//h3[@class='gs_rt']//a/@href")
    return titles, links


def complete_scholar_profile(url: str):
    """
    Complete the missing prefix for user profile links in google scholar.
    """
    if not "https://" in url:
        true_link = "https://scholar.google.com/" + url
        return true_link
    else:
        return url


async def search(query):
    """
    async function to gather search results in first 10 pages
    """
    encoded_query = urllib.parse.quote(query)
    urls = [
        f"https://scholar.google.com/scholar?&q={encoded_query}&start={page}&google_abuse=GOOGLE_ABUSE_EXEMPTION%3DID%3D5996390e8f302f50:TM%3D1597979846:C%3Dr:IP%3D158.132.214.199-:S%3DAPGng0u8PIBYIiJEdJD900VbCQv-pHQ8MA%3B+path%3D/%3B+domain%3Dgoogle.com%3B+expires%3DFri,+21-Aug-2020+06:17:26+GMT"
        for page in range(0, 80, 10)
    ]
    with cf.ThreadPoolExecutor(max_workers=8) as executor:
        loop = asyncio.get_event_loop()
        futures = (
            loop.run_in_executor(executor, get_search_results, url) for url in urls
        )
        async_results = await asyncio.gather(*futures)
        if not async_results is [[]]:
            titles = [title for item in async_results for title in item[0]]
            titles = [f"{n}. {title}" for n, title in enumerate(titles)]
            links = [link for item in async_results for link in item[1]]
        else:
            titles = ["Sorry, rate limit exceeds"]
            links = [urls[0]]
    return titles, links


def main():
    """
    main functions
    """
    arg_c = len(argv)
    if arg_c <= 1:
        return makeReturn([])
    query = argv[1]
    if not query:
        return makeReturn([])
    loop = asyncio.get_event_loop()
    titles, links = loop.run_until_complete(search(query))
    item = [makeItem(query, link, title, link) for title, link in zip(titles, links)]
    out = makeReturn(item)
    return json.dumps(out, indent=4) + "\n"


if __name__ == "__main__":
    results = main()
    stdout.write(results)
