import sys
import re
import csv

if len(sys.argv) < 2:
	print """USAGE: python splitSentiment.py [input_file]"""
	sys.exit()

pos_file = open("positive.csv", 'w')
neg_file = open("negative.csv", 'w')
test_file = open("testset.csv", 'w')
emo_count_file = open("emojiCount.csv", 'w')

pos_out = csv.writer(pos_file, delimiter = '\t', quotechar = '', escapechar = '\\', quoting = csv.QUOTE_NONE)
neg_out = csv.writer(neg_file, delimiter = '\t', quotechar = '', escapechar = '\\', quoting = csv.QUOTE_NONE)
test_out = csv.writer(test_file, delimiter = '\t', quotechar = '', escapechar = '\\', quoting = csv.QUOTE_NONE)
emo_count_out = csv.writer(emo_count_file, delimiter = '\t', quotechar = '', escapechar = '\\', quoting = csv.QUOTE_NONE)

pos_count = 0
neg_count = 0
test_count = 0

sad = '[:=]-?\('
happy = '[:=]-?\)'


for index in range(1, len(sys.argv)):
	doc = open(sys.argv[index], 'rU')
	in_file = csv.reader(doc, delimiter = ',')
	line_idx = 1

	for row in in_file:
		if (line_idx ==1):
			row.extend(["positive_emo_count", "negative_emo_count", "net_emo_count"])
			emo_count_out.writerow(row)
			line_idx += 1
			continue

		if len(row) != 5:
			print "Skipping: malformatted line: %i" %line_idx
			line_ix += 1
			continue

		text = row[1]
		emo_neg_count = len(re.findall(sad, text))
		emo_pos_count = len(re.findall(happy, text))
		row.extend([emo_neg_count, emo_pos_count, emo_pos_count - emo_neg_count])
		if re.search(sad, text) != None and re.search(happy, text) == None:
			neg_out.writerow(row)
			neg_count += 1
		elif re.search(happy, text) != None and re.search(sad, text) == None:
			pos_out.writerow(row)
			pos_count += 1
		else:
			test_out.writerow(row)
			test_count += 1
		emo_count_out.writerow(row)
		line_idx += 1
	doc.close()


neg_file.close()
pos_file.close()
test_file.close()
emo_count_file.close()

print "Splitting finished. Positive: " + str(pos_count) + " Negative:" + str(neg_count) + " Test:" + str(test_count)


























