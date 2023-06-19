import streamlit as st
from Q_A import *



st.header("Semantic Search Engine for Documents and Q&A")
url = False
query = False
options = st.radio(
    'Choose task',
    ('Ask a question','Update the Database'))

if 'Update the Database' in options:
    url = st.text_input("Enter the url of the document")
    
if 'Ask a question' in options:
    query = st.text_input("Enter your question")

button = st.button("Submit")

if button and (url or query) :
    if 'Update the Database' in options:
        with st.spinner("Updating Database..."):
            text=Extract_Data(url)
            chunk=split_text_into_chunks(text, max_chars=2000)
            Embeddings=Generate_Embeddings (chunk)
            Save_Into_Pinecone (url,chunk,Embeddings)

    if 'Ask a question' in options:
        with st.spinner("Searching for the answer..."):
            question,context=finding_match (query,k=1)
            Answer=generate_answer (question,context)
            st.success("Answer: "+Answer)





