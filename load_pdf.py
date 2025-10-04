from langchain_community.document_loaders import PyPDFLoader

def load_pdf(what: str = "apple") -> str:
    docs = {
        "apple" : [
            "content/a411a029-368f-4479-b416-25c404acca3d.pdf", 
            "content/b986f1de-d226-4e8e-9304-29a8458440ec.pdf"
        ],
        "google" : [
            "content/goog-10-q-q1-2025.pdf",
            "content/goog-10-q-q2-2025.pdf"
        ]
    }
    
    requested_docs = [doc for doc_list in docs.values() for doc in doc_list] if what == "all" else docs.get(what, [])

    loaded_documents = []
    for filename in requested_docs:
        loader = PyPDFLoader(filename)
        loaded_documents.extend(loader.load())

    combined_text = ""
    for doc in loaded_documents:
        combined_text += doc.page_content

    print(f"Documents loaded and combined: {requested_docs}")
    return combined_text

def load_pdf_docs(what: str = "apple") -> list:
    docs = {
        "apple" : [
            "content/a411a029-368f-4479-b416-25c404acca3d.pdf", 
            "content/b986f1de-d226-4e8e-9304-29a8458440ec.pdf"
        ],
        "google" : [
            "content/goog-10-q-q1-2025.pdf",
            "content/goog-10-q-q2-2025.pdf"
        ]
    }
    
    requested_docs = [doc for doc_list in docs.values() for doc in doc_list] if what == "all" else docs.get(what, [])

    loaded_documents = []
    for filename in requested_docs:
        loader = PyPDFLoader(filename)
        loaded_documents.extend(loader.load())


    print(f"Documents loaded and combined: {requested_docs}")
    return loaded_documents
