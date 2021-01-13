#!/usr/bin/env python3
"""
manual_sentences.py

This script allows the user to type in their own sentences.
The typed words are then annotated with semantic tags.
"""
from __future__ import unicode_literals, print_function

import os
import sys
sys.path.insert(0, '../preprocessing/')
from pathlib import Path
import spacy

def main():
	output_dir = 'model/'
	nlp = spacy.load(output_dir)

	while True:
		text = input("Please type in a sentence (ENTER to stop): ")
		if text == "":
			break
		prediction = nlp(text)
		
		for ent in prediction.ents:
			print("{}\t{}".format(ent, ent.label_))
		print()

if __name__ == '__main__':
	main()