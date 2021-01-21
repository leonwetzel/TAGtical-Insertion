#!/usr/bin/env python3
"""
baseline.py

This script performs the baseline prediction and evaluation for semantic tagging.
It predicts the label NIL for the last token in the sentence and CON for every other token.
These are the most occurring labels in the dataset.
"""

#all kinds of imports
from __future__ import unicode_literals, print_function

import os
import sys
#insert the correct path to the preprocessing folder, allowing the program to download the files from extraction.py
#sys.path.insert(0, '../preprocessing/')
#for some reason general paths don't work right now on Marjolein's/my virtual box, thus other path here :)
#comment away the path you don't need
sys.path.insert(0, "../preprocessing/")

import re
import random
import warnings
from pathlib import Path

import plac
import spacy
from spacy.util import minibatch, compounding
import sklearn
from sklearn.metrics import f1_score

#imports from extraction.py
import extraction
from extraction import to_spacy_format
from extraction import extract_from_conll
from extraction import get_coordinates

def main():
	#load the created model
	#output_dir = 'model/'
	output_dir = "model/"
	
	#not necessary I think
	print("Loading from", output_dir)
	
	#load the data you want to test on
	nlp = spacy.load(output_dir)
	#corpus = extract_from_conll("../../data/dev.conll")
	corpus = extract_from_conll("../../data/test.conll")
	data = to_spacy_format(corpus)
	
	#create a list that will keep track of the original tags and predicted tags
	y_given = []
	y_predicted = []
	# Counter to track sentence number
	cnt = 0
	
	for text, _ in data:
		real = data[cnt][1].get('entities')
		for item in real:
			y_given.append(item[2])
			y_predicted.append("CON")

		y_predicted[-1] = "NIL"

		cnt += 1

	print(len(y_given), len(y_predicted))
	print(f1_score(y_given, y_predicted, average='micro'))

if __name__ == '__main__':
	main()
