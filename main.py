from fastapi import FastAPI
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.prompts import (ChatPromptTemplate,SystemMessagePromptTemplate,HumanMessagePromptTemplate)
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableParallel

from pydantic import BaseModel

load_dotenv()
app = FastAPI()

class ContentRequest(BaseModel):
    content:str


@app.get('/')
def health():
    return{'status':200}

# first
"""
Content
   ↓
Analysis Chain
   ↓
Result

"""



@app.post('/analysis')
def analysis(request:ContentRequest):
    # define moedl
    model = ChatGroq(model='openai/gpt-oss-20b')

    # define prompt

    prompt_templete = ChatPromptTemplate.from_messages([
       SystemMessagePromptTemplate.from_template("""
  You are an AI content analyst.

        Analyze the provided content and give:
        1. A short summary.
        2. The sentiment.
        3. The main topics.

        Keep the response clear and structured.
"""),
    HumanMessagePromptTemplate.from_template('{content}')
   ])

    # define parser
    parser = StrOutputParser()
    content_analysis_chain = prompt_templete | model | parser
    result_con = content_analysis_chain.invoke({"content": request.content})
    return {'data':result_con}