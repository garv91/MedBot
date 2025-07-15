from src.helper import load_pdf_file, text_split, downlaod_hugging_face_embeddgings
from pinecone import Pinecone, ServerlessSpec
from langchain_pinecone import PineconeVectorStore
from dotenv import load_dotenv
import os
from rich.traceback import install
install()



load_dotenv()    
PINECONE_API_KEY = os.environ.get('PINECONE_API_KEY')
OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY')


extracted_data = load_pdf_file(data="Data/")
text_chunks=text_split(extracted_data)
embeddings=downlaod_hugging_face_embeddgings()

print("This is the pine cone API Key : "+PINECONE_API_KEY)

pc = Pinecone(api_key=PINECONE_API_KEY)
index_name = "medbotindex"


pc.create_index(
    name=index_name,
    dimension=384, # Replace with your model dimensions
    metric="cosine", # Replace with your model metric
    spec=ServerlessSpec(
        cloud="aws",
        region="us-east-1"
    ) 
)

docsearch=PineconeVectorStore.from_documents(
    documents=text_chunks,
    index_name=index_name,
    embedding=embeddings
)