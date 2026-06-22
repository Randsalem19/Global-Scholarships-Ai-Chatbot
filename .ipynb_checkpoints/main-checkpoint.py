import json
import os
from typing import List, Dict

from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from openai import OpenAI
from pydantic import BaseModel

load_dotenv()

app = FastAPI(title="Global Scholarships AI Chatbot")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


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


def format_context(matches: List[Dict]) -> str:
    if not matches:
        return "No matching scholarships found in the database."

    context = ""
    for item in matches:
        context += f"""
Scholarship Name: {item['name']}
Country: {item['country']}
Degree Level: {item['degree_level']}
Majors: {', '.join(item['majors'])}
Description: {item['description']}
---
"""
    return context


@app.post("/chat")
async def chat(request: ChatRequest):
    try:
        scholarships = load_scholarships()
        matches = search_scholarships(request.message, scholarships)
        rag_context = format_context(matches)

        system_prompt = f"""
You are Global Scholarships AI Chatbot, also called المستشار الذكي للمنح العالمية.

Your job:
- Answer scholarship-related questions clearly.
- Recommend suitable scholarships based only on the provided context.
- If the user asks in Arabic, answer in Arabic.
- If the user asks in English, answer in English.
- Be helpful, concise, and student-friendly.
- If no scholarship matches, explain that and give general guidance.

Scholarship Context:
{rag_context}
"""

        response = client.chat.completions.create(
            model="gpt-5.5",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": request.message}
            ],
            temperature=0.4
        )

        return {
            "reply": response.choices[0].message.content,
            "matches": matches
        }

    except Exception as error:
        raise HTTPException(status_code=500, detail=str(error))


@app.get("/")
def home():
    return {"message": "Global Scholarships AI Chatbot API is running."}