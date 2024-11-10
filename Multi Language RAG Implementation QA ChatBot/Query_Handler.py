from langchain_cohere import ChatCohere # Importing Cohere model for language modeling tasks, allowing the use of Cohere’s language generation capabilities.
from langchain_cohere import CohereEmbeddings # Importing CohereEmbeddings for creating embeddings using Cohere, which can be useful for similarity searches or semantic understanding.
from langchain_chroma import Chroma # Importing Chroma vector store from Langchain to store and retrieve embeddings, enabling vector-based similarity searches.
import os # Importing os module for operating system functionalities.
import langid # Importing langid for language detection functionalities.
from langchain.prompts import PromptTemplate # Using Prompt to Provide Context and Query.
from langchain_core.runnables import RunnableSequence  # Importing Sequence to run llmchains
from deep_translator import GoogleTranslator # Language translate
from dotenv import load_dotenv # Loading env variables 
load_dotenv() 


'''
This class is designed to handle user queries presented as questions. It retrieves relevant context
from a Chroma database and generates precise, context-aware responses. The class supports 
multilingual queries, automatically detecting and translating text as needed. By integrating 
language models, it ensures high-quality, accurate answers based on the provided context.

'''
class QueryHandler:

    def __init__(self, persist_directory="./chroma_storage", embedding_model=None):
        # Initialize the class with optional directory and model
        self.persist_directory = persist_directory
        os.environ["COHERE_API_KEY"] = os.environ.get('COHERE_API_KEY')
        self.llm = ChatCohere()
        self.embedding_model = embedding_model or CohereEmbeddings(model="embed-multilingual-v3.0")
        self.chroma_db = Chroma(persist_directory=self.persist_directory, embedding_function=self.embedding_model)
    
    # This Function loads the Chroma DB and queries the relevant documents based on the query text.
    def load_and_query_chroma(self, query_text="none", k=3):
        
        """
        Loads a persisted Chroma database and runs a similarity search on it.
        Automatically detects the language of the query and provides results in the same language.
        
        Args:
        persist_directory (str): Directory where the Chroma database is stored.
        query_text (str): The input query for similarity search.
        k (int): Number of nearest neighbors to retrieve from the search.
        
        Returns:
        results (str): List of search results with relevance scores or a message indicating no suitable match.
        
        """
        try:
            # Detect the language of the query using langid
            query_language, _ = langid.classify(query_text)

            # Check if the language is supported (English or Finnish)
            if query_language not in ["en", "fi"]:
                return "This system currently supports queries in English and Finnish only."

        except Exception as e:
            return "Error detecting language. This system currently supports queries in English and Finnish only."

        # Perform similarity search
        results = self.chroma_db.similarity_search_with_relevance_scores(query=query_text, k=k)

        # Check if any results meet the relevance threshold
        if not results or results[0][1] < 0.3:
            if query_language == "fi":
                return "Emme pystyneet löytämään sopivaa vastausta tähän kyselyyn."
            else:  # Default to English for non-Finnish detected languages
                return "We are unable to find a suitable match for this query."

        # Extract page content from each result
        formatted_results = [result.page_content for result, score in results]

        # Join results into a single string
        joined_results = " ".join(formatted_results)

        # Detect the language of the results (if they are different from the query language, translate them)
        result_language, _ = langid.classify(joined_results)

        if query_language != result_language:
            # Translate results to the language of the query
            translated_results = GoogleTranslator(source=result_language, target=query_language).translate(joined_results)
            return translated_results
        else:
            # Return results in their original language if no translation is needed
            return joined_results
    
    # Function to create a formatted prompt using specific context and question input
    def create_formatted_prompt(self, context, question):
        
        """
        Generates a formatted prompt for answering questions in a structured and professional manner.
        
        Parameters:
        - context (str): The context or background information to base the answer on.
        - question (str): The question to be answered.
        
        Returns:
        - str: A formatted prompt with clear guidelines for the response format and language.
        
        """
        # Enhanced prompt template to ensure precise, relevant, and well-structured responses
        PROMPT_TEMPLATE = """
        You are a professional assistant with expertise in the subject matter. Your goal is to provide the most accurate, clear, and relevant response based on the context provided. Ensure the response is well-organized, insightful, and demonstrates a deep understanding of the topic.
        Response should be in what language question was asked.

        Context:
        {context}
        
        Question:
        {question}
        
        """

        # Initialize the PromptTemplate with defined input variables for context and question
        prompt_template = PromptTemplate(
            input_variables=["context", "question"],
            template=PROMPT_TEMPLATE
            )
        
        # Format the template with the given context and question, returning a final prompt
        return prompt_template.format(context=context, question=question)

    # Main function to generate response
    def generate_response(self, query):
        
        """
        Generates a response to a query by retrieving context from the Chroma database and
        generating an answer using a Cohere LLM.
         
        Parameters:
        - query (str): The user's question or input query.
        
        Returns:
        - str: The generated response based on the context and question.
         
        """
        # Fetch context from the Chroma database
        context = self.load_and_query_chroma(query_text=query)
        
        if context == "Emme pystyneet löytämään sopivaa vastausta tähän kyselyyn.":
            return "Emme valitettavasti löytäneet sopivaa vastausta tähän kyselyyn. Voisitko ystävällisesti tarkentaa tai muotoilla kysymyksesi uudelleen, jotta voimme auttaa sinua paremmin?"  # Return the Finnish no-answer message
        elif context == "We are unable to find a suitable match for this query.":
            return "Unfortunately, we were unable to find a suitable answer to this query. Could you kindly clarify or rephrase your question so that we can assist you better?"  # Return the English no-answer message
    
        
        # Generate the formatted prompt using the context and query
        prompt = self.create_formatted_prompt(context=context, question=query)

        # Create the LLMChain with the prompt template and LLM
        prompt_template = PromptTemplate(input_variables=["context", "question"], template=prompt)
        llm_chain = RunnableSequence(prompt_template, self.llm)

        # Run the chain to generate an answer
        generated_answer = llm_chain.invoke({"context": context, "question": query})
        return generated_answer.content