import os
import datetime
import csv

def argsort(seq):
    return sorted(range(len(seq)), key = seq.__getitem__)

f = open('chart-info-mod.csv')
output = []
raw = f.read().split('\n')
for line in raw:
	tokens = line.replace('\n', '').replace('\r','').split(',')
	if tokens[0] == 'Song':
		tokens = tokens[:4] + ['duration', 'peak', 'peak_week'] + tokens[4:]
		output += [tokens]
	else:
		weeks = [int(week) for week in tokens[4:]]
		week_sort = argsort(weeks)
		peak = min(weeks)
		duration = len(weeks)
		peak_week = datetime.datetime.strptime(tokens[3], "%Y-%m-%d") + datetime.timedelta(7*(week_sort[0]))
		tokens = tokens[:4] + [duration, peak, peak_week.strftime("%Y-%m-%d")] + weeks
		output += [tokens]

print output
f.close()

writer = csv.writer(open(os.path.join('chart-info-addt-2.csv'), 'wb'), quoting=csv.QUOTE_NONE, escapechar=",")
for row in output:
	writer.writerow(row)

