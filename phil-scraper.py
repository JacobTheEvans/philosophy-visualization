from threading import Thread
from bs4 import BeautifulSoup
import requests
import sys
import time
sys.dont_write_bytecode = True
import dbase

main_site = "http://philpapers.org/"

def scrape_work(url):
    response = requests.get(url)
    html_content = response.content
    html_doc = BeautifulSoup(html_content)

    outer_name = html_doc.find("h1", {"class": "recTitle"})
    try:
        name = outer_name.find("a").text
    except:
        name = "None found"

    outer_auth = html_doc.find("span", {"itemprop": "author"})
    try:
        auth = outer_auth.text
    except:
        auth = "None found"

    cit = []
    outer_citations = html_doc.find_all("div", {"class": "citation"})
    for i in outer_citations:
        cit.append(i.find("span", {"class": "articleTitle recTitle"}).text)
    return {"name": name, "citations": cit, "author": auth}

def scrape_branch(url):
    response = requests.get(url)
    html_content = response.content
    html_doc = BeautifulSoup(html_content)
    branch_elements = html_doc.find_all("a", {"class": "tocCatName catName4"})

    results = []
    for i in branch_elements:
        results.append(i["href"])
    branch_name_outer = html_doc.find("h1", {"class": "gh"})
    try:
        branch_name = branch_name_outer.text
    except:
        branch_name = "None Found"
    return {"results": results, "branch_name": branch_name}

def scrape_for_works(url):
        response = requests.get(url)
        html_content = response.content
        html_doc = BeautifulSoup(html_content)
        elements = html_doc.find_all("span", {"class": "citation"})

        results = []
        for i in elements:
            results.append(i.find("a")["href"])
        return results

def thread_scrape(url):
    print("[+] Scraping sub branch")
    sub_branches = scrape_branch(main_site + url)
    for x in sub_branches["results"]:
        print("[+] Scraping inner branch")
        inner_branches = scrape_branch(main_site + x)
        for y in inner_branches["results"]:
            print("[+] Scraping for works in inner branch")
            works = scrape_for_works(main_site + y)
            for t in works:
                raw_data = scrape_work(t)
                isPresent = False
                for i in dbase.get_works():
                    if i.name == raw_data["name"]:
                        isPresent = True
                if not isPresent:
                    dbase.add_work(raw_data["name"], raw_data["author"], inner_branches["branch_name"], raw_data["citations"])

def main():
    print("[+] Starting philosophy scraper")
    print("[+] Scraping main branch")
    branches = scrape_branch(main_site)
    for i in branches["results"]:
        t = Thread(target=thread_scrape, args=(i,))
        t.start()

if  __name__ == "__main__":
    main()
