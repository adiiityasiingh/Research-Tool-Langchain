from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import os
import pickle
import time
import json
from typing import List, Optional
from pydantic import BaseModel
from langchain_openai import OpenAI
from langchain_anthropic import ChatAnthropic
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_community.llms import Ollama
from langchain_community.llms import HuggingFacePipeline
from langchain_huggingface import HuggingFaceEmbeddings
from langchain.chains import RetrievalQAWithSourcesChain
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import UnstructuredURLLoader
from langchain_community.vectorstores import Chroma
from transformers.pipelines import pipeline
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(title="News Research Tool API", version="1.0.0")

# Pydantic models for API requests/responses
class ProcessURLsRequest(BaseModel):
    urls: List[str]
    llm_provider: str = "OpenAI"
    embedding_provider: str = "Hugging Face (Free)"

class QuestionRequest(BaseModel):
    question: str
    llm_provider: str = "OpenAI"
    embedding_provider: str = "Hugging Face (Free)"

class ProcessResponse(BaseModel):
    success: bool
    message: str
    document_count: Optional[int] = None

class AnswerResponse(BaseModel):
    answer: str
    sources: List[str]
    chunks: List[str]

# Global variables for state management
vectorstore = None
current_llm = None
current_embeddings = None

def initialize_llm(provider: str):
    """Initialize LLM based on provider selection"""
    global current_llm
    
    if provider == "OpenAI":
        try:
            current_llm = OpenAI(temperature=0.9, max_tokens=500)
            return True
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"OpenAI Error: {str(e)}")
            
    elif provider == "Anthropic Claude":
        try:
            current_llm = ChatAnthropic(
                model_name="claude-3-sonnet-20240229",
                temperature=0.9,
                timeout=60,
                stop=None
            )
            return True
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Anthropic Error: {str(e)}")
            
    elif provider == "Google Gemini":
        try:
            current_llm = ChatGoogleGenerativeAI(
                model="gemini-1.5-pro",
                temperature=0.9,
                max_tokens=500
            )
            return True
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Google Gemini Error: {str(e)}")
            
    elif provider == "Ollama (Local)":
        try:
            current_llm = Ollama(model="llama2", temperature=0.9)
            return True
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Ollama Error: {str(e)}")

    elif provider == "Local HuggingFace":
        try:
            pipe = pipeline(
                "text-generation",
                model="microsoft/DialoGPT-small",
                max_new_tokens=200,
                temperature=0.9,
                do_sample=True,
                pad_token_id=50256
            )
            current_llm = HuggingFacePipeline(pipeline=pipe)
            return True
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Local Model Error: {str(e)}")
    
    return False

def initialize_embeddings(provider: str):
    """Initialize embeddings based on provider selection"""
    global current_embeddings
    
    if provider == "Hugging Face (Free)":
        try:
            current_embeddings = HuggingFaceEmbeddings(
                model_name="sentence-transformers/all-MiniLM-L6-v2",
                model_kwargs={'device': 'cpu'}
            )
            return True
        except Exception as e:
            try:
                from langchain_openai import OpenAIEmbeddings
                current_embeddings = OpenAIEmbeddings()
                return True
            except:
                raise HTTPException(status_code=400, detail="No working embeddings provider found")
                
    elif provider == "OpenAI":
        try:
            from langchain_openai import OpenAIEmbeddings
            current_embeddings = OpenAIEmbeddings()
            return True
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"OpenAI Embeddings Error: {str(e)}")
    
    return False

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    """Serve the main HTML interface"""
    html_content = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>News Research Tool 📈</title>
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <style>
            body { font-family: Arial, sans-serif; margin: 0; padding: 20px; background: #f5f5f5; }
            .container { max-width: 1200px; margin: 0 auto; background: white; padding: 20px; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }
            .header { text-align: center; margin-bottom: 30px; }
            .config-section { margin-bottom: 30px; padding: 20px; background: #f8f9fa; border-radius: 8px; }
            .form-group { margin-bottom: 15px; }
            label { display: block; margin-bottom: 5px; font-weight: bold; }
            select, input, textarea { width: 100%; padding: 10px; border: 1px solid #ddd; border-radius: 4px; box-sizing: border-box; }
            button { background: #007bff; color: white; padding: 10px 20px; border: none; border-radius: 4px; cursor: pointer; margin: 5px; }
            button:hover { background: #0056b3; }
            .url-input { margin-bottom: 10px; }
            .response { margin-top: 20px; padding: 15px; background: #e9ecef; border-radius: 4px; }
            .error { background: #f8d7da; color: #721c24; }
            .success { background: #d4edda; color: #155724; }
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>Market News Research Tool 📈</h1>
            </div>
            
            <div class="config-section">
                <h3>Configuration</h3>
                <div class="form-group">
                    <label for="llm-provider">LLM Provider:</label>
                    <select id="llm-provider">
                        <option value="OpenAI">OpenAI</option>
                        <option value="Anthropic Claude">Anthropic Claude</option>
                        <option value="Google Gemini">Google Gemini</option>
                        <option value="Ollama (Local)">Ollama (Local)</option>
                        <option value="Local HuggingFace">Local HuggingFace</option>
                    </select>
                </div>
                <div class="form-group">
                    <label for="embedding-provider">Embedding Provider:</label>
                    <select id="embedding-provider">
                        <option value="Hugging Face (Free)">Hugging Face (Free)</option>
                        <option value="OpenAI">OpenAI</option>
                    </select>
                </div>
            </div>
            
            <div class="config-section">
                <h3>News Article URLs</h3>
                <div id="url-inputs">
                    <div class="url-input">
                        <input type="url" placeholder="Enter URL 1" class="url-field">
                    </div>
                    <div class="url-input">
                        <input type="url" placeholder="Enter URL 2" class="url-field">
                    </div>
                    <div class="url-input">
                        <input type="url" placeholder="Enter URL 3" class="url-field">
                    </div>
                </div>
                <button onclick="processURLs()">Process URLs</button>
                <button onclick="clearKnowledgeBase()">🗑️ Clear Knowledge Base</button>
            </div>
            
            <div class="config-section">
                <h3>Ask Questions</h3>
                <div class="form-group">
                    <textarea id="question" rows="4" placeholder="Enter your question here..."></textarea>
                </div>
                <button onclick="askQuestion()">🔍 Search for Answer</button>
            </div>
            
            <div id="response" class="response" style="display: none;"></div>
        </div>
        
        <script>
            async function processURLs() {
                const urls = Array.from(document.querySelectorAll('.url-field')).map(input => input.value).filter(url => url.trim());
                const llmProvider = document.getElementById('llm-provider').value;
                const embeddingProvider = document.getElementById('embedding-provider').value;
                
                const response = await fetch('/process-urls', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ urls, llm_provider: llmProvider, embedding_provider: embeddingProvider })
                });
                
                const result = await response.json();
                showResponse(result.message, result.success ? 'success' : 'error');
            }
            
            async function askQuestion() {
                const question = document.getElementById('question').value;
                const llmProvider = document.getElementById('llm-provider').value;
                const embeddingProvider = document.getElementById('embedding-provider').value;
                
                if (!question.trim()) {
                    showResponse('Please enter a question', 'error');
                    return;
                }
                
                const response = await fetch('/ask-question', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ question, llm_provider: llmProvider, embedding_provider: embeddingProvider })
                });
                
                const result = await response.json();
                if (result.success) {
                    showResponse(`Answer: ${result.answer}<br><br>Sources: ${result.sources.join(', ')}`, 'success');
                } else {
                    showResponse(result.message, 'error');
                }
            }
            
            async function clearKnowledgeBase() {
                const response = await fetch('/clear-knowledge-base', { method: 'POST' });
                const result = await response.json();
                showResponse(result.message, result.success ? 'success' : 'error');
            }
            
            function showResponse(message, type) {
                const responseDiv = document.getElementById('response');
                responseDiv.innerHTML = message;
                responseDiv.className = `response ${type}`;
                responseDiv.style.display = 'block';
            }
        </script>
    </body>
    </html>
    """
    return html_content

@app.post("/process-urls", response_model=ProcessResponse)
async def process_urls(request: ProcessURLsRequest):
    """Process URLs and create knowledge base"""
    global vectorstore, current_llm, current_embeddings
    
    try:
        # Initialize LLM and embeddings
        if not initialize_llm(request.llm_provider):
            return ProcessResponse(success=False, message="Failed to initialize LLM")
        
        if not initialize_embeddings(request.embedding_provider):
            return ProcessResponse(success=False, message="Failed to initialize embeddings")
        
        # Filter out empty URLs
        valid_urls = [url for url in request.urls if url.strip()]
        
        if not valid_urls:
            return ProcessResponse(success=False, message="Please enter at least one valid URL.")
        
        # Load and process data
        loader = UnstructuredURLLoader(urls=valid_urls)
        data = loader.load()
        
        # Split text into chunks
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200,
            length_function=len
        )
        docs = text_splitter.split_documents(data)
        
        # Create or update vectorstore
        if vectorstore is None:
            vectorstore = Chroma.from_documents(
                documents=docs,
                embedding=current_embeddings,
                persist_directory="./chroma_db"
            )
        else:
            vectorstore.add_documents(docs)
        
        vectorstore.persist()
        
        return ProcessResponse(
            success=True,
            message=f"✅ Successfully processed {len(valid_urls)} URLs and created knowledge base with {len(docs)} documents",
            document_count=len(docs)
        )
        
    except Exception as e:
        return ProcessResponse(success=False, message=f"Error processing URLs: {str(e)}")

@app.post("/ask-question")
async def ask_question(request: QuestionRequest):
    """Ask a question and get answer from knowledge base"""
    global vectorstore, current_llm, current_embeddings
    
    try:
        if vectorstore is None:
            return {"success": False, "message": "No knowledge base available. Please process URLs first."}
        
        if current_llm is None:
            if not initialize_llm(request.llm_provider):
                return {"success": False, "message": "Failed to initialize LLM"}
        
        if current_embeddings is None:
            if not initialize_embeddings(request.embedding_provider):
                return {"success": False, "message": "Failed to initialize embeddings"}
        
        # Create QA chain
        chain = RetrievalQAWithSourcesChain.from_llm(
            llm=current_llm,
            retriever=vectorstore.as_retriever(search_kwargs={"k": 3})
        )
        
        # Get answer
        result = chain({"question": request.question})
        
        return {
            "success": True,
            "answer": result["answer"],
            "sources": result["sources"].split(", ") if result["sources"] else [],
            "chunks": []
        }
        
    except Exception as e:
        return {"success": False, "message": f"Error getting answer: {str(e)}"}

@app.post("/clear-knowledge-base")
async def clear_knowledge_base():
    """Clear the knowledge base"""
    global vectorstore
    
    try:
        vectorstore = None
        if os.path.exists("./chroma_db"):
            import shutil
            shutil.rmtree("./chroma_db")
        
        return {"success": True, "message": "Knowledge base cleared successfully!"}
    except Exception as e:
        return {"success": False, "message": f"Error clearing knowledge base: {str(e)}"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 