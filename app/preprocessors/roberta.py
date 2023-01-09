####################################################################################
# Preprocessors for roBERTa
# by JW
#
# A powerful collection of preprocessors for all sorts of NLP applications
# 
# preprocessors / roberta.py
####################################################################################

# IMPORT STATEMENTS ----------------------------------------------------------------

def preprocess_roberta(text):
    new_text = []
    for t in text.split(" "):
        t = '@user' if t.startswith('@') and len(t) > 1 else t
        t = 'http' if t.startswith('http') else t
        new_text.append(t)
    return " ".join(new_text)