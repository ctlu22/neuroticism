The sentiment classifier takes facebook status (test_unfiltered.csv) as input and predicts 
a sentiment score ranging from 1 (fully positive) to -1 (fully negative) for each status (saved as sentiment.csv).

You can run

python classify.py test_nonull.csv sentiment.csv

to see how the sentiment scores are predicted. (sentiment.csv will be overwritten and the program took about 15-20 minutes to run on my computer)

Or if you prefer to start from scratch (assuming only the python scripts and test_unfiltered.csv are kept in the folder), here’s a roadmap:

Step 1: run 

python removeNull.py test_unfiltered.csv test_nonull.csv

to remove null bytes from test_unfiltered.csv.

Step 2: run

python splitSentiment.py test_nonull.csv

to split the data to “positive.csv” (status with happy emoticons only and assign sentiment score of 1), “negative.csv” (status with sad emoticons only and assign sentiment score of -1) and testset.csv (not used).

Step 3: Comment out the function “LoadSentimentClassifier” and uncomment the last line (“TrainSentimentClassifier()”) in “buildclassifier.py” and run

python buildpclassifier.py 

This step trains and saves a Naive Bayes Classifier (using words as features) that predicts sentiment score of facebook status. “positive.csv” and “negative.csv” are used as training/test set.

Step 4: Comment out (“TrainSentimentClassifier()”) and uncomment the function “LoadSentimentClassifier” in “buildclassifier.py” and run

python classify.py test_nonull.csv sentiment.csv,

which computes a sentiment score for each status and the results are saved in sentiment.csv.


