# 🤖 AI Content Intelligence

An AI-powered REST API for analyzing text content using **FastAPI, LangChain, and Groq**.

The project was built as a practical learning project to understand how **LangChain workflows and LCEL components** can be combined to build an AI processing pipeline.

---

## 🚀 Project Overview

AI Content Intelligence analyzes user-provided text and produces:

* 🌐 Language detection
* 📝 Text summary
* 😊 Sentiment classification
* 🏷️ Topic extraction
* 📊 Sentiment score

The main goal of the project is not to build a large production system, but to practice and understand **LangChain workflow concepts** through a real API.

---

## 🧠 Workflow

The application follows this workflow:

```text
                User Content
                     │
                     ▼
            Language Detection
                     │
                     ▼
          ┌─────────────────────┐
          │       Routing       │
          │   RunnableBranch   │
          └──────────┬──────────┘
                     │
                     ▼
             Parallel Analysis
                     │
          ┌──────────┼──────────┐
          ▼          ▼          ▼
       Summary    Sentiment   Topics
          │          │          │
          └──────────┼──────────┘
                     ▼
              Analysis Result
                     │
                     ▼
              Python Processing
                     │
                     ▼
               Sentiment Score
                     │
                     ▼
                Final Result
```

---

## 🔗 LangChain Concepts Used

This project focuses on the following LangChain concepts:

### 1. LCEL

LangChain Expression Language is used to connect components:

```python
prompt | model | parser
```

---

### 2. RunnableLambda

Used to integrate normal Python functions into LangChain workflows.

Example:

```python
def detect_language(content):
    ...
    
detect_language_chain = RunnableLambda(detect_language)
```

It is also used for calculating the sentiment score.

---

### 3. RunnablePassthrough

Used to pass data through the workflow without modifying it.

```python
RunnablePassthrough()
```

---

### 4. RunnablePassthrough.assign()

Used to preserve the existing dictionary and add new information.

For example:

```text
{
    "content": "I love this movie"
}
```

becomes:

```text
{
    "content": "I love this movie",
    "language": "en"
}
```

Later:

```text
{
    "content": "...",
    "language": "en",
    "analysis": {
        "summary": "...",
        "sentiment": "Positive",
        "topics": "..."
    }
}
```

---

### 5. RunnableBranch

Used to select a workflow based on a condition.

```python
RunnableBranch(
    (
        lambda x: x["language"] == "ar",
        ...
    ),
    (
        lambda x: x["language"] == "en",
        ...
    ),
    ...
)
```

The current project uses the branch primarily to practice the routing concept.

---

### 6. RunnableParallel

Used to execute multiple analysis tasks as part of the workflow:

```python
RunnableParallel(
    sentiment=chain_sentiment,
    summary=chain_summary,
    topics=chain_topics
)
```

Conceptually:

```text
              Content
                 │
       ┌─────────┼─────────┐
       ▼         ▼         ▼
    Summary   Sentiment   Topics
       └─────────┼─────────┘
                 ▼
           Combined Result
```

---

### 7. StrOutputParser

Used to convert the model output into a simple string.

```python
parser = StrOutputParser()
```

---

## 🛠️ Tech Stack

* **Python**
* **FastAPI**
* **LangChain**
* **LangChain Groq**
* **Groq**
* **Pydantic**
* **python-dotenv**

---

## 📁 Project Structure

```text
AI-Content-Intelligence/
│
├── main.py
├── .env
├── .gitignore
├── requirements.txt
└── README.md
```

> The project intentionally keeps a simple structure because it was built as a learning project focused on LangChain workflows.

---

## ⚙️ Installation

Clone the repository:

```bash
git clone https://github.com/Fady-Moawad/ai-content-intelligence.git
cd ai-content-intelligence
```

Create a virtual environment:

```bash
python -m venv venv
```

Activate it on Windows:

```bash
venv\Scripts\activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

---

## 🔐 Environment Variables

Create a `.env` file:

```env
GROQ_API_KEY=your_groq_api_key

LANGCHAIN_TRACING_V2=true
LANGCHAIN_API_KEY=your_langsmith_api_key
LANGCHAIN_PROJECT=ai-content-intelligence
```

Do not commit `.env` to GitHub.

---

## ▶️ Run the API

Start the FastAPI server:

```bash
uvicorn main:app --reload
```

The API will be available at:

```text
http://127.0.0.1:8000
```

FastAPI interactive documentation:

```text
http://127.0.0.1:8000/docs
```

---

## 📡 API Endpoints

### Health Check

```http
GET /
```

Response:

```json
{
    "status": 200
}
```

---

### Content Analysis

```http
POST /analysis
```

Request:

```json
{
    "content": "I really enjoyed this movie. It was amazing!"
}
```

Example response:

```json
{
    "data": {
        "content": "I really enjoyed this movie. It was amazing!",
        "language": "en",
        "analysis": {
            "sentiment": "Positive",
            "summary": "The user enjoyed the movie and considered it amazing.",
            "topics": "- Movie\n- Entertainment"
        },
        "score": 1.0
    }
}
```

---

## 🎯 Learning Objectives

This project helped me practice:

* Building AI APIs with FastAPI
* Working with LLMs through Groq
* Creating prompts with LangChain
* Understanding LCEL
* Building sequential chains
* Using `RunnableLambda`
* Using `RunnablePassthrough`
* Using `.assign()`
* Using `RunnableParallel`
* Using `RunnableBranch`
* Combining Python logic with LLM workflows
* Parsing LLM output
* Designing a complete AI processing flow

---

## 🔮 Next Step

The next project will focus on **Retrieval-Augmented Generation (RAG)**.

The goal is to move from:

```text
User Question
      ↓
      LLM
      ↓
    Answer
```

to:

```text
Documents
    ↓
Chunking
    ↓
Embeddings
    ↓
Vector Database
    ↓
Retrieval
    ↓
Relevant Context
    ↓
LLM
    ↓
Grounded Answer
```

This project will be built step-by-step to understand **why each component exists and how the components work together**.

---

## 📌 Project Status

**Completed — Learning Project**

The project intentionally stops here after covering the main LangChain workflow concepts it was designed to practice.