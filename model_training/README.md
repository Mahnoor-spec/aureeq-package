# Model Training & Data Strategy

To make "Aureeq" answer questions based on your specific data, we will implement a **Knowledge Base (RAG)** system. This is the industry standard for AI Sales Agents as it ensures accuracy and allows instant updates to your product data without re-training for hours.

## 1. Project Structure
```
/model_training
  /data           <-- Place your PDF, TXT, CSV, or JSON files here
  /scripts        <-- Python scripts to process data
  /vector_store   <-- Database where the AI "memory" is stored
```

## 2. Approach: Retrieval Augmented Generation (RAG)
Instead of expensive "Fine-Tuning" (which usually teaches style, not facts), we will use **RAG**.

1.  **Ingest**: We read your files from the `/data` folder.
2.  **Embed**: We convert text into numbers (vectors) representing meaning.
3.  **Store**: We save these in a local Vector Database (e.g., ChromaDB or FAISS).
4.  **Query**: When a user asks a question, we:
    - Search the database for relevant info.
    - Feed that info to the LLM (OpenAI/Llama).
    - The LLM answers using *only* your data.

## 3. Technology Stack
- **Language**: Python (Best for AI/Data processing).
- **Framework**: LangChain or LlamaIndex.
- **Database**: ChromaDB (Local, easy to setup).
- **Model**: OpenAI (GPT-4o) or Local (Llama 3 via Ollama).

## 4. Next Steps for You
1.  **Upload Data**: Please provide the files (PDFs, docs, price lists) you want the agent to learn from.
2.  **Choose Backend**:
    - **Cloud**: Use OpenAI/Azure (High accuracy, cost per message).
    - **Local**: Use Ollama (Free, runs on your PC, requires good GPU).
