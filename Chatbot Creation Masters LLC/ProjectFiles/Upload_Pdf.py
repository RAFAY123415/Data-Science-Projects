import streamlit as st
from Data_Storing_Into_Pinecone import *


def pdf_interface_qa():
    # Page title and description
    st.title("PDF Upload App")
    st.write(
        "This app allows you to upload multiple PDF files. "
        "Uploaded files will be displayed below."
    )

    # File uploader for multiple PDFs
    uploaded_files = st.file_uploader("Choose multiple PDF files", type="pdf", accept_multiple_files=True)
    empty_df = pd.DataFrame(columns=['values', 'metadata'])
    # Initialize a flag to track submission status
    submission_completed = False
    if uploaded_files:
        # "Submit" button
        if not submission_completed and st.button("Submit"):
            # Use st.spinner to show a loading spinner during submission
            with st.spinner("Submitting files... Please wait."):
                 # Set the flag to True to prevent further submissions until a new file is uploaded
                submission_completed = True
                # Join current working directory with the temporary folder name
                for file_num, uploaded_file in enumerate(uploaded_files):
                    file_name = uploaded_file.name
                    file_content = Read_Pdf(uploaded_file)
                    text_chunks = Split_Docs_IntoChunks(file_content)
                    list_of_Chunks, Pdf_Name= extract_chunks_and_pdf_names(text_chunks,file_name)
                    embeddings_model = get_openai_transformer_embeddings(model_name="text-embedding-3-large")
                    df=create_embedding(embeddings_model, list_of_Chunks, Pdf_Name)
                    empty_df=empty_df._append(df, ignore_index=True)
                df2=empty_df
                df2['id'] = [f'vec{i+1}' for i in range(empty_df.shape[0])]
                df2['Source'] = df2['metadata'].apply(lambda x: x['Source'])
                df2['chunk_id']=df2['id']+df2['Source']
                vectors = create_vectors_from_dataframe(df2)
                index = initialize_pinecone(api_key="", environment="",
                                        index_name="")
                upsert_vectors_in_batches(index, vectors, vector_length=1000, batch_size=100, namespace="ns1")
                empty_df = pd.DataFrame(columns=['values', 'metadata'])
                # Display success message after successful submission
                st.success("Files submitted successfully to the database!")
            # Allow new submissions only if a new file is uploaded
            submission_completed = False

