"""
Final Project for EECS 595
Implement word embedding method, part-of-speech pattern method on calculating sentence similarity.

@ chameleon_johson.py
@ johson
@ Nov 29, 2018
"""

import sys
import numpy as np
import pickle
from glob import glob
import gensim.downloader as api
from gensim.test.utils import common_texts, get_tmpfile


DEBUG = 1
TESTFILE = 7
TESTLINE = 3000


def read_clean_data(fname):
	"Read in clean data. Return object data."
	with open(fname, 'rb') as f:
		obj = pickle.load(f)

	return obj


def split_conversation(obj):
	"Split conversation by each speaker. Return splited conversation data."
	# Store first line in conversation
	prev_spk = obj[0][0]
	conv = [obj[0]]

	# Start at the second line, check if the speaker does not change
	for line in obj[1:]:
		curr_spk = line[0]
		if curr_spk == prev_spk:
			conv[-1][-1] += line[-1]
		else:
			conv.append(line)
			prev_spk = curr_spk

	return conv


def calculate_word2vec(conv, model, stopwords):
	"""
	Calculate sentence similarity based on word embeddings.
	Return top 3 word similarity scores on each pair of sentence.
	"""
	n = len(conv)
	similar_score_top3_list = []

	for i in range(n - 1):
		senten1 = conv[i][1]
		senten2 = conv[i+1][1]
		senten_vec1 = []
		senten_vec2 = []

		# Calculate word2vec
		for word in senten1:
			if word not in stopwords:
				try:
					senten_vec1.append(model[word])
				except Exception as e:
					e = 0
		for word in senten2:
			if word not in stopwords:
				try:
					senten_vec2.append(model[word])
				except Exception as e:
					e = 0

		# Calculate similarity score
		similar_score = []
		for vec1 in senten_vec1:
			for vec2 in senten_vec2:
				similar_score.append(np.dot(vec1, vec2) / (np.linalg.norm(vec1) * np.linalg.norm(vec2)))
		similar_score_top3 = sorted(similar_score, reverse=True)[:3]
		if (len(similar_score_top3) > 0):
			similar_score_top3_list.append(similar_score_top3)

	return similar_score_top3_list


def main():
	"Main function."
	clean_data_files = glob('TRN_output/*.pkl')
	if DEBUG:
		clean_data_files = clean_data_files[:TESTFILE]

	# Load pretrained gensim model
	model = api.load("glove-twitter-25")

	# Read stop words
	with open('stopwords', 'r') as f:
		lines = f.readlines()
	stopwords = [line.rstrip('\n') for line in lines]

	# Read clean data
	for fname in clean_data_files:
		obj = read_clean_data(fname)

		if len(obj) == 0:
			continue

		if DEBUG:
			obj = obj[:TESTLINE]

		# Get conversation
		conv = split_conversation(obj)

		# Calculate word2vec similarity
		similar_score_top3_list = calculate_word2vec(conv, model, stopwords)
		print(np.sum(np.sum(similar_score_top3_list)))



if __name__ == '__main__':
	main()

