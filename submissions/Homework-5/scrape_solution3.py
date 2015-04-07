import argparse
import os
import sys
import logging
import requests
import csv
from BeautifulSoup import BeautifulSoup

log = logging.getLogger(__name__)
log.setLevel(logging.INFO)
loghandler = logging.StreamHandler(sys.stderr)
loghandler.setFormatter(logging.Formatter("[%(asctime)s] %(message)s"))
log.addHandler(loghandler)

user_agent = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2272.76 Safari/537.36"

def test_run(city, datadir='data/'):
	hotel_boxes = []
	c = 1
	cur_file = os.path.join(datadir, city + '-hotelist-' + str(c) + '.html')
	while (os.path.exists(cur_file)):
		with open(cur_file, "r") as h:
			html = h.read()
			soup = BeautifulSoup(html)
			# Extract hotel name, star rating and number of reviews
			hotel_boxes += soup.findAll('div', {'class' :'listing wrap reasoning_v5_wrap jfy_listing p13n_imperfect'})
			if not hotel_boxes:
				log.info("#################################### Option 2 ######################################")
				hotel_boxes = soup.findAll('div', {'class' :'listing_info jfy'})
			if not hotel_boxes:
				log.info("#################################### Option 3 ######################################")
				hotel_boxes = soup.findAll('div', {'class' :'listing easyClear  p13n_imperfect'})
		h.close()
		c += 1
		cur_file = os.path.join(datadir, city + '-hotelist-' + str(c) + '.html')
		break


	scrape_individual_hotels(hotel_boxes)

def scrape_individual_hotels(hotel_boxes):
	hotel_info = {}
	rating_labels = ["Excellent", "Very Good", "Average", "Poor", "Terrible"]
	star_labels = ["Location", "Sleep Quality", "Rooms", "Service", "Value", "Cleanliness"]

	c = 1
	for hotel_box in hotel_boxes:
	 	hotel_name = hotel_box.find("a", {"target" : "_blank"}).find(text=True)
	 	print (hotel_name)
	 	hotel_name = hotel_name.replace(',', ' - ')
	 	print (hotel_name)
	 	hotel_url = hotel_box.find("a", {"target" : "_blank"})['href']
	# 	log.info("Hotel name: %s" % hotel_name.strip())
	 	hotel_info[hotel_name] = []

	 	# Build the request URL
	 	url = "http://www.tripadvisor.com" + hotel_url
	 	# Request the HTML page
	 	headers = {'User-Agent': user_agent}
	 	response = requests.get(url, headers=headers)
	 	html = response.text.encode('utf-8')

		soup = BeautifulSoup(html)
		div = soup.find("div", {"class" : "content wrap trip_type_layout"})

		ratings = div.findAll("span", {"class" :"compositeCount"})
		for i in range(len(rating_labels)):
			hotel_info[hotel_name] += [int(ratings[i].find(text=True).replace(',', ''))]

		stars = div.findAll("span", {"class": "rate sprite-rating_s rating_s"})
		for i in range(len(star_labels)):
			hotel_info[hotel_name] += [float(stars[i].find("img")['alt'].split()[0])]

	print (hotel_info)
	writer = csv.writer(open(args.datadir + args.city + 'dict.csv', 'wb'), quoting=csv.QUOTE_NONE, escapechar="\\")
	writer.writerow(rating_labels + star_labels)
	for key, value in hotel_info.items():
	   writer.writerow([key.replace('\n', '')] + value)

if __name__ == "__main__":
	parser = argparse.ArgumentParser(description='Scrape tripadvisor')
	parser.add_argument('-datadir', type=str,
                        help='Directory with html files',
                        default="data/")
	parser.add_argument('-city', type=str,
                        help='City for which the hotel data is required.',
                        required=True)

	args = parser.parse_args()
	
	test_run(args.city, args.datadir)