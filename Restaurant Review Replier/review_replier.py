import openai
import streamlit as st

openai.api_key ='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'

st.header("Restaurant Review Replier")
review  = st.text_area("Enter Customer Review")
button = st.button("Generate Reply")

def generate_reply(review):
    response = openai.Completion.create(
    model="text-davinci-003",
    prompt=f"This is a restaurant review replier bot. If the customer has any concerns address them.\n\nReview:{review}\n\nreplay:",
    temperature=0.7,
    max_tokens=100,
    top_p=1,
    frequency_penalty=0,
    presence_penalty=0
    )
    return response.choices[0].text

if button and review:
    with st.spinner("Generating Reply..."):
        reply = generate_reply(review)
    st.write(reply)
