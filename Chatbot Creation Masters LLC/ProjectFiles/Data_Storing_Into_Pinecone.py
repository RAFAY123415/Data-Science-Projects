import os
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings.openai import OpenAIEmbeddings
import PyPDF2
import pandas as pd
from pinecone import Pinecone
import warnings
warnings.filterwarnings("ignore")


def Read_Pdf(file):
        with file as f:
            pdf_reader = PyPDF2.PdfReader(f)
            text = ""
            for page_num in range(len(pdf_reader.pages)):
                text += pdf_reader.pages[page_num].extract_text()
            return text
    
def Split_Docs_IntoChunks(pdf_text,chunk_size=1000,chunk_overlap=20):
  text_splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
  chunks = text_splitter.split_text(pdf_text)
  return chunks

def get_openai_transformer_embeddings(model_name="text-embedding-3-large"):
    OPENAI_API_KEY = os.getenv('OPENAI_API_KEY') or ''
    return OpenAIEmbeddings(model=model_name,openai_api_key=OPENAI_API_KEY)

def extract_chunks_and_pdf_names(list_of_chunks,pdf_name):
    pdf_names = [pdf_name for interation in range(len(list_of_chunks))]
    return list_of_chunks, pdf_names

def create_embedding(embeddings_model, list_of_Chunks, Pdf_Name):
    # Generate embeddings for each chunk
    embeddings = embeddings_model.embed_documents(list_of_Chunks)
    # Generate unique IDs for each chunk
    # Format chunks with metadata
    formatted_chunks = [{"text": chunk, "Source": pdf_file_name} for chunk, pdf_file_name in zip(list_of_Chunks, Pdf_Name)]
    # Create a DataFrame
    df = pd.DataFrame({
        'values': embeddings,
        'metadata': formatted_chunks
    })
    return df


def create_vectors_from_dataframe(df):
    # Initialize an empty list to store the vectors
    vectors = []
    # Iterate through DataFrame rows
    for _, row in df.iterrows():
        vector = {
            "id":row['chunk_id'],
            "values": row['values'],
            "metadata": {"text": row['metadata']['text'], "source": row['metadata']['Source']}
        }
        vectors.append(vector)
    return vectors

def initialize_pinecone(api_key="", environment="", index_name=""):
  pc = Pinecone(api_key=api_key, environment=environment)
  index = pc.Index(index_name)
  return index

def upsert_vectors_in_batches(index, vectors, vector_length=1000, batch_size=100, namespace="ns1"):
        for batch_start in range(0, len(vectors), batch_size):
            batch_end = min(batch_start + batch_size, len(vectors))
            batch_data = vectors[batch_start:batch_end]
            # Use Pinecone's batch upsert function to insert or update documents in batch
            index.upsert(batch_data, namespace=namespace)



