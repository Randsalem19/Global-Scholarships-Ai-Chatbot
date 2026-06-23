import json
import os
from typing import List, Dict
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from openai import OpenAI
from pydantic import BaseModel

load_dotenv()

app = FastAPI(title="ScholarAI Backend")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# باستخدام Groq ليكون مجانياً وسريعاً جداً
client = OpenAI(
    api_key=os.getenv("GROQ_API_KEY"),
    base_url="https://api.groq.com/openai/v1"
)

class ChatRequest(BaseModel):
    message: str

def load_scholarships() -> List[Dict]:
    with open("data.json", "r", encoding="utf-8") as file:
        return json.load(file)

def search_scholarships(query: str, scholarships: List[Dict]) -> List[Dict]:
    query_words = query.lower().split()
    results = []
    for scholarship in scholarships:
        searchable_text = " ".join([
            scholarship["name"],
            scholarship["country"],
            scholarship["degree_level"],
            " ".join(scholarship["majors"]),
            scholarship["description"]
        ]).lower()
        if any(word in searchable_text for word in query_words):
            results.append(scholarship)
    return results[:3]

@app.post("/chat")
async def chat(request: ChatRequest):
    try:
        scholarships = load_scholarships()
        matches = search_scholarships(request.message, scholarships)
        
        context = ""
        if matches:
            for item in matches:
                context += f"- {item['name']} in {item['country']} ({item['degree_level']}): {item['description']}\n"
        else:
            context = "No direct exact matches found in the specific database. Use your broad knowledge to suggest suitable real scholarships."

        system_prompt = f"""
You are "ScholarAI", a highly professional Global Scholarships AI Advisor developed by Rand Salem.
Your goal is to guide students to find fully-funded scholarships.

CRITICAL RULES:
1. If the user speaks Arabic, YOU MUST REPLY IN PROFESSIONAL ARABIC.
2. If the user speaks English, reply in English.
3. Base your recommendations on this context if available: 
{context}
4. If the context is empty, use your internal knowledge to recommend actual 2026 scholarships based on the user's request.
5. Format your response beautifully using bullet points.
6. If you provide any website URLs, ALWAYS format them strictly as Markdown links like this: [Website Name](URL).
"""

        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile", # أسرع وأذكى نموذج لغوي متاح مجاناً
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": request.message}
            ],
            temperature=0.5
        )

        return {
            "reply": response.choices[0].message.content
        }

    except Exception as error:
        raise HTTPException(status_code=500, detail=str(error))