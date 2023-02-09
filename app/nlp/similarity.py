###
# This script can be used to compare two or more strings or documents and return a similarity score
###

# Some basic libraries
import os
import pandas as pd
import argparse

# Analyzation Libraries
import spacy
import multiprocessing as mp
import numpy as np

def calc_similarity_multicore(text_list, save_dir):
    try:
        print("-------- START OF SIMILARITY CALCULATION --------")
        # Load the large English model
        nlp = spacy.load("en_core_web_sm")

        text_list = [
            "Apple is a technology company based in Cupertino, California.",
            "Microsoft is a technology company based in Redmond, Washington.",
            "Amazon is an e-commerce company based in Seattle, Washington.",
        ]
        # Create doc objects for each text
        docs = [nlp(text) for text in text_list]

        n = len(docs)
        similarity_matrix = np.zeros((n, n))

        # Split the input indices into chunks
        chunk_size = max(n // mp.cpu_count(), 1)
        inputs = [(i, j) for i in range(n) for j in range(i+1, n)]
        inputs = [inputs[i:i+chunk_size] for i in range(0, len(inputs), chunk_size)]

        # Create a pool of workers
        with mp.Pool(processes=mp.cpu_count()) as pool:
            # Map the worker function to each chunk of input indices
            pool.map(worker, [(inputs[i], similarity_matrix, docs, nlp) for i in range(len(inputs))])


        average_similarity = sum(similarity_matrix)/len(similarity_matrix)
        print("Similarity calculated. The average similarity is: " + str(average_similarity) + ".")

        # Save the similarity matrix
        np.save(os.path.join(save_dir, "similarity_matrix.npy"), similarity_matrix)
        print("Similarity matrix saved.")

        return similarity_matrix, average_similarity

    except Exception as e:
        print("An error occurred while calculating the similarity.")
        print(e)
        return None

# Define the worker function
def worker(args):
    inputs, similarity_matrix, compute_similarity = args
    for i, j in inputs:
        similarity_matrix[i, j] = compute_similarity(i, j)
        similarity_matrix[j, i] = similarity_matrix[i, j]

# Define the compute_similarity function
def compute_similarity(doc1, doc2, nlp):
    return doc1.similarity(doc2)

def calc_similarity(text_df, save_dir = "."):
    try:
        print("-------- START OF SIMILARITY CALCULATION --------")
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
        # Calculate the similarity between the documents.
        similarity = []
        for i in range(len(text_df)):
            for j in range(i+1, len(text_df)):
                similarity.append(nlp(text_df.iloc[i]["text"]).similarity(nlp(text_df.iloc[j]["text"])))
        print("Similarity calculated. The average similarity is: " + str(sum(similarity)/len(similarity)) + ".")
        average_similarity = sum(similarity)/len(similarity)
        return similarity, average_similarity

    except Exception as e:
        print("An error occurred while calculating the similarity.")
        print(e)
        return None

if __name__ == "__main__":
    # Get some arguments.
    parser = argparse.ArgumentParser()
    parser.add_argument("--text", help="Provide a list of text samples.", required=True)
    parser.add_argument("--save_dir", help="Provide a directory to save the similarity matrix.", required=False, default=".")
    parser.add_argument("--num_workers", help="Provide the number of workers to use.", required=False, default=4)
    args = parser.parse_args()

    similarity_matrix, average_similarity = calc_similarity_multicore(args.text, args.save_dir)