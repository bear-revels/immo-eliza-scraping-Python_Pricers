import requests
from bs4 import BeautifulSoup
import threading
#from scraper import get_property_urls
from time import Rlock                #need if we want to wait on info from an other thread to continue


#lock =  threading.Lock()            #not using it now
num_pages = 11

import time
start_time = time.time()
def get_property_urls(num_of_pages, session=None):
    if session is None:
            session = requests.Session()
    #store threads objects into :
    threads = []
    '''iteration over list all_urls (from Geraldine) and for all urls create a thread that calls get_property_urls
    function as argument and start, and we want to split each batch into 10  pages (optional)'''
    for i in range(0, num_pages, 10):
        start_page = i +1
        end_page = min(i + 10, num_pages)            #check if max 10 pages
        thread = threading.Thread(target=get_property_urls, args=(start_page, end_page, session, urls))
        threads.append(thread)
        thread.start()
    '''making sure all threads are done before continuing'''
    for thread in threads:
        thread.join()

concurrency_time = time.time() - start_time
print("Time to loop throughout Concurrency: ", concurrency_time)
    

#parallelism

urls = []
start_time = time.time()
for i in range (1, num_page + 1):
        print(i)
        root_url = f'https://www.immoweb.be/en/search/house-and-apertment/for-sale?countries=BE&page={i}'
        req = session.get(root_url)
        content = req.content
        soup = BeautifulSoup(content, "html.parser")
        if req.status_code == 200:
            urls.extend(tag.get("href")for tag in soup.find_all("a", attrs={"class":"card__title-link"}))
        else:
            print("No url found")
            break
parallel_time = time.time - start_time
print(" Parallel time: ", parallel_time)



