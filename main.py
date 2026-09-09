from fastapi import FastAPI
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.prompts import (ChatPromptTemplate,SystemMessagePromptTemplate,HumanMessagePromptTemplate)
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import( RunnableParallel , RunnablePassthrough, RunnableLambda, RunnableBranch)
import os
from pydantic import BaseModel
from typing import Literal

load_dotenv()
app = FastAPI()

# LangSmith
os.getenv("LANGCHAIN_TRACING_V2")
os.getenv("LANGCHAIN_API_KEY")

class ContentRequest(BaseModel):
    content:str

# class SentimentResult(BaseModel):
#     sentiment : str = Field(
#         description="The sentiment of the content. Must be Positive, Negative, or Neutral."
#     )

# more restracted
class SentimentOutput(BaseModel):
    sentiment : Literal["Positive", "Negative", "Neutral"]
    
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
    model = ChatGroq(model='openai/gpt-oss-20b',api_key=os.getenv("GROQ_API_KEY"))
    # structured_model = model.with_structured_output(SentimentOutput)

    # define language
    def detect_language(content):
      arabic = any(
        '\u0600' <= char <= '\u06FF'
        for char in content
    )

      english = any(
        ('a' <= char.lower() <= 'z')
        for char in content
    )

      if arabic:
        return "ar"
      elif english:
        return "en"
      else:
        return "none"

    detect_language_chain = RunnableLambda(detect_language)

    language_detection= RunnablePassthrough.assign(
       language= detect_language_chain
    )
    
    routing = RunnableBranch(
       (
          lambda  x: x['language']=='ar',
          RunnablePassthrough()
       ),
       (
          lambda  x: x['language']=='en',
            RunnablePassthrough()
       ),
       RunnablePassthrough()
    )

    routing_chain = language_detection | routing
    # define prompt all task
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

    # summary
    prompt_templete_summary = ChatPromptTemplate.from_messages([
       SystemMessagePromptTemplate.from_template("""
        You are an AI content summarization assistant.
        Summarize the provided content in 2-3 concise sentences.
        Do not add information that is not present in the content.
        """),
    HumanMessagePromptTemplate.from_template('{content}')
   ])

    # sentiment
    prompt_templete_sentiment = ChatPromptTemplate.from_messages([
    SystemMessagePromptTemplate.from_template("""
    You are a sentiment classification assistant.
    Classify the sentiment of the content as exactly ONE of these values:
    Positive
    Negative
    Neutral
    IMPORTANT:
    - Return ONLY ONE WORD.
    - Do not explain your answer.
    - Do not use Markdown.
    - Do not use **.
    - Do not add punctuation.
    - Do not add any extra text.
    """),
    HumanMessagePromptTemplate.from_template('{content}')
]) 
    
    # topics
    prompt_templete_topics = ChatPromptTemplate.from_messages([
       SystemMessagePromptTemplate.from_template("""
        You are a topic extraction assistant.
        Extract the main topics discussed in the content.
        Return them as a short bullet list.
        """),
    HumanMessagePromptTemplate.from_template('{content}')
   ])

    # define parser
    parser = StrOutputParser()

    #corrention function
    def calc_score(data):
     sentiment = data["analysis"]["sentiment"].strip().lower()

     if sentiment == "positive":
        return 1.0
     elif sentiment == "negative":
        return 0.0
     elif sentiment == "neutral":
        return 0.5
     else:
        return None
     
    score_cahin = RunnableLambda(calc_score)

    # pipline multi models
    chain_summary = prompt_templete_summary | model | parser
    chain_sentiment = prompt_templete_sentiment | model | parser
    chain_topics = prompt_templete_topics | model | parser

    # paralle runnable
    parallel_analysis =RunnableParallel(
        sentiment=chain_sentiment,
        summary=chain_summary,
        topics=chain_topics
        )

    #runnable pass through
    content_analysis_chain = routing_chain | RunnablePassthrough.assign(analysis=parallel_analysis) | RunnablePassthrough.assign(score = score_cahin)

    result_con = content_analysis_chain.invoke({"content": request.content})
    return {'data':result_con}

"""
RunnablePassthrough.assign(analysis=parallel_analysis)

RunnablePassthrough => "content": "...",
.assign(analysis=parallel_analysis) => take content + output analysis
output => "content": "...","analysis":"..."

next RunnablePassthrough.assign(score = score_cahin)
first input ignore 
RunnablePassthrough =>"content": "...","analysis":"..." 
.assign(analysis=parallel_analysis) => "content": "...","analysis":"..."   + score

"""