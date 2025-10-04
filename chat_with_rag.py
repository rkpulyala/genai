import os
os.environ['GRPC_VERBOSITY'] = 'NONE'
from langchain_community.vectorstores import Chroma
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
from setup_env import setup_env
from load_pdf import load_pdf_docs

def setup_rag_db(emb_model: str, combined_text: str):
    # Initialize the embedding model
    embedding_model = GoogleGenerativeAIEmbeddings(model=emb_model)

    # Create a Chroma vector store from the loaded documents
    # We need to chunk the documents for better RAG performance
    from langchain.text_splitter import RecursiveCharacterTextSplitter

    # Adjusting chunk size and overlap for potentially better performance with financial data
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=4000, chunk_overlap=800)
    docs = text_splitter.split_documents(combined_text)

    vectorstore = Chroma.from_documents(docs, embedding_model)

    print("RAG setup complete.")
    return vectorstore

def chat_with_rag(vectorstore):
    # Define the prompt template

    template = """
    Persona: You are a helpful assistant that answers questions based ONLY on the provided text.
    Action: You will take the user question (human message) and look for its answer in the provided "Document Context" and respond.
    Restrictions: If found, respond with the answer. If you cannot find the answer in the text, respond with "Not a relevant question".
    Document Context:
    {context}

    Question:
    {question}
    """
    prompt = ChatPromptTemplate.from_template(template)
    # Initialize the Chat Model
    # Make sure to replace "models/gemini-1.5-pro-latest" with a model from the list you generated if needed
    llm = ChatGoogleGenerativeAI(model="models/gemini-2.5-pro-preview-03-25")

    # Create a retriever with similarity score threshold
    retriever = vectorstore.as_retriever(
        search_type="similarity_score_threshold",
        search_kwargs={'score_threshold': 0.5, 'k': 10} # Adjusted threshold and number of chunks
    )

    # Create the RAG chain using the pipe operator
    rag_chain = (
        {"context": retriever, "question": RunnablePassthrough()}
        | prompt
        | llm
        | StrOutputParser()
    )

    print("RAG chain created.")
    return rag_chain


if __name__ == "__main__":
    setup_env()
    combined_text = load_pdf_docs("all")

    print("Chatbot started....")
    emb_model = "models/text-embedding-004"
    rag_db = setup_rag_db(emb_model, combined_text)
    rag_chain = chat_with_rag(rag_db)
    
    # Implement the chat loop
    while True:
        user_input = input("You: ")
        if user_input.lower() == "quit":
            break
        try:
            response = rag_chain.invoke(user_input)
            print(f"Bot: {response}")
        except Exception as e:
            print(f"An error occurred: {e}")

    print("Chatbot stopped.")