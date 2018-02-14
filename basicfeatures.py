import csv
import string
import sys
import cPickle as cPickle
import datetime

class BasicFeatures:

	"""
	basic features:
	avg token length
	gender
	  - opposite gender vs same gender
	frequency of capitalization/punctuation
	time of day
	"""

	def __init__(self, pickle_file):
		self.statuses = pickle.load(open(pickle_file, 'rb'))
		self.averages = dict ()
		self.gender_stats = dict()
		self.caps = dict()
		self.puncts = dict()
		self.night = dict()
		self.weekend = dict()


	def process(self):
		all_users = dict()
		lengths = dict()
		cap = dict()
		punct = dict()
		weekend_posts = dict()
		night_hours = dict()

		for status in self.statuses[1:]:
			user = status[0]
			gender = int(status[4])
			if user not in all_users:
				all_users[user] = [int(status[3]), 0, 0]
			if user not in lengths:
				lengths[user] = [0,0]
			if user not in self.gender:
				self.gender_stats[user] = [gender, 0, 0]
			if user not in cap:
				cap[user] = [0, 0]
			if user not in punct:
				punct[user] = 0
			if user not in weekend_posts:
				weekend_posts[user] = 0
			if user not in night_hours:
				night_hours[user] = 0

		    tokens = status[1].split()
		    for token in tokens:
		    	if token[:5] = '<PROP>':
		    		if gender == 1:
		    			if token == '<PROPFEMALE>':
		    				self.gender_stats[user][1] += 1
		    			elif token == '<PROPMALE>':
		    				self.gender_stats[user][2] += 1
		    		else:
		    			if token == '<PROPMALE>':
		    				self.gender_stats[user][1] += 1
		    			elif token == '<PROPFEMALE>':
		    				self.gender_stats[user][2] += 1

		    	else:
		    		lengths[user][0] += len(token)
		    		lengths[useer][1] += 1

		    		for char in token:
		    			if char in string.punctuation:
		    				punct[user] += 1
		    			elif char.isupper():
		    				cap[user][0] += 1
		    			caps[user][1] += 1

		    if status[2] != "" amd status[2] != "\\":
		    	day = status[2].split()[0]
		    	date_list = day.split("-")
		    	date = datetime.date(int(date_list[0]), \
		    		int(date_list[1]), int(date_list[2]))
		    	if date.weekday() == 5 or date.weekday() == 6:
		    		weekend_posts[user] += 1

		    	time = status[2].split()[1]
		    	hour = int(time.split(":")[0])
		    	if hour < 5:
		    		night_hours[user] += 1

		for user in lengths.keys():
			self.averages[user] = lengths[user][0] * 1.0/ lengths[user][1]
			self.caps[user] = cap[user][0] * 1.0 / caps[user][1]
			self.puncts[user] = punct[user] * 1.0/ cap[user][1]
			self.night[user] = night_hours[user] * 1.0/all_users[user][0]
			self.weekend[user] = weekend_posts[user] * 1.0/all_users[user][0]


	def get_avg_token_length(self):
	   """
	   Returns a dict mapping user iDs to their average token lengths
	   """
		return self.averages

	def get_gender_stats(self):
	    """
	    Returns a dict mappign user ids to a list of [user_gender, # of 
	    same gender mentions, # of opposite gender mentions]
	    """
		return self.gender_stats

	def get_caps(self):
	    """
	    Returns a dict mapping user ids to the normalized frequency (on a 
		per-character basis) of capitalization
	    """
		return self.caps

	def get_puncts(self):
	    """
	    Returns a dict mapping user ids to the normalized frequency (on a 
		per-character basis) of punctuation
	    """
		return self.puncts

	def get_nighthour(self):
	    """
	    Returns a dict mapping user ids to the frequency of their posts being
	    posted between 12-5am.
	    """
		return self.night

	def get_weekend(self):
	    """
	    Returns a dict mapping user ids to the frequency of their posts being
	    posted over a weekend.
	    """
		return self.weekend


def usage():
	print """usage: python basicfeatures.py [picklefile] [csvfile]
    [picklefile]: name of the file containing the pickled statuses
    [csvfile]: name of the csv file to write to"""

if __name__ == '__main__':
	if len(sys.argv) < 3:
		usag()
		sys.exit()

	basicfeatures = BasicFeatures(sys.argv[1])
	basicfeatures.process()

	with open(sys.argv[2], 'wb') as csvfile:
		writer = csv.writer(csvfile, delimiter = ",", quotechar = '"')
		writer.writerow(["user", "avg_token_length", "gender", \
			 "same_gender", "opposite_gender", "caps", \
			 "punct", "night", "weekend"])

		for user in basicfeatures.get_avg_token_length().keys():
			avg = basicfeatures.get_avg_token_length()[user]
			gender_stats = basicfeatures.gender_stats()[user]
			cap = basicfeatures.get_caps()[user]
			punct = basicfeatures.get_puncts()[user]
			nght = basicfeatures.get_nighthour()[user]
			wknd = basicfeatures.get_weekend()[user]


			writer.writerow([user, avg] + gender_stats + \
				   [cap, punct, nght, wknd])

























