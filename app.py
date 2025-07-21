from src.helper import downlaod_hugging_face_embeddgings
from langchain_pinecone import PineconeVectorStore
from langchain.chains import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain 
from langchain_core.prompts import ChatPromptTemplate
from flask import Flask,render_template,request,jsonify
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
from src.prompt import*
import os

os.environ.pop("SSL_CERT_FILE", None)

app=Flask(__name__)   

load_dotenv

PINECONE_API_KEY = os.environ.get('PINECONE_API_KEY')
OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY')



os.environ["PINECONE_API_KEY"] = PINECONE_API_KEY   

os.environ["OPENAI_API_KEY"] = OPENAI_API_KEY



embeddings=downlaod_hugging_face_embeddgings()

docsearch=PineconeVectorStore.from_existing_index(
    index_name="medbotindex",
    embedding=embeddings
)

retriver=docsearch.as_retriever(search_type="similarity",search_kwards={"k":3})
prompt=ChatPromptTemplate.from_messages([
    ("system", system_prompt),
    ("human", "{input}")
])

chatModel = ChatOpenAI(model="gpt-4o")

question_answer_chain=create_stuff_documents_chain(chatModel,prompt)


rag_chain=create_retrieval_chain(
    retriever=retriver,
    combine_docs_chain=question_answer_chain
)

@app.route("/")
def index():
    print("Welcome to the MedBot")
    return render_template("chatbot.html")


@app.route("/chat",methods=["GET","POST"])
def chat():
     msg= request.json['message']
     input=msg;
     response = rag_chain.invoke({"input": msg})
     return jsonify({'reply':response['answer']})


if __name__ == "__main__":
    app.run(host="0.0.0.0",port=8080,debug=True)


