
from openai import OpenAI
import streamlit as st
import os 
from langchain.embeddings.openai import OpenAIEmbeddings
from pinecone import Pinecone


def initialize_pinecone(api_key="", environment="", index_name=""):
  pc = Pinecone(api_key=api_key, environment=environment)
  index = pc.Index(index_name)
  return index

# get openai api key from platform.openai.com

def get_openai_transformer_embeddings(model_name="text-embedding-3-large"):
  OPENAI_API_KEY = os.getenv('OPENAI_API_KEY') or ''
  return OpenAIEmbeddings(model=model_name,openai_api_key=OPENAI_API_KEY)


def find_match(embeddings_model,index,query, k=2, score=False):
    result=index.query(
    namespace="ns1",
    vector=embeddings_model.embed_query(query),
    top_k=k,
    include_values=True,
    include_metadata=True)
    return result['matches'][0]['metadata']['text']+"\n"+result['matches'][1]['metadata']['text']


def return_answer (context,query):
  client = OpenAI(
    # defaults to os.environ.get("OPENAI_API_KEY")
    api_key='')
  # Make a request using the OpenAI API
  response = client.chat.completions.create(
    model="gpt-4",
    messages=[
        {"role": "system", "content": '''Fallow all the Following Instructions Given Below
        1.You Need to be Super Intelligent to Understand User Context and Query I am going to Pass You Context and Query inside user content.
        2.Provide Cleaned and Refined Answer according to Provided Context.
        3.Revise the provided text to eliminate any spacing errors and ensure a professional presentation.
        4.Correct spacing should be applied consistently throughout the text.'''},
        {"role": "user", "content": f"Context: \n{context}\n\nQuery: {query}"}
        ],
    temperature=0,
    max_tokens=2000,
    top_p=0,
    frequency_penalty=0,
    presence_penalty=0)
  return response.choices[0].message.content


def query_refiner(conversation, query):
    client = OpenAI(
    # defaults to os.environ.get("OPENAI_API_KEY")
    api_key='')
    response = client.completions.create(
    model="gpt-3.5-turbo-instruct",
    prompt=f"Given the following user query and conversation log, formulate a question that would be the most relevant to provide the user with an answer from a knowledge base.\n\nCONVERSATION LOG: \n{conversation}\n\nQuery: {query}\n\nRefined Query:",
    temperature=0,
    max_tokens= 500,
    top_p=0,
    frequency_penalty=0,
    presence_penalty=0
    )
    return response.choices[0].text


def get_conversation_string():
    conversation_string = ""
    for i in range(len(st.session_state['responses'])-1):
        conversation_string += "Human: "+st.session_state['requests'][i] + "\n"
        conversation_string += "Bot: "+ st.session_state['responses'][i+1] + "\n"
    return conversation_string
