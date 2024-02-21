import requests
import csv
import time
import json
from bs4 import BeautifulSoup

class Immoscraper:

    def __init__(self):
        pass
    
    def get_property_urls(num_of_pages, session=None):
        '''Gets a list of urls of properties for sale from immoweb

        :param: number_of_pages(int): number of immoweb pages to process
        :param: session (requests.Session): optional session object for requests

        :return: (list) all property urls in the specified page(s)
        '''
        if session is None:
            session = requests.Session()

        all_urls = []
        for i in range(1, num_of_pages + 1):
 #           print(i)
            root_url = f"https://www.immoweb.be/en/search/house-and-apartment/for-sale?countries=BE&page={i}"
            req = session.get(root_url)
            soup = BeautifulSoup(req.content, "html.parser")
            if req.status_code == 200:
                all_urls.extend(tag.get("href") for tag in soup.find_all("a", attrs={"class": "card__title-link"}))
            else:
                print("No url found.")
                break
#        print(f"Number of urls: {len(all_urls)}")
        return all_urls


    def get_property_details(url):
        ''' Extract property details from a given url

        :param: url (str): url of property to pull details from

        :return: (dict) property details in a dictionary
        '''
        #Example: 'https://www.immoweb.be/en/classified/house/for-sale/leuven/3000/10850046'
        property_dict = {
            "property_id": 10850046, 
            "locality_name": 'leuven', 
            "postal_code": 3000, 
            "price": 845000, 
            "property_type": 1, 
                # 1=house, 2=apartment
            "subtype": 5, 
                # 1=Bungalow, 2=Chalet, 3=Farmhouse, 4=Country house, 5=Town-house, 6=Mansion, 7=Villa,
                # 8=Manor house, 9= Ground floor, 10=Duplex, 11=Triplex, 12=Studio, 13=Penthouse, 14=Loft
            "sale_type": 'private',
            "num_rooms": 3, 
            "living_area": 173, 
            "equipped_kitchen": 1, 
            "furnished": 0, 
            "open_fire": 0, 
            "terrace_area": 6, 
            "garden_area": 24,
            "surface_of_good": 76, 
            "num_facades": 2, 
            "swimming_pool": 0, 
            "building_state": 1,
                # 1=good, 2=As new, 3=To restore, 4=Just renovated, 5=To be done up, 6=To renovate
            "url": url
        }

        return property_dict


    def write_dict_to_csv(data_dict, csv_filename):
        keys = data_dict.keys()

        with open(csv_filename, 'w', newline='') as csv_file:
            writer = csv.DictWriter(csv_file, fieldnames=keys)        
            writer.writeheader()        
            writer.writerow(data_dict)
    

def write_json(content, file):
    with open(file, 'w') as json_file:
        json.dump(content, json_file, indent=4)

    print("Property URLs have been saved to:", file)




# start_time = time.time()
# immo_urls = Immoscraper.get_property_urls(334) --> 403 seconds
# end_time = time.time()
# elapsed_time = end_time - start_time
# print(f"Elapsed time: {elapsed_time} seconds")

# write_json(immo_urls, "immo_urls.json")
    


#import library:
from concurrent.futures import ThreadPoolExecutor
#making a function to thread the data
def thread_properties():
    immo = Immoscraper()
    urls = immo.get_property_urls(10)           #get urls from 10pages
    with ThreadPoolExecutor(max_workers=10) as executor:
        executor.map(immo.get_property_details, urls)


# to compaire with and without threading:
def time_with_theading():
    immo = Immoscraper()
    start_time = time.time()
    urls = immo.get_property_urls(10)           #get urls from 10pages

    with ThreadPoolExecutor(max_workers=10) as executor:
        executor.map(immo.get_property_details, urls)
    
    end_time = time.time()
    time_with_threading = end_time - start_time
    print("Time with treading: ", time_with_theading)

def time_without_threading():
    immo = Immoscraper()
    start_time = time.time()
    urls = immo.get_property_urls(10)           #get urls from 10pages

    for url in urls:
        immo.get_property_urls(10)              #get url for 10 pages

    end_time = time.time()
    time_without_threading = end_time - start_time
    print("Time with treading: ", time_without_threading)






if __name__ == "__main__":
    time_with_theading()
    time_without_threading()



     