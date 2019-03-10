# RIW
Projet de recherche d'information
Construction d'un moteur de recherche

Download the document corpus:  
- http://ir.dcs.gla.ac.uk/resources/test_collections/cacm/

## Project set up:

- create a python3 virtualenvironment for the project

> `python3 -m venv .`

- enter the virtual environment

> `source bin/activate`

- install the requirements

> `pip install -r requirements.txt`

- import nltk packages: after installing the nltk requirement, you will need to install the punkt library

- on macOS, you may have to `pip install PyQt5` to make it works.

## Running the project

- run the following command to see all available options:

> `python run.py --h`

## To quickly test the search engine's performance on the corpus, run the following command from the root directory:

> `python run_all.py`

## Stanford collection

To test with the stanford collection, start by running the preparation file:  
> `python prepare_pa1.py`  

This will load the documents, create an inverted index and serialize them. Once this is done, you can test the search using the main file run file for the stanford collection. Use the following command:
> `run_pa1.py`

