import os
os.environ['GRPC_VERBOSITY'] = 'NONE'

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage, SystemMessage
import google.generativeai as genai
from setup_env import setup_env
from load_pdf import load_pdf

def chat_with_docs(question: str, context: str):
    """
    Interacts with the generative model to answer questions based on provided context.

    Args:
        question: The user's question.
        context: The document text to be used as context.

    Returns:
        The model's response or an error message.
    """

    # Initialize the Chat Model
    llm = ChatGoogleGenerativeAI(model="models/gemini-2.5-pro-preview-03-25")

    messages = [
        SystemMessage(content=f"""
        You are a helpful assistant that answers questions based ONLY on the provided text.
        If you cannot find the answer in the text, respond with "Not a relevant question".
        Document Context:
        {context}
        """),
        HumanMessage(content=question)
    ]
    try:
        response = llm.invoke(messages)
        return response.content
    except Exception as e:
        return f"An error occurred: {e}"



if __name__ == "__main__":
    setup_env()
    #List models
    # list_models() # Commented out as the user has already seen the list
    combined_text = load_pdf("apple")
    print("Chatbot started....")
    user_input = input("You: ")
    response = chat_with_docs(user_input, combined_text)
    print(f"Bot: {response}")