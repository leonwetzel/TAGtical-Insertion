#!/usr/bin/env python3
"""
find_problematic_sentences.py

This script finds every sentence that contains mistakes in tokenization or prediction.
This is used for development and error analysis.
"""

from __future__ import unicode_literals, print_function

import os
import sys
sys.path.insert(0, '/home/tux/Computational-Semantics/tagtical_insertion/preprocessing/')
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
	nlp2 = spacy.load(output_dir)
	corpus = extract_from_conll("../../data/test.conll")
	train_data = to_spacy_format(corpus)

	sentences = []
	count = 0
	for text in train_data:
		number = train_data[count][1].get('entities')
		if len(number) == 0:
			sentences.append(text[0])
		count +=1
	print(sentences)
	with open('sentences.txt', 'w') as f:
		for item in sentences:
			f.write(item)
			f.write("\n")

if __name__ == '__main__':
	main()

