#!/usr/bin/env python3
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
    with open(filename, "r") as F:
        lines = F.readlines()

    tokens, lemmas, semantic_tags, entities = [], [], [], []
    sentence_id = None

    for line in lines:
        if line.startswith('# newdoc id'):
            sentence_id = line.split(" ")[-1].strip()
        elif line.isspace():
            if tokens and semantic_tags:
                sentence = " ".join(tokens)
                sentence = re.sub(
                    r"\s([,?.!'`](?:\s*|$))", r'\1', sentence
                )
                entities = [get_coordinates(token, tag, sentence) for
                            token, tag in zip(tokens, semantic_tags)]

                corpus[sentence_id] = {
                    "sentence": sentence,
                    "tokens": tokens.copy(),
                    "lemmas": lemmas.copy(),
                    "semantic_tags": semantic_tags.copy(),
                    "entities": entities.copy()
                }
                tokens.clear()
                lemmas.clear()
                semantic_tags.clear()
                entities.clear()
        else:
            # TODO figure out which info to use
            token, lemma, sem_tag, ccg_tag, sense, themes = line.split()
            tokens.append(token)
            lemmas.append(lemma)
            semantic_tags.append(sem_tag)

    return corpus


def get_coordinates(token, tag, sentence):
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
    start_index = sentence.find(token)
    end_index = start_index + len(token)  # if the start_index is not -1
    return start_index, end_index, tag


def to_spacy_training_format(corpus):
    """

    Parameters
    ----------
    corpus : dict

    Returns
    -------

    """
    training_data = []
    for _, sentence in corpus.items():
        entry = (sentence['sentence'],
                 {"entities": sentence['entities']})
        training_data.append(entry)
    return training_data
