#!/usr/bin/env python3
"""
evaluation.py

This script performs the evaluation on out Spacy Semantic Label Tagger.
It outputs multiple text files:
- evaluation.txt: Contains the overall f1 score, as well as the incorrectly predicted sentences for development and error analysis.
- label_scores.txt: Contains the f1 score and the amnount of instances per label in the dataset.
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
#sys.path.insert(0, '/home/tux/Computational-Semantics/tagtical_insertion/preprocessing/')

import re
import random
import warnings
from pathlib import Path

import plac
import spacy
from spacy.util import minibatch, compounding
import sklearn
from sklearn.metrics import classification_report, f1_score

#imports from extraction.py
import extraction
from extraction import to_spacy_format
from extraction import extract_from_conll
from extraction import get_coordinates

def uneven_tokens(pred_entities, gold_entities):
	"""
	This function is called whenever the amount of tokens in the pred and gold data are uneven.
	It adds an articifal label --- to whichever data is shorter until the two are of an even length.
	"""
	pred_labels = []
	gold_labels = []
	for entity in pred_entities:
		pred_labels.append(entity.label_)

	for item in gold_entities:
		gold_labels.append(item[2])

	if len(pred_labels) > len(gold_labels):
		while len(pred_labels) > len(gold_labels):
			gold_labels.append('---')

	else:
		while len(gold_labels) > len(pred_labels):
			pred_labels.append('---')

	return pred_labels, gold_labels


def label_scores(y_given, y_predicted):
	"""
	This function calculates the f1 score per label in the data.
	It sorts and writes the scores in a .txt file.
	"""
	scores_dict = classification_report(y_given,y_predicted, output_dict=True)

	f1_dict = {}
	for key in scores_dict:
		if len(key) == 3:
			f1_dict[key] = scores_dict[key]

	sorted_scores = dict(sorted(f1_dict.items(), key=lambda item: (item[1]['f1-score'], item[1]['support']), reverse=True))

	f2 = open("label_scores.txt", "w+")

	f2.write("label\tf1-score\t# of instances\n")
	for key in sorted_scores:
		f2.write(key + "\t" + str(round(sorted_scores[key]['f1-score'], 4)) + "\t" + str(sorted_scores[key]['support']) + "\n")

	f2.close()

def main():
	#load the created model
	#output_dir = 'model/'
	output_dir = "model/"
	#output_dir = '/home/tux/Computational-Semantics/tagtical_insertion/pipeline/model/'
	
	#not necessary I think
	print("Loading from", output_dir)
	
	#load the data you want to test on
	nlp = spacy.load(output_dir)
	#corpus = extract_from_conll("../../data/dev.conll")
	corpus = extract_from_conll("../../data/dev.conll")
	#corpus = extract_from_conll("/home/tux/Computational-Semantics/data/train.conll")
	data = to_spacy_format(corpus)
	
	#create a list that will keep track of the original tags and predicted tags
	y_given = []
	y_predicted = []
	
	#some counters, cnt keeps track of total number of sentences, wrong_token keeps track of sentences
	#with incorrect number of predicted tokens and no_entities keeps track of number of sentences without any tokens
	cnt = 0
	wrong_token = 0
	no_entities = 0
	
	list_of_empty_sentences = []
	list_of_sentences_with_wrong_tokens = []
	list_of_sentences_with_incorrect_tags = []
	incorrect_tags_original = []
	incorrect_tags_predicted = []
	
	x_counter = 0
	
	for text, _ in data:
		prediction = nlp(text)
		real = data[cnt][1].get('entities')
		if len(real) == 0:
			list_of_empty_sentences.append(text)
			no_entities +=1
		elif len(prediction.ents) == len(real):
			for item in real:
				y_given.append(item[2])
			for ent in prediction.ents:
				y_predicted.append(ent.label_)
			
			for i in range(len(prediction.ents)):
				x = prediction.ents[i]
				if real[i][2] != x.label_:
					x_counter +=1
					list_of_sentences_with_incorrect_tags.append(text)
					minilist = []
					for item in real:
						minilist.append(item[2])
					incorrect_tags_original.append(minilist)
					minilist = []
					for ent in prediction.ents:
						minilist.append(ent.label_)
					incorrect_tags_predicted.append(minilist)
					break
		else:
			wrong_token += 1
			list_of_sentences_with_wrong_tokens.append(text)
			pred_labels, gold_labels = uneven_tokens(prediction.ents, real)
			for label in pred_labels:
				y_predicted.append(label)
			for label in gold_labels:
				y_given.append(label)
			
		cnt +=1

	correct = cnt - wrong_token - no_entities
	with open('evaluation.txt', 'w') as f:
		f.write("We evaluated the model on the file dev.conll")
		f.write("\n")
		f.write("This file consists of " + str(cnt) + " sentences.")
		f.write("\n")
		f.write("Out of these " + str(cnt) + " sentences, " + str(correct) + " sentences are correctly tokenized")
		f.write("\n")
		f.write("\n")
		
		if len(list_of_empty_sentences) > 0:
			f.write(str(no_entities) + " sentence(s) are not tokenized at all, and return an empty string, these include the following sentence(s):")
			f.write("\n")
			for sentence in list_of_empty_sentences:
				f.write(sentence)
				f.write("\n")
		
		f.write("\n")
		
		if len(list_of_sentences_with_wrong_tokens) > 0:
			f.write(str(wrong_token) + " sentence(s) have an incorrect number of tokens. These include the following sentence(s):")
			f.write("\n")
			for sentence in list_of_sentences_with_wrong_tokens:
				f.write(sentence)
				f.write("\n")			
		f.write("\n")
		
		f.write("We evaluated the performance of the tagger on the set of sentences that is correctly tokenized.")
		f.write("\n")
		f.write("The F-Score returns the following score:" + str(f1_score(y_given,y_predicted, average='micro')))
		f.write("\n")
		
		f.write("In total " + str(x_counter) + " sentences with incorrect tags were found. These were found in the following sentences:")
		f.write("\n")
		for i in range(len(list_of_sentences_with_incorrect_tags)):
			f.write("Sentence: " + list_of_sentences_with_incorrect_tags[i])
			f.write("\n")
			f.write("Correct tags: " + str(incorrect_tags_original[i]))
			f.write("\n")
			f.write("Predicted tags: " + str(incorrect_tags_predicted[i]))
			f.write("\n")
			f.write("\n")					
		

	label_scores(y_given, y_predicted)

	#print(cnt)
	
	#print(wrong_token)
	#print(list_of_sentences_with_wrong_tokens)
	
	#print(no_entities)
	#print(list_of_empty_sentences)
	
	#print(len(y_given))
	#print(len(y_predicted))
	#print(list_of_sentences_with_incorrect_tags[1])
	#print(incorrect_tags_original[1])
	#print(incorrect_tags_predicted[1])

	#from sklearn.metrics import f1_score
	#print(f1_score(y_given,y_predicted, average='micro'))
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
