
import requests
from bs4 import BeautifulSoup
from sentence_transformers import SentenceTransformer
import pinecone
import openai


def Extract_Data(url):
    response = requests.get(url)
    # Create a BeautifulSoup object to parse the HTML content
    soup = BeautifulSoup(response.content, 'html.parser')
    # Find and remove script tags from the parsed HTML
    for script in soup(['script']):
        script.extract()
    # Find the main content element on the page
    content_element = soup.find(id='mw-content-text')
    # Extract the text from the content element
    page_content = content_element.get_text()
    page_content=' '.join(page_content.split())
    return page_content

def split_text_into_chunks(text, max_chars=2000):
    chunks = []
    current_chunk = ""
    words = text.split()
    for word in words:
        if len(current_chunk + " " + word) <= max_chars:
            current_chunk += " " + word
        else:
            chunks.append(current_chunk.strip())
            current_chunk = word

    if current_chunk:
        chunks.append(current_chunk.strip())

    return chunks

def Generate_Embeddings (chunk) :
  model = SentenceTransformer('all-MiniLM-L6-v2')
  embeddings = model.encode(chunk)
  return embeddings

def Save_Into_Pinecone (url,chunks,Embeddings) :
  pinecone.init(api_key="8b39dd7f-0ed7-4314-be6a-04eb9b7656f9", environment="us-east1-gcp")
  # Create an index
  index = pinecone.Index(index_name='question')
  # Prepare the data for upsert
  upsert_data = []
  # Store the URL, chunks, and embeddings in the Pinecone index with metadata
  for chunk, embedding in zip(chunks, Embeddings):
    metadata = {'url': url, 'chunk': chunk}
    flat_embedding = embedding.flatten().tolist()
    truncated_id = (url + "#" + chunk)[:512]  # Truncate the ID if necessary
    ascii_id = truncated_id.encode('ascii', 'ignore').decode('ascii')  # Encode ID to ASCII
    upsert_data.append((ascii_id, flat_embedding, metadata))
  # Convert the upsert data to the required format
  upsert_data_formatted = [(id, vector, meta) for id, vector, meta in upsert_data]
  # Upsert the data
  upsert_response = index.upsert(vectors=upsert_data_formatted, namespace='example-namespace')
  # Close the index and shutdown Pinecone
  index.close()


def finding_match (question,k=1):
  value=Generate_Embeddings(question).flatten().tolist()
  pinecone.init(api_key="8b39dd7f-0ed7-4314-be6a-04eb9b7656f9", environment="us-east1-gcp")
  index = pinecone.Index("question")
  result=index.query(value,top_k=k,include_metadata=True,namespace = 'example-namespace')
  return question,result['matches'][0]['metadata']['chunk']

def generate_answer (question,context):
  try:
    openai.api_key ='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'
    # Create a completions using the question and context
    response = openai.Completion.create(
        prompt=f"Answer the question based on the context, and if the question can't be answered based on the context, say \"I don't know\"\n\nContext: {context}\n\n---\n\nQuestion: {question}\nAnswer:",
        temperature=0.5,
        max_tokens=200,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0,
        stop=None,
        model="text-davinci-003",
        )
    return response["choices"][0]["text"].strip()
  except Exception as e:
    return ""