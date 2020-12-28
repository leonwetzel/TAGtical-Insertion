# Computational Semantics
Contains all code and documentation of the final project of the course
 Computational Semantics, taught at the University of Groningen.
 
The main purpose of APPLICATION_NAME is to tag sentences using
 semantic tags. These semantic tags are described in detail in [Abzianidze and Bos (2017)](https://www.aclweb.org/anthology/W17-6901.pdf).
 The data used in this application originates from the Parallel Meaning
  Bank, also known as the PMB ([Abzianidze et al., 2017](https://www.aclweb.org/anthology/E17-2039.pdf)).

## Getting started

### Installing additional packages

As the scripts in this repository may rely on external functionality,
it might be wise to install the required software beforehand. Open your
 favourite command line interface, create a new [`virtualenv`](
 https://docs.python.org/3/library/venv.html) (or
 install the required packages system-wide if that is your preference 😀)
 and enter the following line.
 
 ```shell script
pip install -r requirements.txt
```

When you have installed the required packages, you are ready to further
explore the functionalities of APPLICATION_NAME!


### Obtaining the PMB data

Before you can train and/or test the tagger, you need to download the
 data from the [Parallel Meaning Bank](https://pmb.let.rug.nl/). We use
  the .conll files from [Rik van Noord's](http://www.rikvannoord.nl/)
   [GitHub repository](https://github.com/RikVN/DRS_parsing), as these
    files are already preprocessed and standardised for easier use
     ([Abzianidze et al., 2017](https://www.aclweb.org/anthology/E17-2039.pdf)).
    
You can easily download these files from the repository by entering the
following lines of code in your Python command line interface.

```python
>>> from src.pipeline.retrieval import DownloadManager
>>> DownloadManager.download()
```

The files will pop up in the `data` directory. Note that this directory
will be created automatically if it was not present before the download.

### Preparing for training

We cannot directly feed the data from the .conll files into the training
script for the semantic tagger. Using the functionality in
the package `src.preprocessing.extraction`, we convert the data
to the format that suits spaCy. In the code sample below, you can see 
how you can perform the conversion from your Python command line interface.

```python
>>> from src.preprocessing.extraction import extract_from_conll, to_spacy_training_format
>>> corpus = extract_from_conll("data/train.conll")
>>> training_data = to_spacy_training_format(corpus)
```

We also added functionality to store the training data in a pickle,
so you can quickly re-use the data at a later moment.

```python
>>> from src.preprocessing.extraction import store
>>> store(training_data, "data/training_data.pickle")
```

## Training the tagger

As mentioned in the last subsection, we use spaCy for the construction
of our semantic tagger [(Montani et al., 2020)](https://doi.org/10.5281/zenodo.1212303). spaCy offers functionality to create custom NER-like taggers.
We can apply the same techniques to perform semantic tagging, using the
tags mentioned in [Abzianidze and Bos (2017)](https://www.aclweb.org/anthology/W17-6901.pdf)
as the labels for the tokens.

## References

Lasha Abzianidze, Johan Bos (2017): Towards Universal Semantic Tagging. Proceedings of the 12th International Conference on Computational Semantics (IWCS 2017) -- Short Papers, pp 1–6, Montpellier, France.

Lasha Abzianidze, Johannes Bjerva, Kilian Evang, Hessel Haagsma, Rik van Noord, Pierre Ludmann, Duc-Duy Nguyen, Johan Bos (2017): The Parallel Meaning Bank: Towards a Multilingual Corpus of Translations Annotated with Compositional Meaning Representations. Proceedings of the 15th Conference of the European Chapter of the Association for Computational Linguistics (EACL), pp 242–247, Valencia, Spain.

Abzianidze, L., Bjerva, J., Evang, K., Haagsma, H., van Noord, R., Ludmann, P., Nguyen, D. & Bos, J. The Parallel Meaning Bank: Towards a Multilingual Corpus of Translations Annotated with Compositional Meaning Representations, EACL 2017

Ines Montani, Matthew Honnibal, Matthew Honnibal, Sofie Van Landeghem, Adriane Boyd, Henning Peters, … Avadh Patel. (2020, December 11). explosion/spaCy: v2.3.5: Bug fixes and simpler source installs (Version v2.3.5). Zenodo. http://doi.org/10.5281/zenodo.4317367