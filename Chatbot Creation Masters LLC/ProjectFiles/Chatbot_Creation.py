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
import warnings
warnings.filterwarnings("ignore")


def chatbot_interfaces_qa():

    if 'responses' not in st.session_state:
        st.session_state['responses'] = ["How can I assist you?"]

    if 'requests' not in st.session_state:
        st.session_state['requests'] = []

    llm = ChatOpenAI(model_name="gpt-4", openai_api_key="")

    if 'buffer_memory' not in st.session_state:
        st.session_state.buffer_memory = ConversationBufferWindowMemory(k=3, return_messages=True)

    system_msg_template = SystemMessagePromptTemplate.from_template(
        template="""Follow all the Following Instructions Given Below
            1.You are a helpful AI assistant I am going to Pass You Context and Query inside user content.
            2.Provide the Best, Professional, Error Free, Cleaned and Refined Answer according to User Query Based on Context.
            3.Revise the provided text to eliminate any spacing errors and ensure a professional presentation.
            4.Correct spacing should be applied consistently throughout the text."""
    )

    human_msg_template = HumanMessagePromptTemplate.from_template(template="{input}")

    prompt_template = ChatPromptTemplate.from_messages(
        [system_msg_template, MessagesPlaceholder(variable_name="history"), human_msg_template]
    )

    conversation = ConversationChain(memory=st.session_state.buffer_memory, prompt=prompt_template, llm=llm, verbose=True)

    response_container = st.container()
    textcontainer = st.container()

    with textcontainer:
        query_key = "input"
        query_input = st.text_input("Query: ", key=query_key, value='', type='default')
        #col1, col2 = st.columns([10, 1])
        #with col2:
            #submit_button = st.button("➡️")  # Unicode representation of the right arrow symbol
        if query_input: # or submit_button:
            with st.spinner("..."):
                index = initialize_pinecone()
                embeddings_model = get_openai_transformer_embeddings()
                context = find_match(embeddings_model, index, query_input)
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
        max-width: 800px;
        padding-right: 2rem;
        z-index: 9999;
        border: 1px solid #ccc;  
        border-radius: 5px;  
    }
    
    </style>
    """,
    unsafe_allow_html=True
    )
