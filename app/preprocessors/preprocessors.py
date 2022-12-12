####################################################################################
# Preprocessors
# by JW
#
# A powerful collection of preprocessors for all sorts of NLP applications
# 
# preprocessors / preprocessors.py
####################################################################################

# IMPORT STATEMENTS ----------------------------------------------------------------

import nltk
nltk.download('punkt')
nltk.download('words')
nltk.download('stopwords')
nltk.download('wordnet')
from nltk.tokenize import word_tokenize
from nltk.corpus import words, stopwords
from nltk.stem import PorterStemmer, WordNetLemmatizer 
import num2words
import splitter

def query_filter(data, query, special_words):
    # query = tokenize_data(query)
    # query = lowercase(query)
    # query = remove_logic_operators(query)
    # query = remove_punctuation(query)
    # query = remove_single_chars(query)
    # data = remove_custom_words(data, query)

    query = split_add_special_words(query, special_words)
    #new_query = tokenize_data(new_query)
    query = lowercase(query)
    query = remove_logic_operators(query)
    query = remove_punctuation(query)
    query = remove_single_chars(query)
    query = split_compound_words(query)
    data = remove_custom_words(data, query, "Block") # Query Specific Custom Words!
    data = remove_custom_words(data, query, "Supply ") # Query Specific Custom Words!
    return data

def wordcloud_filter(data):
    remove_stopwords(data)
    return data

def lowercase(data):
    # Lowercase
    if isinstance(data, str):
        data = data.lower()
    else:
        for i in range(len(data)):
            try:
                data[i] = data[i].lower()
            except:
                print("An error occured " + str(data[i]))
    return data

def tokenize_data(data):
    if isinstance(data, str):
        data = word_tokenize(data)
    else:
        for i in range(len(data)):
            try:
                data = word_tokenize(data[i])
            except:
                print("An error occured " + str(data[i]))
    return data

def remove_stopwords(data):
    # Stopwords
    stop_words = set(stopwords.words('english'))
    if isinstance(data, str):
        text_tokens = word_tokenize(data)
        data = [word for word in text_tokens if not word in stop_words]
        data = " ".join(data)
    else:
        for i in range(len(data)):
            try:
                text_tokens = word_tokenize(data[i])
                data[i] = [word for word in text_tokens if not word in stop_words]
                data[i] = " ".join(data[i])
            except:
                print("An error occured " + str(data[i]))
    return data

def split_compound_words(data):
    # Split well known compount words...
    if isinstance(data, str):
        splitter.split(data)
    else:
        for i in range(len(data)):
            try:
                splitter.split(data[i])
            except:
                print("An error occured " + str(data[i]))
    return data

def split_add_special_words(data, special_words):
    # Split defined words and add them to the data (special words has to be dictionary!)
    if isinstance(data, str):
        data = tokenize_data(data)
        for key in special_words:
            for word in data:
                if word == key:
                    print("[str] Found " + key)
                    data.extend(special_words.get(key).split())
    else:
        for i in range(len(data)):
            try:
                for key in special_words:
                    if data[i] == key:
                        print("[list] Found " + key)
                        data[i] += (" " + special_words.get(key))
            except:
                print("An error occured " + str(data[i]))
    return data

def replace_words(data, special_words):
    # Replace special words
    if isinstance(data, str):
        data = tokenize_data(data)
        for key in special_words:
            for word in data:
                if word == key:
                    print("[str] Found " + key)
                    data.replace(word, key)
                    #data.extend(special_words.get(key).split())
    else:
        for i in range(len(data)):
            try:
                for key in special_words:
                    if data[i] == key:
                        print("[list] Found " + key + " and will replace it with " + str(special_words.get(key)))
                        data[i] = special_words.get(key)
                        #data[i].replace(data[i], special_words.get(key))
            except:
                print("An error occured " + str(data[i]))
    return data


def remove_custom_words(data, query, custom_words):
    # Custom Word Remover - Takes only tokenized list "data"
    if isinstance(data, str):
        for j in query:
            data = data.replace(j, '')
        data = data.replace(custom_words, '')
    else:
        for i in range(len(data)):
            try:
                for j in query:
                    data[i] = data[i].replace(j, '')
                data[i] = data[i].replace(custom_words, '')
            except:
                print("An error occured " + str(data[i]))
        data = list(filter(None, data))
    return data

def remove_logic_operators(data):
    # Logic Operators
    logic_operators = ["AND","and","And","OR","Or","or","NOT","Not","not"]
    if isinstance(data, str):
        for j in logic_operators:
            data = data.replace(j, '')
    else:
        for i in range(len(data)):
            for j in logic_operators:
                data[i] = data[i].replace(j, '')
        data = list(filter(None, data))
    return data

def remove_words_from_list(data, words):
    if isinstance(data, str):
        for j in words:
            data = data.replace(j, '')
    else:
        for i in range(len(data)):
            for j in words:
                data[i] = data[i].replace(j, '')
        data = list(filter(None, data))
    return data

def remove_other_things(data):
    # Other Things
    other_things = ["Author", "Author(s)", "\\u00a9", "©", "also", "use", "using", "based"]
    if isinstance(data, str):
        for j in other_things:
            data = data.replace(j, '')
    else:
        for i in range(len(data)):
            for j in other_things:
                try:
                    data[i] = data[i].replace(j, '')
                except:
                    print("An error occured @ removing other things")
        data = list(filter(None, data))
    return data

def remove_custom_things(data, custom_things):
    # custom_things
    # custom_things = ["Author", "Author(s)", "\\u00a9", "©", "also", "use", "using", "based", "s"]
    if isinstance(data, str):
        for j in custom_things:
            data = data.replace(j, '')
    else:
        for i in range(len(data)):
            for j in custom_things:
                try:
                    data[i] = data[i].replace(j, '')
                except:
                    print("An error occured @ removing custom things")
        data = list(filter(None, data))
    return data

def remove_first_end_spaces(data):
    # Strip strings from spaces
    if isinstance(data, str):
        data = data.strip()
    else:
        for i in range(len(data)):
            try:
                data[i] = data[i].strip()
            except:
                print("An error occured " + str(data[i]))
    return data

def remove_punctuation(data):
    # Punctuation
    symbols = ["!","#","$","%","&","(",")","*","+","-",".","/",":",";","<","=",">","?","@","[","\\","]","^","_","`","{","|","}","~","\n","\"", "'", ","]
    if isinstance(data, str):
        for j in symbols:
            data = data.replace(j, '')
    else:
        for i in range(len(data)):
            for j in symbols:
                data[i] = data[i].replace(j, '')
        data = list(filter(None, data))
    return data

def remove_single_chars(data):
    # Single Characters
    
    if isinstance(data, str):
        try:
            ' '.join(word for word in data.split() if len(word)>2)
        except:
            print("An error occured")
    else:
        for i in range(len(data)):
            try:
                ' '.join(word for word in data[i].split() if len(word)>2)
            except:
                print("An error occured " + str(data[i]))
    return data

def remove_double_chars(data):
    # Double Characters
    
    if isinstance(data, str):
        try:
            ' '.join(word for word in data.split() if len(word)>3)
        except:
            print("An error occured")
    else:
        for i in range(len(data)):
            try:
                ' '.join(word for word in data[i].split() if len(word)>2)
            except:
                print("An error occured " + str(data[i]))
    return data

def num_to_words(data):
    # Converting numbers in the text to words
    for i in range(len(data)):
        try:
            #' '.join(num2words(word) for word in data[i].split() if word.isdigit() == True)
            text_tokens = word_tokenize(data[i])
            data[i] = [num2words(word) for word in text_tokens if word.isdigit() == True]
            data[i] = " ".join(data[i])
        except:
            print("An error occured " + str(data[i]))
    return data

def deleteNumbers(data):
    # Delete numerical values in the text
    for i in range(len(data)):
        try:
            text_tokens = word_tokenize(data[i])
            data[i] = [word for word in text_tokens if not word.isdigit() == True]
            data[i] = " ".join(data[i])
        except:
            print("An error occured " + str(data[i]))
    return data

def lemmatize_words(data):
    lemmatizer = WordNetLemmatizer()
    for i in range(len(data)):
        try:
            ' '.join(word for word in data[i].split() if len(word)>2)
            text_tokens = word_tokenize(data[i])
            data[i] = [lemmatizer.lemmatize(word) for word in text_tokens]
            data[i] = " ".join(data[i])
        except:
            print("An error occured " + str(data[i]))
    return data

def find_ngrams(data):
    return zip(*[data[i:] for i in range(len(data))])

def stem_words(data):
    # Stemming
    ps = PorterStemmer()
    for i in range(len(data)):
        try:
            ' '.join(word for word in data[i].split() if len(word)>2)
            text_tokens = word_tokenize(data[i])
            data[i] = [ps.stem(word) for word in text_tokens]
            data[i] = " ".join(data[i])
        except:
            print("An error occured " + str(data[i]))
    return data

def extract_unusual_words(data):
    """Use the nltk corpus to generate a list of unusual tokens in the
    corpus of documents."""
    text_vocab = set(word for document in data for word in document)
    english_vocab = set(w.lower() for w in words.words())
    unusual = text_vocab.difference(english_vocab)

    data = [[token for token in document if token not in unusual] for document in data]
    return set(unusual)