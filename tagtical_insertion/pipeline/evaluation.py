#!/usr/bin/env python3
from __future__ import unicode_literals, print_function

import os
import sys
sys.path.insert(0, '../preprocessing/')
import re
import random
import warnings
from pathlib import Path

import plac
import spacy
from spacy.util import minibatch, compounding
import sklearn

import extraction
from extraction import to_spacy_format
from extraction import extract_from_conll
from extraction import get_coordinates

def main():
	output_dir = 'model/'
	print("Loading from", output_dir)
	nlp = spacy.load(output_dir)
	corpus = extract_from_conll("../../data/dev.conll")
	train_data = to_spacy_format(corpus)

	y_given = []
	y_predicted = []
	cnt = 0
	correct_token = 0
	no_entities = 0
	for text, _ in train_data:
		prediction = nlp(text)
		real = train_data[cnt][1].get('entities')
		if len(real) == 0:
			no_entities +=1
		elif len(prediction.ents) == len(real):
			correct_token += 1
			for item in real:
				y_given.append(item[2])
			for ent in prediction.ents:
				y_predicted.append(ent.label_)
			#y_predicted.append(prediction
		cnt +=1

	print(len(y_given))
	print(len(y_predicted))

	from sklearn.metrics import f1_score
	print(f1_score(y_given,y_predicted, average='micro'))
	#for item in real:
	#	print(item[2])
	#print(real[1])
	#print(y_given)
	#print(correct_token)
	#print(cnt)
	#print(no_entities)
		
	#print(train_data)
	#print(train_data[2])
	#for i in range(len(train_data)):
	#	print(train_data[i][1])

	#x = train_data[6][1]
	#x = x.get('entities')
	#print(x)
	#print(len(x))

	#print(train_data[2])
	#text = 'She likes short skirts.'
	#doc=nlp2(text)
	#for ent in doc.ents:
	#	print(ent.label_)
	#print("Entities", [(ent.text, ent.label_) for ent in doc.ents])
	#print("Tokens", [(t.text, t.ent_type_, t.ent_iob) for t in doc])

	#text gives the full sentences like "Tom ripped out the page"
	#for text, _ in train_data:
		#doc = nlp2(text)
		#print("Entities", [(ent.text, ent.label_) for ent in doc.ents])
		#print("Tokens", [(t.text, t.ent_type_, t.ent_iob) for t in doc])

if __name__ == '__main__':
	main()