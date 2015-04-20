import os
import datetime
import csv

f = open('chart-info-mod.csv')
output = []
for line in f:
	tokens = line.replace('\n', '').replace('\r','').split(',')
	if tokens[0] == 'Song':
		tokens = tokens[:4] + ['duration', 'peak', 'peak_week'] + tokens[4:]
		output += [tokens]
	else:
		weeks = tokens[4:]
		peak = max(weeks)
		duration = len(weeks)
		peak_week = datetime.datetime.strptime(tokens[3], "%Y-%m-%d") + datetime.timedelta(7*(duration-1))
		tokens = tokens[:4] + [duration, peak.replace('\r',''), peak_week.strftime("%Y-%m-%d")] + weeks
		output += [tokens]

print output
f.close()

writer = csv.writer(open(os.path.join('chart-info-addt.csv'), 'wb'), quoting=csv.QUOTE_NONE, escapechar=",")
for row in output:
	writer.writerow(row)

