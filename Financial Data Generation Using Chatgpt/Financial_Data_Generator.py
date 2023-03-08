import openai
import streamlit as st
import pandas as pd
import numpy as np

openai.api_key ='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'

st.header(":blue[Financial Data Generator]")
input  = st.text_area("Enter Financial Data Description")
button = st.button("Generate Reply")

def generate_reply(input) :
    response = openai.Completion.create(
    model="text-davinci-003",
    prompt=f"User Input a keyword ,question ,description ,or ask anything about financial domain please answer according to that and make sure you should be 100 percent accurate and relevant to Finance Domain.If the user input any nonsense, trickery,not related to Finance, or has no clear answer, I will respond with 'Please Ask Anything Related To Financial Domain.Thank You.'Input:{input}Answer:",
    temperature=0.5,
    max_tokens=3000,
    top_p=1,
    frequency_penalty=0,
    presence_penalty=0
    )
    return str(response.choices[0].text)


if button and input:
    with st.spinner("Generating Reply..."):
        reply = generate_reply(input)
    st.write(reply)

  
