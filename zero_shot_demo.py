import os
os.environ['GRPC_VERBOSITY'] = 'NONE'

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage, SystemMessage
import google.generativeai as genai
from setup_env import setup_env

setup_env()

#List models
# list_models() # Commented out as the user has already seen the list

# Initialize the Chat Model
# Make sure to replace "models/gemini-1.5-pro-latest" with a model from the list you generated if needed
llm = ChatGoogleGenerativeAI(model="models/gemini-2.5-pro-preview-03-25")

# Create a system message and a human message
messages = [
    SystemMessage(content="""
    Persona: You are expert at solving math puzzles.
    Action: Given a user prompt, you will identify and solve the math puzzle.
    Information: The given prompt will always be a math puzzle. You need to parse out the puzzle, explain the puzzle in math, and then solve it.
    Restrictions:
    1. Show your work and list any intermediate steps. Record the final answer as 'Final Answer'.
    2. Make sure the results make sense in terms of units. If the results come out as fractions, the final answer may need to be rounded up/down.
    """),
    HumanMessage(content="""The puzzle is:
    "A family of four (Mom, Dad, Son, and Daughter) is at the grocery store.
    ​The Son's cart has 2 bags of chips.
    ​The Daughter's cart has twice as many bags of chips as her brother's.
    ​Dad's cart has one more bag than his son and daughter's combined total.
    ​Mom's cart has half the total number of bags of chips from all three of the other family members.
    ​The Question: How many bags of chips does the family have in total?"
    """)
]

# Invoke the model and print the response
response = llm.invoke(messages)
print(response.content)