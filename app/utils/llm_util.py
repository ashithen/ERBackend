import json

from google import genai
from google.genai import types
from tenacity import retry, wait_fixed, stop_after_attempt

from app.core.config import settings
from app.models.data_model import LongQuestionData
from app.utils import path_util

doc_process_prompt: str = path_util.get_resource("doc_process_prompt.txt")
long_question_feedback_prompt: str = path_util.get_resource("long_question_feedback_prompt.txt")

genai_client = genai.Client(api_key=settings.gemini_api_key)


@retry(wait=wait_fixed(1), stop=stop_after_attempt(3))
async def generate_doc_result(doc_text: str) -> dict:
    contents = [
        types.Content(
            role="user",
            parts=[
                types.Part.from_text(text=doc_text)
            ],
        ),
    ]
    generate_content_config = types.GenerateContentConfig(
        response_mime_type="application/json",
        system_instruction=[
            types.Part.from_text(text=doc_process_prompt),
        ],
    )
    response = genai_client.models.generate_content(model=settings.llm_model, contents=contents,
                                                    config=generate_content_config)
    if not response or not response.text:
        raise Exception("Doc process GenAI request failed")
    return json.loads(response.text)


@retry(wait=wait_fixed(1), stop=stop_after_attempt(3))
async def generate_long_question_feedback(long_question: LongQuestionData, user_answer: str) -> str:
    user_content = {
        "question": long_question.question,
        "valid_answer": long_question.answer,
        "student_answer": user_answer
    }
    contents = [
        types.Content(
            role="user",
            parts=[
                types.Part.from_text(text=json.dumps(user_content))
            ],
        ),
    ]
    generate_content_config = types.GenerateContentConfig(
        response_mime_type="application/json",
        system_instruction=[
            types.Part.from_text(text=long_question_feedback_prompt),
        ],
    )
    response = genai_client.models.generate_content(model=settings.llm_model, contents=contents,
                                                    config=generate_content_config)
    if not response or not response.text:
        raise Exception("Long Question Feedback GenAI request failed")
    return response.text
