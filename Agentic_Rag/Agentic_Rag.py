"""
Designing Agentic Rag Using Langchain

Agentic RAG builds upon traditional RAG by introducing agents — autonomous decision-making entities capable of dynamic task execution. 
Unlike static retrieval processes, Agentic RAG leverages agents to adapt workflows based on context, integrating tools like APIs, 
databases, and external functions.
"""

'''
Building an Agentic RAG Chatbot with LangChain

LangChain provides a robust framework for integrating LLMs with tools, workflows, and external data. 
Here, we’ll build a chatbot capable of retrieving knowledge and accessing live APIs for real-time responses.
'''
import os
from dotenv import load_dotenv
from pathlib import Path

from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import TextLoader
from langchain_classic.chains import RetrievalQA
from langchain_classic.agents import AgentType
from langchain_classic.tools import Tool
from langchain_classic.agents.initialize import initialize_agent




# Set up your OpenAI API key:

# -----------------------------
# Load environment
# -----------------------------
BASE_DIR: Path = Path(__file__).resolve().parent
load_dotenv(".env.local")
LLM_VERSION = os.getenv("LLM_VERSION")


# Step 2: Creating a Vector Store for Document Retrieval
'''
A vector store is essential for RAG workflows. It stores knowledge in embeddings for efficient retrieval.
'''

# Load data from a text file
loader = TextLoader("langchain_knowledge_base.txt")  # Replace with your knowledge base
documents = loader.load()

# Split data into manageable chunks
text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
docs = text_splitter.split_documents(documents)

# Create a vector store with embeddings
embeddings = OpenAIEmbeddings()
vector_store = FAISS.from_documents(docs, embeddings)

# Initialize a retriever for querying the vector store
retriever = vector_store.as_retriever(search_type="similarity", search_k=3)



# Step 3: Defining Tools for the Agent
'''
Tools enable the agent to perform specific tasks. Here’s an example of integrating a weather API:
'''

# Example: Weather API function
def get_weather(location: str):
    return f"The current weather in {location} is sunny and 25°C."

# Define the tool
weather_tool = Tool(
    name="Weather Tool",
    func=get_weather,
    description="Provides weather information for a given location."
)

# Step 4: Building a Retrieval QA Chain
'''
The Retrieval QA chain combines the vector store with an LLM to answer knowledge-based queries.
'''

# Initialize the LLM
llm = ChatOpenAI(model=LLM_VERSION)

# Create the Retrieval QA chain
retrieval_qa_chain = RetrievalQA.from_chain_type(
    llm=llm,
    retriever=retriever,
    return_source_documents=True
)

# Combine tools and retrieval chain
tools = [
    Tool(
        name="Document Retrieval",
        func=lambda q: retrieval_qa_chain({"query": q})["result"],
        description="Retrieve knowledge from the document database."
    ),
    weather_tool
]

# Initialize the agent
agent = initialize_agent(
    tools=tools,
    llm=llm,
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    verbose=True
)

def chatbot_agentic_rag():
    print("Agentic RAG Chatbot is running! Type 'exit' to quit.")
    while True:
        user_query = input("You: ")
        if user_query.lower() == "exit":
            print("Chatbot session ended.")
            break
        try:
            response = agent.run(user_query)
            print(f"Bot: {response}")
        except Exception as e:
            print(f"Error: {e}")

chatbot_agentic_rag()

