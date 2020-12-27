#!/usr/bin/env python3

def extract_from_conll(filename):
    """Extract relevant data from the .conll files.

    Parameters
    ----------
    filename

    Returns
    -------

    """
    corpus = {}
    with open(filename, "r") as F:
        lines = F.readlines()

    tokens, semantic_tags = [], []
    sentence_id = None

    for line in lines:
        if line.startswith('# newdoc id'):
            sentence_id = line.split(" ")[-1]
        elif line.isspace():
            if tokens and semantic_tags:
                corpus[sentence_id] = {
                    "sentence": " ".join(tokens),
                    "tokens": tokens.copy(),
                    "semantic_tags": semantic_tags.copy()
                }
                tokens.clear()
                semantic_tags.clear()
        else:
            token, _, sem_tag, ccg_tag, sense, _ = line.split()
            tokens.append(token)
            semantic_tags.append(sem_tag)

    return corpus
