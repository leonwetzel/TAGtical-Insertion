#!/usr/bin/env python3
import os
import sys

import spacy

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = f"pipeline/model/"


def main():
    """

    Returns
    -------

    """
    print(os.getcwd())
    print(f"Loading model from {os.getcwd()}/{MODEL_PATH}")
    nlp = spacy.load(f"{os.getcwd()}/{MODEL_PATH}")

    for line in sys.stdin:
        prediction = nlp(line)

        for entity in prediction.ents:
            print("{}\t{}".format(entity, entity.label_), '\n')


if __name__ == '__main__':
    main()
