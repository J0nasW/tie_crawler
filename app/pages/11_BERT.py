from transformers import BertTokenizer, BertModel, pipeline
import streamlit as st

st.title("BERT Playground")

model_choice = st.selectbox("Select model", ["bert-base-uncased", "distilbert-base-uncased", "bert-base-cased", "bert-large-uncased", "bert-large-cased"])

unmasker = pipeline('fill-mask', model=model_choice)
masked_sentence = st.text_input("Enter text to mask with [MASK] token")
if masked_sentence:
    res = unmasker(masked_sentence)
    #st.write(unmasker(masked_sentence))

    st.markdown("## " + masked_sentence)
    a,b,c,d,e = st.columns(5)
    a.metric(str(round(res[0]["score"] * 100,2)) + " %", res[0]["token_str"])
    b.metric(str(round(res[1]["score"] * 100,2)) + " %", res[1]["token_str"])
    c.metric(str(round(res[2]["score"] * 100,2)) + " %", res[2]["token_str"])
    d.metric(str(round(res[3]["score"] * 100,2)) + " %", res[3]["token_str"])
    e.metric(str(round(res[4]["score"] * 100,2)) + " %", res[4]["token_str"])

tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
model = BertModel.from_pretrained("bert-base-uncased")
text = st.text_input("Enter text to tokenize")
if text:
    encoded_input = tokenizer(text, return_tensors='pt')
    output = model(**encoded_input)
    st.write(output)