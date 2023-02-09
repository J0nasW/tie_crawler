###
# This LDA python script can take a list of strings as input and output an lda model and a list of topics.
###

# Some basic libraries
import os
import pandas as pd

# Analyzation Libraries
import spacy
import pyLDAvis.gensim_models
from gensim.models import LdaMulticore
from gensim.corpora.dictionary import Dictionary
from gensim.corpora.mmcorpus import MmCorpus

import argparse

def is_file(path):
    return os.path.isfile(path)

def train_lda(text_df, save_dir = ".", dict_no_below = int(5), dict_no_above = float(0.5), dict_keep_n = int(10000), num_iterations = int(10), num_topics = int(5), num_workers = int(1), num_passes = int(10)):
    try:
        print("-------- START OF LDA TRAINING --------")
        text_df = pd.DataFrame(text_df)
        text_df.columns = ['text']
        # Create a dictionary from the text_df.
        nlp = spacy.load("en_core_web_md")
        # Tags I want to remove from the text
        removal= ['ADV','PRON','CCONJ','PUNCT','PART','DET','ADP','SPACE', 'NUM', 'SYM']
        tokens = []
        for summary in nlp.pipe(text_df["text"]):
            proj_tok = [token.lemma_.lower() for token in summary if token.pos_ not in removal and not token.is_stop and token.is_alpha]
            tokens.append(proj_tok)
        text_df.loc(axis=1)['tokens'] = tokens
        dictionary = Dictionary(text_df["tokens"])
        # Filter out words that occur less than 5 documents, or more than 50% of the documents. Also keep only the first 100000 most frequent words.
        dictionary.filter_extremes(no_below=dict_no_below, no_above=dict_no_above, keep_n=dict_keep_n)
        dictionary.save(os.path.join(save_dir, "dictionary.gensim"))
        # Create a corpus from the text_df.
        corpus = [dictionary.doc2bow(text) for text in text_df["tokens"]]
        MmCorpus.serialize(os.path.join(save_dir, "corpus.mm"), corpus)
        # Train the model.
    
        # Train LDA model.
        print("Training LDA model...")
        lda_model = LdaMulticore(corpus=corpus, id2word=dictionary, iterations=num_iterations, num_topics=num_topics, workers=num_workers, passes=num_passes)
        print("LDA model trained.")
        lda_model.save(os.path.join(save_dir, "lda_model.gensim"))
        # Save the model.
        lda_display = pyLDAvis.gensim_models.prepare(lda_model, corpus, dictionary)
        pyLDAvis.save_html(lda_display, os.path.join(save_dir, "lda_display.html"))
        return lda_model, dictionary, corpus

    except Exception as e:
        print("An error occurred while training the LDA model.")
        print(e)
        return None

if __name__ == "__main__":
    # Get some arguments.
    parser = argparse.ArgumentParser()
    parser.add_argument("--text_csv", help="Provide the directory to a valid csv file for processing.", required=True)
    parser.add_argument("--save_dir", help="The path, where to save numerous files including the lda model.", default="", required=False)
    parser.add_argument("--num_iterations", help="Number of iterations to train the model.", default=10, required=False)
    parser.add_argument("--num_topics", help="Number of topics to train the model.", default=5, required=False)
    parser.add_argument("--num_workers", help="Number of CPU workers to train the model. Default is 1 process.", default=1, required=False)
    parser.add_argument("--num_passes", help="Number of passes to train the model.", default=1, required=False)
    parser.add_argument("--dict_no_below", help="Number of documents a word must appear in to be included in the dictionary.", default=5, required=False)
    parser.add_argument("--dict_no_above", help="The maximum proportion of documents a word can appear in to be included in the dictionary.", default=0.5, required=False)
    parser.add_argument("--dict_keep_n", help="The maximum number of words to keep in the dictionary.", default=10000, required=False)
    args = parser.parse_args()

    # Check if the text_csv file exists.
    if not is_file(args.text_csv) or not args.text_csv.endswith(".csv"):
        print("The text_csv file does not exist or is not formatted correctly.")
        exit(1)

    text_df = pd.read_csv(args.text_csv, names=["text"])
    #print(text_df)
    print("The CSV was loaded successfully. LDA training will begin shortly...")
    lda_model, dictionary, corpus = train_lda(text_df, str(args.save_dir), int(args.dict_no_below), float(args.dict_no_above), int(args.dict_keep_n), int(args.num_iterations), int(args.num_topics), int(args.num_workers), int(args.num_passes))
    print("LDA model trained successfully. The model will be saved to the save_dir: " + str(args.save_dir))
    print("Here are the LDA topics: " + str(lda_model.print_topics()))