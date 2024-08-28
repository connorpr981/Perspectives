import logging
from typing import List, Dict, Any
from firebase_admin import firestore
from _helpers.question_helper import get_enrichment_questions, add_answer_to_question
from _llm.models.message_models import Messages
from _llm.llm_processing import get_response
from pydantic import BaseModel, Field
from datetime import datetime
import os
from openai import OpenAI

current_date = datetime.now().strftime("%Y-%m-%d")

class EnrichmentAnswer(BaseModel):
    answer: str = Field(..., description="The answer to the enrichment question")

ANTHROPIC_SYSTEM_PROMPT = """You are an expert in providing concise, informative answers to enrichment questions. Your task is to answer the given question with accurate and relevant information. Today's date is {current_date}.

Guidelines for Answering Enrichment Questions:
1. Provide a clear, concise answer that directly addresses the question.
2. Limit your response to 1-3 sentences.
3. Focus on factual information, established concepts, or well-documented historical or cultural context.
4. Use simple, straightforward language that is easy to understand.
5. If the question is about a specific statistic or fact that may have changed since your last update, mention that the information is based on your last update and may not reflect the most current data.
6. Never use first-person pronouns (I, me, my, etc.) in your answers.
7. If you don't have enough information to answer the question accurately, respond with: "The answer to this question could not be found based on the available information."

Remember:
- Stick to verified, factual information.
- Do not speculate or offer personal opinions.
- Always write in the third person, as if providing an objective, encyclopedic entry.
"""

ANTHROPIC_USER_PROMPT = """Please answer the following enrichment question:

Question: {question}

Answer:"""

PERPLEXITY_SYSTEM_PROMPT = """You are an expert in providing up-to-date, concise, and informative answers to enrichment questions. Your task is to answer the given question with the most current and accurate information available. Today's date is {current_date}.

Guidelines for Answering Enrichment Questions:
1. Provide a clear, concise answer that directly addresses the question with the most recent data available.
2. Limit your response to 1-3 sentences.
3. Focus on current factual information, recent statistics, or the latest developments related to the question.
4. Use simple, straightforward language that is easy to understand.
5. If possible, include the date or year of the information you're providing to emphasize its currency.
6. Never use first-person pronouns (I, me, my, etc.) in your answers.
7. If you don't have enough current information to answer the question accurately, respond with: "The answer to this question could not be directly found."

Remember:
- Prioritize the most recent and reliable information available.
- If there have been significant recent changes or developments related to the question, mention them briefly.
- Always write in the third person, as if providing an objective, encyclopedic entry.
"""

PERPLEXITY_USER_PROMPT = """Please answer the following enrichment question with the most up-to-date information available:

Question: {question}

Answer:"""

def simulate_answering_enrichment_questions(transcript_id: str):
    db = firestore.client()
    transcript_ref = db.collection('transcripts').document(transcript_id)
    
    questions = get_enrichment_questions(transcript_ref)
    
    for question in questions:
        question_data = question.to_dict()
        requires_current_info = question_data.get('requires_current_info', False)
        
        if requires_current_info:
            answer = answer_current_info_question(question_data['question'])
        else:
            answer = answer_static_info_question(question_data['question'])
        
        add_answer_to_question(question.reference, answer)
    
    logging.info(f"Simulated answering {len(questions)} enrichment questions for transcript {transcript_id}")

def answer_current_info_question(question: str) -> str:
    messages = Messages()
    messages.add_system_message(PERPLEXITY_SYSTEM_PROMPT.format(current_date=current_date))
    messages.add_user_message(PERPLEXITY_USER_PROMPT.format(question=question))
    
    client = OpenAI(api_key=os.getenv("PERPLEXITY_API_KEY"), base_url="https://api.perplexity.ai")

    try:
        response = client.chat.completions.create(
            model="llama-3.1-sonar-huge-128k-online",
            messages=messages.to_api_format(),
        )
        answer = response.choices[0].message.content
        logging.info(f"Successfully generated answer for current info question: {question}\n{answer}")
        return EnrichmentAnswer(answer=answer).answer
    except Exception as e:
        error_message = f"Error in answer_current_info_question: {str(e)}"
        logging.error(error_message)
        return "The answer to this question could not be found due to an error in processing."

def answer_static_info_question(question: str) -> str:
    messages = Messages()
    messages.add_system_message(ANTHROPIC_SYSTEM_PROMPT.format(current_date=current_date))
    messages.add_user_message(ANTHROPIC_USER_PROMPT.format(question=question))
    
    response, _ = get_response(
        provider="anthropic",
        messages=messages,
        response_model=EnrichmentAnswer
    )
    
    return response.answer
