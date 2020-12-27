# Computational Semantics
Contains all code and documentation of the final project of the course
 Computational Semantics, taught at the University of Groningen.
 
The goal of this application is to tag sentences using semantic tags.

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

When you have installed the required packages, you are ready to explore


### Obtaining the PMB data

Before you can train and/or test the tagger, you need to download the
 data from the [Parallel Meaning Bank](https://pmb.let.rug.nl/) (also
  known as the PMB). We use
  the .conll files from [Rik van Noord's](http://www.rikvannoord.nl/)
   [GitHub repository](https://github.com/RikVN/DRS_parsing), as these
    files are already preprocessed and standardised for easier use.
    
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
## Training the tagger

As mentioned in the last subsection, we use spaCy for the construction
of our semantic tagger.