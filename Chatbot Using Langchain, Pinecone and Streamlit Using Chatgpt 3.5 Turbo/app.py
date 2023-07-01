import streamlit as st
from langchain.chat_models import ChatOpenAI
from langchain.chains import ConversationChain
from langchain.chains.conversation.memory import ConversationBufferWindowMemory
from langchain.prompts import (
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
    ChatPromptTemplate,
    MessagesPlaceholder
)
from streamlit_chat import message
from utils import *

st.subheader("Chatbot with Langchain, ChatGPT, Pinecone, and Streamlit")

if 'responses' not in st.session_state:
    st.session_state['responses'] = ["How can I assist you?"]

if 'requests' not in st.session_state:
    st.session_state['requests'] = []

llm = ChatOpenAI(model_name="gpt-3.5-turbo", openai_api_key="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")

if 'buffer_memory' not in st.session_state:
    st.session_state.buffer_memory = ConversationBufferWindowMemory(k=3, return_messages=True)

system_msg_template = SystemMessagePromptTemplate.from_template(
    template="""Answer the question as truthfully as possible using the provided context, 
    and if the answer is not contained within the text below, say 'I don't know'"""
)

human_msg_template = HumanMessagePromptTemplate.from_template(template="{input}")

prompt_template = ChatPromptTemplate.from_messages(
    [system_msg_template, MessagesPlaceholder(variable_name="history"), human_msg_template]
)

conversation = ConversationChain(memory=st.session_state.buffer_memory, prompt=prompt_template, llm=llm, verbose=True)

st.title("Langchain Chatbot")

response_container = st.container()
textcontainer = st.container()

with textcontainer:
    query_key = "input"
    query_input = st.text_input("Query: ", key=query_key, value='', type='default')
    col1, col2 = st.columns([10, 1])
    with col2:
        submit_button = st.button("➡️")  # Unicode representation of the right arrow symbol
    if query_input and submit_button:
        with st.spinner("..."):
            conversation_string = get_conversation_string()
            refined_query = query_refiner(conversation_string, query_input)
            context = find_match(refined_query)
            response = conversation.predict(input=f"Context:\n {context} \n\n Query:\n{query_input}")
        st.session_state.requests.append(query_input)
        st.session_state.responses.append(response)

with response_container:
    if st.session_state['responses']:
        for i in range(len(st.session_state['responses'])):
            message(st.session_state['responses'][i], key=str(i))
            if i < len(st.session_state['requests']):
                message(st.session_state['requests'][i], is_user=True, key=str(i) + '_user')

# Add custom CSS to make the query input box fixed and adjust the layout
st.markdown(
    """
    <style>
    .stTextInput {
        position: fixed;
        bottom: 20px;
        width: 85%;
        max-width: 600px;
        padding-right: 2rem;
        z-index: 9999;
    }
    .stButton > button {
        width: 100%;
        height: 100%;
        border-radius: 0 5px 5px 0;
    }
    .stButton {
        position: fixed;
        bottom: 20px;
        right: 400px;
        width: 15%;
        max-width: 120px;
        height: 38px;
        padding: 0;
        z-index: 9999;
    }
    </style>
    """,
    unsafe_allow_html=True
)
