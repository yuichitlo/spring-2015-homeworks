import datetime
import os
import requests

base_url = "http://www.billboard.com/charts/hot-100/"
user_agent = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2272.76 Safari/537.36"

stop = datetime.datetime(2012, 1, 7)
date = datetime.datetime(2015, 4, 18)
while (stop <= date):
	url = base_url + date.strftime("%Y-%m-%d")
	# Request the HTML page
	headers = {'User-Agent': user_agent}
	response = requests.get(url, headers=headers)
	html = response.text.encode('utf-8')
	with open(os.path.join(date.strftime("%Y-%m-%d") + '.html'), "w") as h:
		h.write(html)

	date = date - datetime.timedelta(7)