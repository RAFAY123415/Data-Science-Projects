import streamlit as st
import PyPDF2
from Data_Storing_Into_Pinecone import *


def main():
    st.title("PDF Reader App")

    uploaded_files = st.file_uploader("Upload PDF files", type=["pdf"], accept_multiple_files=True)
    empty_df = pd.DataFrame(columns=['values', 'metadata'])


    if uploaded_files:
     
        for file_num, uploaded_file in enumerate(uploaded_files):
            file_name = uploaded_file.name
            file_content = Read_Pdf(uploaded_file)
            text_chunks = Split_Docs_IntoChunks(file_content)
            list_of_Chunks, Pdf_Name= extract_chunks_and_pdf_names(text_chunks,file_name)
            embeddings_model = get_openai_transformer_embeddings(model_name="text-embedding-3-large")
            df=create_embedding(embeddings_model, list_of_Chunks, Pdf_Name)
            empty_df=empty_df._append(df, ignore_index=True)
            st.dataframe(empty_df)
        
        df2=empty_df
        df2['id'] = [f'vec{i+1}' for i in range(empty_df.shape[0])]
        df2['Source'] = df2['metadata'].apply(lambda x: x['Source'])
        df2['chunk_id']=df2['id']+df2['Source']
        st.dataframe(df2)
        vectors = create_vectors_from_dataframe(df2)
        index = initialize_pinecone(api_key="", environment="",
                                        index_name="")
        upsert_vectors_in_batches(index, vectors, vector_length=1000, batch_size=30, namespace="ns1")
        st.write('done')
        empty_df = pd.DataFrame(columns=['values', 'metadata'])
        st.dataframe(empty_df)

if __name__ == "__main__":
    main()
