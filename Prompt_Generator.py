from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from google import genai
import os


# FastAPI 앱 초기화
app = FastAPI()

# CORS 설정 (로컬 환경에서 프론트엔드 HTML이 백엔드 API에 접근할 수 있도록 허용)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Gemini 클라이언트 초기화 
# 환경 변수에 GEMINI_API_KEY가 설정되어 있어야 함
#client = genai.Client()

# 프론트엔드에서 받을 데이터 모델
class PromptRequest(BaseModel):
    draft_prompt: str

@app.post("/api/refine_prompt")
async def refine_prompt(request: PromptRequest):
    # Gemini에게 번역 및 프롬프트 다듬기를 지시하는 메타 프롬프트
    meta_prompt = f"""
    You are an expert AI prompt engineer. 
    Below is a draft prompt template containing a mix of English structure and Korean user input.
    
    Your task:
    1. Translate the Korean text (Context, Request, Examples, etc.) into precise, professional, and highly effective English suitable for instructing an LLM.
    2. Refine the overall structure to ensure maximum clarity and performance.
    3. Keep the structural constraints (Role, Task, Constraints, Output Format).
    4. DO NOT answer the user's actual question. ONLY output the final, polished English prompt template.
    
    [Draft Prompt]
    {request.draft_prompt}
    """
    
    # Gemini API 호출 (Gemini 2.5 Flash 모델이 번역 및 텍스트 처리에 빠르고 적합함)
    response = client.models.generate_content(
        model='gemini-2.5-flash',
        contents=meta_prompt,
    )
    
    return {"refined_prompt": response.text.strip()}
