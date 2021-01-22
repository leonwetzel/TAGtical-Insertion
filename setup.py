import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="tagtical_insertion", # Replace with your own username
    version="1.0.0",
    author="Leon Wetzel, Marjolein Spijkerman and Nik van 't Slot",
    author_email="l.f.a.wetzel@student.rug.nl",
    description="A semantic tagger, based on spaCy's NER pipeline",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/leonwetzel/TAGtical-Insertion",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)