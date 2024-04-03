import streamlit as st
from utils import *
import warnings
warnings.filterwarnings("ignore")


def medication_analyzer_qa():
    # Add custom CSS styles
    st.markdown(
        """
        <style>
            /* Add your custom styles here */
            body {
                font-family: 'Arial', sans-serif;
                background-color: #f0f0f0;
                color: #333333;
            }
            .stTextInput {
                background-color: #ffffff;
                border: 1px solid #cccccc;
                border-radius: 5px;
                padding: 8px;
                margin-bottom: 12px;
            }
            .stHeader {
                color: #0077cc;
            }
        </style>
        """,
        unsafe_allow_html=True
    )


    # User inputs
    Gender = st.selectbox("Select Person Gender", ["Male", "Female", "Other"], key="gender")
    Age = st.number_input("Enter Person Age", min_value=0, max_value=150, key="age")
    Height = st.number_input("Height In (Feet & Inches)", min_value=0.1, max_value=8.99, step=0.01, value=1.00)
    Weight = st.number_input("Weight In (Pounds)", min_value=1.0, max_value=1000.1, step=0.1, value=1.0)
    Medication = st.text_area("Enter Medication", key="medication")
    Health = st.text_area("Enter Health Conditions", key="health")
    Query = st.text_area("Please Clearly Define What Information You Want To Get From System", key="query")

    # Button to trigger reply generation
    button = st.button("Generate Reply")

    # Function to generate replies
    def generate_reply_1(Height,Weight,Gender, Age, Medication, Health, query):
        index = initialize_pinecone()
        embeddings_model = get_openai_transformer_embeddings()
        Context_query = Medication + Health
        Age="{} {}".format("Age",Age)
        Weight="{} {}{}".format("Weight",Weight, "lbs")
        Height = str(Height)
        feet, inches_decimal = map(int, Height.split('.'))
        Height = "{} ft {} in".format(feet, inches_decimal)
        Context = Height + Weight + Gender + Age + find_match(embeddings_model, index, Context_query)
        return return_answer(Context, query)

    def generate_reply_2(Height,Weight,Gender, Age, Medication, Health, query):
        index = initialize_pinecone()
        embeddings_model = get_openai_transformer_embeddings()
        Context_query = Medication + Health + query
        Age="{} {}".format("Age",Age)
        Weight="{} {}{}".format("Weight",Weight, "lbs")
        Height = str(Height)
        feet, inches_decimal = map(int, Height.split('.'))
        Height = "{} ft {} in".format(feet, inches_decimal)
        Context = Height + Weight + Gender + Age + find_match(embeddings_model, index, Context_query)
        return return_answer(Context, Context_query)
    
    def generate_reply_3(Height,Weight,Gender, Age, Medication, Health, query):
        index = initialize_pinecone()
        embeddings_model = get_openai_transformer_embeddings()
        Age="{} {}".format("Age",Age)
        Weight="{} {}{}".format("Weight",Weight, "lbs")
        Height = str(Height)
        feet, inches_decimal = map(int, Height.split('.'))
        Height = "{} ft {} in".format(feet, inches_decimal)
        Context_query = Height + Weight + Gender + Age + Medication + Health
        Context = find_match(embeddings_model, index, Context_query)
        return return_answer(Context, query)

    # Check if the button is clicked and all input fields are filled
    if button and Gender and Age and Medication and Health:
        with st.spinner("Generating Reply..."):
            # Generate replies
            reply_1 = generate_reply_1(Height, Weight, Gender, Age, Medication, Health, Query)
            reply_2 = generate_reply_2(Height,Weight, Gender, Age, Medication, Health, Query)
            reply_3 = generate_reply_3(Height,Weight,Gender, Age, Medication, Health, Query)

        # Display generated replies with titles
        st.markdown("<h3 class='stHeader'>User Output 1 For Testing</h3>", unsafe_allow_html=True)
        st.write(reply_1)

        st.markdown("<h3 class='stHeader'>User Output 2 For Testing</h3>", unsafe_allow_html=True)
        st.write(reply_2)

        st.markdown("<h3 class='stHeader'>User Output 3 For Testing</h3>", unsafe_allow_html=True)
        st.write(reply_3)
