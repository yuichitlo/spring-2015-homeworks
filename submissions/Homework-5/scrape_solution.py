#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import sys
import time
import argparse
import logging
import requests
import csv
from BeautifulSoup import BeautifulSoup


log = logging.getLogger(__name__)
log.setLevel(logging.INFO)
loghandler = logging.StreamHandler(sys.stderr)
loghandler.setFormatter(logging.Formatter("[%(asctime)s] %(message)s"))
log.addHandler(loghandler)

base_url = "http://www.tripadvisor.com/"
user_agent = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2272.76 Safari/537.36"



def get_city_page(city, state, datadir):
    """ Returns the URL of the list of the hotels in a city. Corresponds to
    STEP 1 & 2 of the slides.

    Parameters
    ----------
    city : str

    state : str

    datadir : str


    Returns
    -------
    url : str
        The relative link to the website with the hotels list.

    """
    # Build the request URL
    url = base_url + "city=" + city + "&state=" + state
    # Request the HTML page
    headers = {'User-Agent': user_agent}
    response = requests.get(url, headers=headers)
    html = response.text.encode('utf-8')
    with open(os.path.join(datadir, city + '-tourism-page.html'), "w") as h:
        h.write(html)

    # Use BeautifulSoup to extract the url for the list of hotels in
    # the city and state we are interested in.

    # For example in this case we need to get the following href
    # <li class="hotels twoLines">
    # <a href="/Hotels-g60745-Boston_Massachusetts-Hotels.html" data-trk="hotels_nav">...</a>
    soup = BeautifulSoup(html)
    li = soup.find("li", {"class": "hotels twoLines"})
    city_url = li.find('a', href=True)
    return city_url['href']


def get_hotellist_page(city_url, page_count, city, datadir='data/'):
    """ Returns the hotel list HTML. The URL of the list is the result of
    get_city_page(). Also, saves a copy of the HTML to the disk. Corresponds to
    STEP 3 of the slides.

    Parameters
    ----------
    city_url : str
        The relative URL of the hotels in the city we are interested in.
    page_count : int
        The page that we want to fetch. Used for keeping track of our progress.
    city : str
        The name of the city that we are interested in.
    datadir : str, default is 'data/'
        The directory in which to save the downloaded html.

    Returns
    -------
    html : str
        The HTML of the page with the list of the hotels.
    """
    url = base_url + city_url
    # Sleep 2 sec before starting a new http request
    time.sleep(2)
    # Request page
    headers = { 'User-Agent' : user_agent }
    response = requests.get(url, headers=headers)
    html = response.text.encode('utf-8')
    # Save the webpage
    with open(os.path.join(datadir, city + '-hotelist-' + str(page_count) + '.html'), "w") as h:
        h.write(html)
    return html


def parse_hotellist_page(html):
    """Parses the website with the hotel list and prints the hotel name, the
    number of stars and the number of reviews it has. If there is a next page
    in the hotel list, it returns a list to that page. Otherwise, it exits the
    script. Corresponds to STEP 4 of the slides.

    Parameters
    ----------
    html : str
        The HTML of the website with the hotel list.

    Returns
    -------
    URL : str
        If there is a next page, return a relative link to this page.
        Otherwise, exit the script.
    """
    soup = BeautifulSoup(html)
    # # Extract hotel name, star rating and number of reviews
    # hotel_boxes = soup.findAll('div', {'class' :'listing wrap reasoning_v5_wrap jfy_listing p13n_imperfect'})
    # if not hotel_boxes:
    #     log.info("#################################### Option 2 ######################################")
    #     hotel_boxes = soup.findAll('div', {'class' :'listing_info jfy'})
    # if not hotel_boxes:
    #     log.info("#################################### Option 3 ######################################")
    #     hotel_boxes = soup.findAll('div', {'class' :'listing easyClear  p13n_imperfect'})

    # for hotel_box in hotel_boxes:
    #     hotel_name = hotel_box.find("a", {"target" : "_blank"}).find(text=True)
    #     log.info("Hotel name: %s" % hotel_name.strip())

    #     stars = hotel_box.find("img", {"class" : "sprite-ratings"})
    #     if stars:
    #         log.info("Stars: %s" % stars['alt'].split()[0])

    #     num_reviews = hotel_box.find("span", {'class': "more"}).findAll(text=True)
    #     if num_reviews:
    #         log.info("Number of reviews: %s " % [x for x in num_reviews if "review" in x][0].strip())

    # Get next URL page if exists, otherwise exit
    #div = soup.find("div", {"class" : "unified pagination "})
    div = soup.find("div", {"class" : "pagination paginationfillbtm"})
    # check if this is the last page
    #if div.find('span', {'class' : 'nav next disabled'}):
    if div.find('span', {'class' : 'guiArw pageEndNext'}):
        #log.info("We reached last page")
        return None
    # If not, return the url to the next page
    hrefs = div.findAll('a', href= True)
    for href in hrefs:
        if href.find(text = True) == '&raquo;':
            #log.info("Next url is %s" % href['href'])
            return href['href']


def scrape_hotels(city, state, datadir='data/'):
    """Runs the main scraper code

    Parameters
    ----------
    city : str
        The name of the city for which to scrape hotels.

    state : str
        The state in which the city is located.

    datadir : str, default is 'data/'
        The directory under which to save the downloaded html.
    """

    # Get current directory
    current_dir = os.getcwd()
    # Create datadir if does not exist
    if not os.path.exists(os.path.join(current_dir, datadir)):
        os.makedirs(os.path.join(current_dir, datadir))

    # Get URL to obtain the list of hotels in a specific city
    city_url = get_city_page(city, state, datadir)
    c = 0
    while(city_url is not None):
        c += 1
        html = get_hotellist_page(city_url, c, city, datadir)
        city_url = parse_hotellist_page(html)

def parse_hotellist_pages(city, datadir='data/'):
    hotel_boxes = []
    c = 1
    cur_file = os.path.join(datadir, city + '-hotelist-' + str(c) + '.html')
    log.info(cur_file)
    while (os.path.exists(cur_file)):
        with open(cur_file, "r") as h:
            html = h.read()
            soup = BeautifulSoup(html)
            # Extract hotel name, star rating and number of reviews
            cur_hotel_boxes = soup.findAll('div', {'class' :'listing wrap reasoning_v5_wrap jfy_listing p13n_imperfect'})
            if not cur_hotel_boxes:
               # log.info("#################################### Option 2 ######################################")
                cur_hotel_boxes = soup.findAll('div', {'class' :'listing_info jfy'})
            if not cur_hotel_boxes:
                #log.info("#################################### Option 3 ######################################")
                cur_hotel_boxes = soup.findAll('div', {'class' :'listing easyClear  p13n_imperfect'})
            hotel_boxes += cur_hotel_boxes
        h.close()
        c += 1
        cur_file = os.path.join(datadir, city + '-hotelist-' + str(c) + '.html')
        log.info(len(hotel_boxes))
        log.info(cur_file)

    scrape_individual_hotels(hotel_boxes, city, datadir)

def scrape_individual_hotels(hotel_boxes, city, datadir="data/"):
    hotel_info = {}
    rating_labels = ["Excellent", "Very good", "Average", "Poor", "Terrible"]
    category_labels = ["Families", "Couples", "Solo", "Business"]
    star_labels = ["Location", "Sleep Quality", "Rooms", "Service", "Value", "Cleanliness"]

    for hotel_box in hotel_boxes:
        hotel_name = hotel_box.find("a", {"target" : "_blank"}).find(text=True)
        hotel_name = hotel_name.replace(',', ' -')
        hotel_url = hotel_box.find("a", {"target" : "_blank"})['href']
        print (hotel_name)

        # Build the request URL
        url = "http://www.tripadvisor.com" + hotel_url
        # Request the HTML page
        headers = {'User-Agent': user_agent}
        response = requests.get(url, headers=headers)
        html = response.text.encode('utf-8')

        soup = BeautifulSoup(html)
        div = soup.find("div", {"class" : "content wrap trip_type_layout"})

        if div is not None:
            hotel_info[hotel_name] = []
            ratings_div = div.findAll("div", {"class":"wrap row"})
            #ratings = div.findAll("span", {"class" :"compositeCount"})
            for i in range(len(rating_labels)):
                rating = ratings_div[i].find("span", {"class": "compositeCount"})
                if rating is not None:
                    hotel_info[hotel_name] += [int(rating.find(text=True).replace(',', ''))]
                else:
                    hotel_info[hotel_name] += [0]

            category_div = div.findAll("div", {"class": "filter_connection_wrapper"})
            for i in range(len(category_labels)):
                value = category_div[i].findAll("div")[0].find(text=True)
                if value is not None:
                    hotel_info[hotel_name] += [int(category_div[i].findAll("div")[1].find(text=True).replace(',', ''))]
                else:
                    hotel_info[hotel_name] += 0

            stars_div = div.find("div", {"class":"wrap subrating"})
            cur_star_labels = [label.find("div", {"class": "name"}).find(text=True) for label in stars_div.findAll("li")]
            cur_stars = 0
            stars = div.findAll("span", {"class": "rate sprite-rating_s rating_s"})
            for i in range(len(star_labels)):
                if star_labels[i] not in cur_star_labels:
                    hotel_info[hotel_name] += [0]
                else:
                    hotel_info[hotel_name] += [float(stars[cur_stars].find("img")['alt'].split()[0])]
                    cur_stars += 1


    writer = csv.writer(open(os.path.join(datadir, city + '-hotel-info.csv'), 'wb'), quoting=csv.QUOTE_NONE, escapechar="\\")
    writer.writerow(rating_labels + category_labels + star_labels)
    for key, value in hotel_info.items():
       writer.writerow([key.replace('\n', '')] + value)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Scrape tripadvisor')
    parser.add_argument('-datadir', type=str,
                        help='Directory to store raw html files',
                        default="data/")
    #parser.add_argument('-state', type=str,
    #                    help='State for which the hotel data is required.',
    #                    required=True)
    parser.add_argument('-city', type=str,
                        help='City for which the hotel data is required.',
                        required=True)

    args = parser.parse_args()
    #scrape_hotels(args.city, args.state, args.datadir)
    parse_hotellist_pages(args.city, args.datadir)
