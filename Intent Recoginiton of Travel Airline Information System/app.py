import openai
import streamlit as st

openai.api_key ='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'

st.header("Intent Recoginiton of Travel Airline Information System")
review  = st.text_area("Enter Text To Recognize Content")
button = st.button("Generate Reply")

def generate_reply(review):
    response = openai.Completion.create(
        model="ada:ft-personal-2023-02-07-14-10-09",
        prompt='{review}\n\nIntent:\n\n',
        max_tokens=5,
        temperature=0,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0,
        stop=["END"]
        )
    return response.choices[0].text

if button and review:
    with st.spinner("Generating Reply..."):
        reply = generate_reply(review)
    st.write(reply)