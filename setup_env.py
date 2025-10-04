import os
from dotenv import load_dotenv
# We only need the top-level package for list_models and configure
from google.generativeai import list_models, configure 

def setup_env(verbose: bool = False):
  os.environ['GRPC_VERBOSITY'] = 'NONE'
  # 1. Load the environment variables from the .env file.
  load_dotenv() 

  # Read the key from the environment
  google_api_key = os.getenv('GOOGLE_API_KEY')

  # 2. **CRITICAL FIX: Explicitly configure the SDK**
  if google_api_key:
    configure(api_key=google_api_key) 
    if verbose:
      print("Google GenAI configured successfully.")
  
  # ... (Rest of your LangChain setup can remain)
  os.environ['LANGCHAIN_TRACING_V2'] = os.getenv('LANGCHAIN_TRACING_V2', 'true')
  os.environ['LANGCHAIN_PROJECT'] = os.getenv('LANGCHAIN_PROJECT', 'langchain-demo')


  if verbose:
    print(f"Google API Key loaded: {bool(google_api_key)}")
    print(f"LangChain API Key loaded: {bool(os.getenv('LANGCHAIN_API_KEY'))}")

    # List models
    if google_api_key:
      print("\nAvailable Models:")
      try:
          # This will now succeed because configure() was called
          for m in list_models(): 
              print(f"- {m.name}")
      except Exception as e:
          print(f"Error listing models: {e}")
    else:
      print("Cannot list models: GOOGLE_API_KEY is missing.")


if __name__ == "__main__":
  setup_env(verbose=True)