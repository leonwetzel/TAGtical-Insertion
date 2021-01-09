#!/usr/bin/env python3
import pickle
import re


def extract_from_conll(filename):
    """Extract relevant data from the .conll files.
    Also converts the data to a spaCy-friendly format.

    Parameters
    ----------
    filename : str
        Name of the .conll file.

    Returns
    -------
    corpus : dict
        Converted data in spaCy-friendly format.
    """
    corpus = {}
    with open(filename, "r", encoding='utf-8') as F:
        lines = F.readlines()

    tokens, semantic_tags = [], []
    sentence_id = None

    for line in lines:
        # start of document
        if line.startswith('# newdoc id'):
            sentence_id = line.split(" ")[-1].strip()
        # end of document
        elif line.isspace():
            if tokens and semantic_tags:
                sentence = " ".join(tokens)
                print(sentence)

                entities = get_coordinates(tokens, semantic_tags,
                                           sentence)

                corpus[sentence_id] = {
                    "sentence": sentence,
                    "tokens": tokens.copy(),
                    "semantic_tags": semantic_tags.copy(),
                    "entities": entities.copy()
                }
                tokens.clear()
                semantic_tags.clear()
        # within document
        else:
            token, _, sem_tag, _, _, _ = line.split()
            tokens.append(token)
            semantic_tags.append(sem_tag)

    return corpus


def get_coordinates(tokens, tags, sentence):
    """Get coordinates of a given token in a sentence.

    Returns the coordinates in a spaCy-friendly format,
    along with the relevant semantic tag.

    Parameters
    ----------
    token : str
        Token that is present in the given sentence.
    tag : str
        Semantic tag that is related to the given token.
    sentence : str
        Sentence in which the given token occurs.

    Returns
    -------

    """
    # {"entities": [(0, 4, "ORG")]}
    training_data = []
    counter = 0
    pattern = rf"(\b(\w+|\d+)\b)|([.,\/#@?!$%\^&\*;:=\-_`()])"
    amount_of_matches = len([*re.finditer(pattern, sentence)])

    for m in re.finditer(pattern, sentence):
        if len(tokens) == amount_of_matches:
            token = (m.start(), m.end(), tags[counter])
            counter += 1
            training_data.append(token)
    return training_data


def to_spacy_format(corpus):
    """Gets the relevant information from the corpus
    for use with spaCy.

    Parameters
    ----------
    corpus : dict
        Object that contains sentences and the tags, along with their
        respective coordinates.

    Returns
    -------

    """
    data = []
    for _, sentence in corpus.items():
        entry = (sentence['sentence'],
                 {"entities": sentence['entities']})
        data.append(entry)
    return data


def store(corpus, filename):
    """

    Parameters
    ----------
    corpus
    filename

    Returns
    -------

    """
    with open(filename, "wb") as F:
        pickle.dump(corpus, F)
