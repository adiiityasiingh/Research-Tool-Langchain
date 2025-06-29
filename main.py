import os
import streamlit as st
import pickle
import time
from langchain_openai import OpenAI
from langchain_anthropic import ChatAnthropic
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_community.llms import Ollama
from langchain_community.llms import HuggingFacePipeline
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain.chains import RetrievalQAWithSourcesChain
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import UnstructuredURLLoader
from langchain_community.vectorstores import FAISS
from transformers.pipelines import pipeline

from dotenv import load_dotenv
load_dotenv() 
 # take environment variables from .env

st.title("RockyBot: News Research Tool 📈")
st.sidebar.title("Configuration")

# LLM Provider Selection
llm_provider = st.sidebar.selectbox(
    "Choose LLM Provider:",
    ["OpenAI", "Anthropic Claude", "Google Gemini", "Ollama (Local)", "Local HuggingFace"],
    help="Select your preferred LLM provider"
)

# Initialize LLM based on selection
llm = None
if llm_provider == "OpenAI":
    try:
        llm = OpenAI(temperature=0.9, max_tokens=500)
    except Exception as e:
        st.sidebar.error(f"OpenAI Error: {str(e)}")
        st.sidebar.info("Please check your OpenAI API key in .env file")
        
elif llm_provider == "Anthropic Claude":
    try:
        llm = ChatAnthropic(
            model_name="claude-3-sonnet-20240229",
            temperature=0.9,
            timeout=60,
            stop=None
        )
    except Exception as e:
        st.sidebar.error(f"Anthropic Error: {str(e)}")
        st.sidebar.info("Please add ANTHROPIC_API_KEY to your .env file")
        
elif llm_provider == "Google Gemini":
    try:
        llm = ChatGoogleGenerativeAI(
            model="gemini-1.5-pro",
            temperature=0.9,
            max_tokens=500
        )
    except Exception as e:
        st.sidebar.error(f"Google Gemini Error: {str(e)}")
        st.sidebar.info("Please add GOOGLE_API_KEY to your .env file")
        
elif llm_provider == "Ollama (Local)":
    try:
        llm = Ollama(model="llama2", temperature=0.9)
    except Exception as e:
        st.sidebar.error(f"Ollama Error: {str(e)}")
        st.sidebar.info("Please install Ollama and run: ollama pull llama2")

elif llm_provider == "Local HuggingFace":
    try:
        with st.spinner("Loading local model..."):
            # Use a small, fast model
            pipe = pipeline(
                "text-generation",
                model="microsoft/DialoGPT-small",
                max_new_tokens=200,
                temperature=0.9,
                do_sample=True,
                pad_token_id=50256
            )
            llm = HuggingFacePipeline(pipeline=pipe)
        st.sidebar.success("Local model loaded successfully!")
    except Exception as e:
        st.sidebar.error(f"Local Model Error: {str(e)}")
        st.sidebar.info("This requires downloading a small model (~500MB)")

# Embeddings Selection
embedding_provider = st.sidebar.selectbox(
    "Choose Embedding Provider:",
    ["Hugging Face (Free)", "OpenAI"],
    help="Select your preferred embedding provider"
)

# Initialize embeddings
embeddings = None
if embedding_provider == "Hugging Face (Free)":
    try:
        embeddings = HuggingFaceEmbeddings(
            model_name="sentence-transformers/all-MiniLM-L6-v2",
            model_kwargs={'device': 'cpu'}
        )
    except Exception as e:
        st.sidebar.error(f"Hugging Face Embeddings Error: {str(e)}")
        st.sidebar.info("This will use OpenAI embeddings as fallback")
        try:
            from langchain_openai import OpenAIEmbeddings
            embeddings = OpenAIEmbeddings()
        except:
            st.sidebar.error("No working embeddings provider found")
            
elif embedding_provider == "OpenAI":
    try:
        from langchain_openai import OpenAIEmbeddings
        embeddings = OpenAIEmbeddings()
    except Exception as e:
        st.sidebar.error(f"OpenAI Embeddings Error: {str(e)}")

st.sidebar.title("News Article URLs")

urls = []
for i in range(3):
    url = st.sidebar.text_input(f"URL {i+1}")
    urls.append(url)

process_url_clicked = st.sidebar.button("Process URLs")
file_path = "faiss_store.pkl"

main_placeholder = st.empty()

if process_url_clicked:
    # Check if we have working LLM and embeddings
    if llm is None:
        st.error("Please configure a working LLM provider first.")
    elif embeddings is None:
        st.error("Please configure a working embeddings provider first.")
    else:
        # Filter out empty URLs
        valid_urls = [url for url in urls if url.strip()]
        
        if not valid_urls:
            st.error("Please enter at least one valid URL.")
        else:
            try:
                # load data
                loader = UnstructuredURLLoader(urls=valid_urls)
                main_placeholder.text("Data Loading...Started...✅✅✅")
                data = loader.load()
                
                if not data:
                    st.error("No content could be loaded from the provided URLs. Please check if the URLs are accessible and contain text content.")
                else:
                    # split data
                    text_splitter = RecursiveCharacterTextSplitter(
                        separators=['\n\n', '\n', '.', ','],
                        chunk_size=1000
                    )
                    main_placeholder.text("Text Splitter...Started...✅✅✅")
                    docs = text_splitter.split_documents(data)
                    
                    if not docs:
                        st.error("No text chunks could be created from the loaded content.")
                    else:
                        # create embeddings and save it to FAISS index
                        main_placeholder.text("Embedding Vector Started Building...✅✅✅")
                        
                        # Create FAISS index with error handling
                        try:
                            vectorstore = FAISS.from_documents(docs, embeddings)
                            time.sleep(2)

                            # Save the FAISS index to a pickle file
                            with open(file_path, "wb") as f:
                                pickle.dump(vectorstore, f)
                            
                            st.success("URLs processed successfully! You can now ask questions.")
                        except Exception as e:
                            st.error(f"Error creating embeddings: {str(e)}")
                            st.info("This might be due to empty documents or API issues. Please check your URLs and try again.")
                            
            except Exception as e:
                st.error(f"Error loading URLs: {str(e)}")
                st.info("Please check if the URLs are valid and accessible.")

query = main_placeholder.text_input("Question: ")
search_button = st.button("🔍 Search for Answer")

if search_button and query:
    if llm is None:
        st.error("Please configure a working LLM provider first.")
    elif os.path.exists(file_path):
        try:
            with st.spinner("🔍 Searching through documents..."):
                with open(file_path, "rb") as f:
                    vectorstore = pickle.load(f)
                    chain = RetrievalQAWithSourcesChain.from_llm(llm=llm, retriever=vectorstore.as_retriever())
                    
            with st.spinner("🤖 Generating answer..."):
                result = chain({"question": query}, return_only_outputs=True)
                
            # result will be a dictionary of this format --> {"answer": "", "sources": [] }
            st.header("Answer")
            st.write(result["answer"])

            # Display sources, if available
            sources = result.get("sources", "")
            if sources:
                st.subheader("Sources:")
                sources_list = sources.split("\n")  # Split the sources by newline
                for source in sources_list:
                    st.write(source)
        except Exception as e:
            st.error(f"Error processing query: {str(e)}")
    else:
        st.warning("Please process some URLs first before asking questions.")