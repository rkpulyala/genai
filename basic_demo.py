import os
os.environ['GRPC_VERBOSITY'] = 'NONE'

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage, SystemMessage
import google.generativeai as genai
from setup_env import setup_env

setup_env()
# Initialize the Chat Model
llm = ChatGoogleGenerativeAI(model="models/gemini-2.5-pro-preview-03-25")

# Create a system message and a human message
messages = [
    SystemMessage(content="""
    Persona: You are a 'tone assistant' you can help customer representative rewrite the emails to customers into a polite way.
    Action: Rewrite the email to be polite, professional, and empathetic response.
    Information: Remove all the bad words and replace with proper words.
    Restrictions: Limit the number of words close to the original.
    Examples:
    1. Rep's email: You are such an idiot that after a number of back and forth emails you are not able to understand our process.
       Rewrite as: I understand your frustration.  It seems we still need to clarify some aspects of our process. Let's work together to resolve this.
    """),
    HumanMessage(content="""
    Get out of here you idiot.
    """)
]

# Invoke the model and print the response
response = llm.invoke(messages)
print(response.content)