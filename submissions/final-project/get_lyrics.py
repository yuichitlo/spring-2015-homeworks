import os
import requests
from BeautifulSoup import BeautifulSoup
import csv
import unicodedata

base_url = "http://genius.com/search?q="
user_agent = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2272.76 Safari/537.36"

f = open('chart-info-addt.csv')
not_found = []
original_artist = {'Seven Nation Army': 'The White Stripes', 'Take Me To Church': 'Hozier', 'Bridge Over Troubled Water': 'Simon &amp; Garfunkel', 'Say Aah': 'Trey Songz', 'Let It Be': 'The Beatles', 'I Have Nothing': 'Whitney Houston', 'Make It Rain': 'Ed Sheeran', 'A Case of You': 'Joni Mitchell', 'Roxanne': 'The Police', 'Hallelujah': 'Leonard Cohen'}
for row in f:
	tokens = row.replace('\n','').replace('\r','').split(',')
	if tokens[0] != 'Song':
		song = tokens[0]
		artist = tokens[1]
		
		song_explicit = song.replace('#', '').replace('F**k', 'Fuck').replace('F*****g', 'Fuck').replace('Sh*t', 'Shit')
		if 'Version)' in song:
		 	song_tokens = song.split('(')
		 	song_explicit = song_tokens[0]
		
		actual_artist = ''
		if song in original_artist:
			actual_artist = original_artist[song]
		else:
			actual_artist = artist
		
		headers = {'User-Agent': user_agent}
		response = requests.get(url, headers=headers)
		url = base_url + song_explicit + '+' + actual_artist.replace(' ', '+')
		if response.status_code != 404:
			html = response.text.encode('utf-8')
			soup = BeautifulSoup(html)
			print html
			link = soup.find('li', {'class': 'search_result'})
			if link is not None:
				link = link.find('a', href=True).get('href')
			else:
				not_found += [song_explicit]
				continue

			response = requests.get(link, headers=headers)
			if response.status_code != 404:
				html = response.text.encode('utf-8')
				soup = BeautifulSoup(html)
				section = soup.find('div', {'class': 'lyrics'})
				tokens = section.findAll(text=True)
				cur_line = ''
				lyrics = []
				for token in tokens:
					if '\n' in token:
						lyrics += [cur_line]
						cur_line = ''
						if "u'\n'" != token:
							cur_line += token.replace('\n','')
					else:
						cur_line += token

				writer = csv.writer(open(os.path.join('data/' + song.replace('/','') + '-' + artist + '.csv'), 'wb'), delimiter=';', quoting=csv.QUOTE_NONE, escapechar=",")
				lyrics = [unicodedata.normalize('NFKD', lyric.replace("\r", " ").replace("\n", " ").replace("\t", '').replace("\"", "").replace(u"\u2018", "").replace(u"\u2019", "").replace(u'\u2014', ' - ').replace(u'\u201c', '').replace(u'\xfc','').replace(u'\u201d', '').replace(u'\xe9', '').replace(u'\u2013', '').replace(u'\xdc','')).encode('ascii','ignore') for lyric in lyrics]
				writer.writerow(lyrics)

writer = csv.writer(open(os.path.join('data/' + 'not_found.csv'), 'wb'), quoting=csv.QUOTE_NONE, escapechar=",")
writer.writerow(not_found)
