from threading import Thread
from bs4 import BeautifulSoup
import requests
import sys
import time
sys.dont_write_bytecode = True
import dbase

main_site = "http://philpapers.org/"
que = []

def scrape_work(url):
    hasPassed = False
    while not hasPassed:
        try:
            response = requests.get(url)
            hasPassed = True
        except:
            print("[-] Connection Failed Waiting To Retry")
            time.sleep(5)
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
    hasPassed = False
    while not hasPassed:
        try:
            response = requests.get(url)
            hasPassed = True
        except:
            print("[-] Connection Failed Waiting To Retry")
            time.sleep(5)
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
    hasPassed = False
    while not hasPassed:
        try:
            response = requests.get(url)
            hasPassed = True
        except:
            print("[-] Connection Failed Waiting To Retry")
            time.sleep(5)
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
        time.sleep(0.2)
        inner_branches = scrape_branch(main_site + x)
        for y in inner_branches["results"]:
            print("[+] Scraping for works in inner branch")
            time.sleep(0.2)
            works = scrape_for_works(main_site + y)
            for t in works:
                time.sleep(0.5)
                raw_data = scrape_work(t)
                isPresent = False
                for i in dbase.get_works():
                    if i.name == raw_data["name"]:
                        isPresent = True
                if not isPresent:
                    que.append({"name": raw_data["name"], "author": raw_data["author"], "branch_name": inner_branches["branch_name"], "citations": raw_data["citations"]})

def thread_que():
    while True:
        if len(que) > 1:
            dbase.addwork(que[0]["name"], que[0]["author"], que[0]["branch_name"], que[0]["citations"])
            del que[0]
        else:
            time.sleep(1)

def main():
    print("[+] Starting philosophy scraper")
    print("[+] Scraping main branch")
    branches = scrape_branch(main_site)
    for i in branches["results"]:
        t = Thread(target=thread_scrape, args=(i,))
        t.start()

if  __name__ == "__main__":
    main()
