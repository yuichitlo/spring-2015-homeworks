import os
import csv
import unicodedata

for i in os.listdir(os.getcwd()):
	if i.startswith("not_found"): 
		continue
	else:
		f = open(i)
		raw = f.read().split(';')

		count = 0
		sections = {}
		in_section = False
		cur_tag = ''
		output = []
		while count < len(raw)-1:
			if '[' in raw[count]:
				tag = raw[count].replace('[','').replace(']','').split(':')[0]
				if tag not in sections and raw[count+1] != '':
					sections[tag] = ''
					cur_tag = tag
					in_section = True
				else:
					output += [sections[tag]]
				count += 1
			else:
				if in_section:
					sections[cur_tag] += raw[count]
					if '[' in raw[count+1]:
						in_section = False
						output += [sections[tag]]
				else:
					output += [raw[count]]
				count += 1
		f.close()
		print output
		writer = csv.writer(open(i, 'wb'), delimiter=';', quoting=csv.QUOTE_NONE, escapechar=",")
		writer.writerow(output)
		break

