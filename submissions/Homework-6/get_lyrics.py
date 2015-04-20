import os
import requests
from BeautifulSoup import BeautifulSoup
import csv
import unicodedata

base_url = "http://genius.com/search?q="
user_agent = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2272.76 Safari/537.36"

f = open('chart-info-addt.csv')
not_found = []
for row in f:
	tokens = row.replace('\n','').replace('\r','').split(',')
	if tokens[0] != 'Song':
		song = tokens[0]
		artist = tokens[1]
		
		if song in [u'Word Crimes',u'Tonight Is The Night',u'Sugar',u'Please Remember Me',u'Human Nature',u'Go Get It',u'Live For The Night',u'My Story',u'I Do',u'Young And Beautiful',u'Magic (Coldplay Version)',u'Begin Again',u'A Light That Never Comes',u'Die In Your Arms',u'White Walls',u'Automatic',u'Stoner',u'Eyes Open',u'Me And My Broken Heart',u'Let Me Love You (Until You Learn To Love Yourself)',u'Play The Guitar',u'Southern Girl',u'Night Changes',u'Beat Of The Music',u'Acapella',u'Rewind',u'Holland Road',u'Good Time',u'Started From The Bottom',u'Jump Right In',u'Don&#039;t You Worry Child (Swedish House Mafia Feat. John Martin Version',u'Ready Or Not',u'Can&#039;t Help Falling In Love',u'Without You (Glee Cast Version)',u'Gangnam Style',u'Do You Want To Build A Snowman?',u'Let It Rain',u'Pom Poms',u'Prayer In C',u'Tuesday',u'The Old Rugged Cross',u'Talladega',u'Wonderland',u'Home',u'Don&#039;t Wake Me Up',u'I Hold On',u'Can&#039;t Get Enough',u'Pompeii',u'Sirens',u'Give It 2 U',u'In Your Arms',u'FourFiveSeconds',u'Neon Light',u'Stay',u'Try Me',u'Levels',u'Compass',u'I Can&#039;t Tell You Why',u'Everything I Didn&#039;t Say',u'I Like It Like That',u'Gone',u'The Prayer',u'Made Me',u'The Worst',u'Seen It All',u'Crash And Burn',u'El Cerrito Place',u'1994',u'Hard To Love',u'Crown',u'We Are One (Ole Ola) [The 2014 FIFA World Cup Official Song]',u'Turn The Page',u'On Top Of The World',u'Nobody Love',u'What Makes You Beautiful',u'So Many Girls',u'Reality',u'Homegrown',u'C&#039;mon',u'Lonely Tonight',u'We Run The Night',u'Black Widow',u'Heroes (We Could Be)',u'A Little Party Never Killed Nobody (All We Got)',u'A Woman Like You',u'Where It&#039;s At',u'Hey Girl',u'Drink On It',u'If I Lose Myself',u'Gotta Have It',u'Sweet Little Somethin&#039;',u'Get Low',u'Party On Fifth Ave.',u'Long Live A$AP',u'I Don&#039;t F**k With You',u'Get Lucky',u'Come Join The Murder',u'Mercy (Dave Matthews Band Version)',u'Amnesia',u'When We Stand Together',u'Good Lovin',u'Slow Motion',u'I&#039;m All Yours',u'When I Was Your Man',u'Pirate Flag',u'It&#039;s Time (Glee Cast Version)',u'They Don&#039;t Know',u'Mercy',u'Kiss Me Kiss Me',u'She Came To Give It To You',u'Feel So Close',u'Now &amp; Forever',u'We Still In This B****',u'Santa Tell Me',u'El Perdon',u'Believe Me',u'Timber',u'Wildfire',u'Move That Doh',u'Between The Raindrops',u'Midnight',u'Wop',u'Worst Behavior',u'Sweet Nothing',u'Bad Blood (Taylor Swift Version)',u'TKO',u'Raise &#039;Em Up',u'Downtown',u'Wiggle',u'Last Christmas',u'Safe &amp; Sound',u'Lookin&#039; For That Girl',u'Bugatti',u'Little Bit Of Everything',u'Summertime Sadness (Lana Del Rey &amp; Cedric Gervais Version)',u'Work',u'Leave Your Lover',u'No Mediocre',u'Dear Future Husband',u'CoCo',u'Billie Jean',u'Change Me',u'Doin&#039; What She Likes',u'Beat It',u'Round Of Applause',u'Mr. Wrong',u'We Are Young (Fun. Version)',u'Titanium',u'Human',u'Mirror',u'Troublemaker',u'Irresistible',u'Better Than I Know Myself',u'Cups (Pitch Perfect&#039;s When I&#039;m Gone)',u'Almost Is Never Enough',u'Trophies',u'Adore You',u'LoveHate Thing',u'Hookah',u'Turn Down For What',u'It&#039;s A Man&#039;s\ Man&#039;s\ Man&#039;s World',u'Power Trip',u'We Found Love',u'Perfect Storm',u'What Kind Of Man',u'Hail To The King',u'One Last Time',u'Play Hard',u'Love Never Felt So Good',u'Right Here',u'Shots',u'Set Fire To The Rain',u'Latch',u'We Are Tonight',u'Beautiful',u'River Bank']:
			continue

		url = base_url + song + '+' + artist.replace(' ', '+')
		headers = {'User-Agent': user_agent}
		response = requests.get(url, headers=headers)
		if response.status_code != 404:
			print "Here"
			html = response.text.encode('utf-8')
			soup = BeautifulSoup(html)
			print html
			link = soup.find('li', {'class': 'search_result'})
			if link is not None:
				link = link.find('a', href=True).get('href')
			else:
				not_found += [song]
				continue
			print "LINK: " + str(link)

			response = requests.get(link, headers=headers)
			if response.status_code != 404:
				print "Here 2"
				html = response.text.encode('utf-8')
				soup = BeautifulSoup(html)
				section = soup.find('div', {'class': 'lyrics'})
				tokens = section.findAll(text=True)
				print "TOKENS"
				print tokens
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
				print lyrics
				writer = csv.writer(open(os.path.join('data/' + song.replace('/','') + '-' + artist + '.csv'), 'wb'), delimiter=';', quoting=csv.QUOTE_NONE, escapechar=",")
				lyrics = [unicodedata.normalize('NFKD', lyric.replace("\r", " ").replace("\n", " ").replace("\t", '').replace("\"", "").replace(u"\u2018", "").replace(u"\u2019", "").replace(u'\u2014', ' - ').replace(u'\u201c', '').replace(u'\xfc','').replace(u'\u201d', '').replace(u'\xe9', '').replace(u'\u2013', '').replace(u'\xdc','')).encode('ascii','ignore') for lyric in lyrics]
				writer.writerow(lyrics)
writer = csv.writer(open(os.path.join('data/' + 'not_found.csv'), 'wb'), quoting=csv.QUOTE_NONE, escapechar=",")
writer.writerow(not_found)
