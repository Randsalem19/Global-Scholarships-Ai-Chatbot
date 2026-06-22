# 🎓 ScholarAI: Global Scholarships AI Advisor
**AI-Powered Chatbot designed for the "Foras Khadra" Platform**

## 📌 Project Overview
ScholarAI is an intelligent, bilingual (Arabic/English) conversational assistant built to help students discover and apply for fully-funded global scholarships. This project was developed as a technical task for the **Foras Khadra** AI Team, demonstrating the practical integration of Large Language Models (LLMs) into web applications using a Retrieval-Augmented Generation (RAG) approach.

## 🚀 Key Features
* **Bilingual Support:** Automatically detects whether the user is asking in Arabic or English and responds in the same language with professional formatting.
* **Smart Retrieval (RAG):** Searches a dynamic JSON knowledge base of 2026 global scholarships (e.g., Chevening, Fulbright, DAAD) based on user queries (majors, countries, degrees).
* **Automated Web Scraper:** Includes a Python-based web scraper (`scraper.py`) that extracts new scholarship data from external sources and updates the internal database, ensuring the data remains fresh without data duplication.
* **Modern SaaS UI/UX:** A highly responsive, corporate-style dashboard customized with "Foras Khadra" brand colors, featuring quick-action prompt buttons for seamless user interaction.
* **Error Handling & Real-time Feedback:** Features a typing indicator, clean Markdown rendering, and robust error handling to guide users if API limits are reached.

## 🛠️ Technology Stack
* **Backend:** Python, FastAPI, Uvicorn
* **AI Integration:** Groq API / OpenAI API (LLaMA3 / GPT models)
* **Frontend:** HTML5, Vanilla JavaScript (ES6+), Custom CSS3
* **Data Processing:** BeautifulSoup4 (for web scraping), RegEx (for keyword extraction)

## 📁 Project Structure
```text
scholarships-ai-chatbot/
├── backend/
│   ├── main.py            # FastAPI server & RAG pipeline
│   ├── scraper.py         # Automated web scraper for scholarships
│   ├── data.json          # Dynamic knowledge base
│   ├── .env               # Environment variables (API Keys)
│   └── requirements.txt   # Python dependencies
└── frontend/
    ├── index.html         # SaaS-style UI
    ├── style.css          # Foras Khadra green-themed styling
    └── app.js             # Client-side logic & API communication