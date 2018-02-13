import sys
import csv
import buildclassifier


if len(sys.argv) < 3:
  print """USAGE: python classifier.py [input_filename] [output_filename] 
This script computes sentiment scores ranging from -1 (fully negative) to 1 (fully positive) for facebook status.
To run this script, you'll need:
--The files 'classifier.pickle','features.pickle', and 'time_limit.py' 
--The python package 'nltk' and nltk stopwords corpus installed 
  sys.exit()"""


buildclassifier.LoadSentimentClassifier(feature_file = "features.pickle", classifier_file = "classifier.pickle")

print "Started to read and classify status..."

inFilename = sys.argv[1]
outFilename = sys.argv[2]
f = open(sys.argv[1], 'rU')
g = open(sys.argv[2], 'w')
fi = csv.reader(f, delimiter = ',')
fo = csv.writer(g, delimiter= ',')

line_idx = 1

for row in fi:
  if line_idx == 1:
    headers = ["userid", "message", "updated_time", "n_status", "gender", "sentiment"]
    fo.writerow(headers)
  
  if (len(row) != 5):
    print "Skipped malformatted line_idx: %i." % line_idx
    line_idx += 1
    continue

  text = row[1]
  score = buildclassifier.ClassifySentiment(text)
  row.append(score)
  fo.writerow(row)

  line_idx += 1
  if line_idx % 500 == 0:
    print(line_idx)

f.close()
g.close()

print "fiished Reading and Classifying status."

