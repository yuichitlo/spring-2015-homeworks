from BeautifulSoup import BeautifulSoup
import os
import datetime
import csv

def parse_chart(chart_rows):
	songs = {}
	song_names = []

	for date, rows in chart_rows:
		for row in rows:
			song_name = row.find('h2').find(text=True).replace('\t','').replace('\n','')
			artist = ''
			featuring = ''
			spot = int(row.find('span', {'class': 'this-week'}).find(text=True))
			if row.find('h3').find('a') is None:	
				artist = row.find('h3').find(text=True).replace('\t','').replace('\n','')
			else:
				artist = row.find('h3').find('a').find(text=True).replace('\t','').replace('\n','')

			if (len(artist.split(' Featuring ')) > 1):
					featuring = 'Featuring ' + artist.split(' Featuring ')[1]
					artist = artist.split(' Featuring ')[0]

			if song_name not in song_names:
				songs[song_name] = [artist, featuring, date, spot]
				song_names += [song_name]
			else:
				if songs[song_name][0] == artist:
					songs[song_name] += [spot]
				else:
					if song_name + ' (' + artist + ' Version)' not in song_names:
						songs[song_name + ' (' + artist + ' Version)'] = [artist, featuring, date, spot]
						song_names += [song_name + ' (' + artist + ' Version)']
					else:
						songs[song_name + ' (' + artist + ' Version)'] += [spot]

	writer = csv.writer(open(os.path.join('chart-info.csv'), 'wb'), quoting=csv.QUOTE_NONE, escapechar="\\")
	most_weeks = max([len(li) for li in songs.values()]) - 1
	writer.writerow(['Song', 'Artist', 'Featuring'] + [i for i in range(1, most_weeks)])
	for key, value in songs.items():
		key = key.decode('utf8') if isinstance(key, str) else key
		writer.writerow([key.replace('\n', '')] + value)

	return songs

date = datetime.datetime(2012, 1, 7)
stop = datetime.datetime(2015, 4, 25)
chart_rows = []
while (date <= stop):
	chart = os.path.join(date.strftime("%Y-%m-%d") + '.html')
	f = open(chart)
	html = f.read()
	soup = BeautifulSoup(html)
	chart_rows += [(date.strftime("%Y-%m-%d"), soup.findAll('div', {'class': 'row-primary'}))]

	date = date + datetime.timedelta(7)
	f.close()

all_songs = parse_chart(chart_rows)

print all_songs