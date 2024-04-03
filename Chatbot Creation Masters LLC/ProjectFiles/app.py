# your_streamlit_app.py
import streamlit as st
from Chatbot_Creation import *
from Get_Medication_Analyzer import *
from Upload_Pdf import *
import warnings
warnings.filterwarnings("ignore")

def pdf_interface():
    st.title("PDF Upload Interface")
    pdf_interface_qa()
    
def chatbot_interface():
    st.title("Question Answer Chatbot")
    chatbot_interfaces_qa()

def medication_interface():
    st.title("Medication and Health Conditions Analyzer")
    medication_analyzer_qa()
    # Add logic for the third interface


def main():
    st.sidebar.title("Navigation")
    app_mode = st.sidebar.radio("Select Interface", ["PDF Upload", "Chatbot Question Answer", "Medication and Health Conditions Analyzer"])

    if app_mode == "PDF Upload":
        pdf_interface()
    elif app_mode == "Chatbot Question Answer":
        chatbot_interface()
    elif app_mode == "Medication and Health Conditions Analyzer":
        medication_interface()
   

if __name__ == '__main__':
    main()
