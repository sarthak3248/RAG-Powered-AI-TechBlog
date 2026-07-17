# 🤖 RAG-Powered AI TechBlog

> An intelligent AI-powered blogging platform built with Django, Machine Learning, NLP, and Retrieval-Augmented Generation (RAG).

![Python](https://img.shields.io/badge/Python-3.14-blue)
![Django](https://img.shields.io/badge/Django-6.0-success)
![Transformers](https://img.shields.io/badge/HuggingFace-Transformers-yellow)
![PyTorch](https://img.shields.io/badge/PyTorch-DeepLearning-red)
![License](https://img.shields.io/badge/License-MIT-green)

---

# 📖 Overview

RAG-Powered AI TechBlog is a full-stack intelligent blogging platform that combines modern web development with Artificial Intelligence to deliver personalized content recommendations, semantic search, AI-generated summaries, toxicity moderation, and an intelligent chatbot powered by Retrieval-Augmented Generation (RAG).

Unlike traditional blogging websites, this platform understands user interests, recommends relevant articles using Machine Learning, summarizes lengthy articles using Transformer models, moderates comments using AI, and allows users to interact with blog content through an intelligent conversational assistant.

---

# 🚀 Key Features

## 🧠 AI Features

- 🤖 Retrieval-Augmented Generation (RAG) Chatbot *(In Progress)*
- 📚 Semantic Search using Sentence Transformers
- 📝 AI-powered Article Summarization
- 🛡️ Toxic Comment Detection using Jigsaw Toxicity Model
- ❤️ Personalized Content Recommendation Engine
- 🔥 Hybrid Recommendation System
- 📊 User Preference Modeling
- 🎯 Similar Article Recommendation

---

## 🌐 Blog Features

- User Registration & Authentication
- Rich Blog Posts
- Categories
- Like System
- Bookmark System
- Reading Analytics
- AI Comment Moderation
- Responsive Bootstrap UI
- About Page
- Contact Form
- User Dashboard

---

# 🏗️ System Architecture

```
                 User
                  │
                  ▼
        Django Web Application
                  │
      ┌───────────┴────────────┐
      │                        │
      ▼                        ▼
 Recommendation Engine     AI Services
                              │
      ┌───────────────────────┼────────────────────┐
      │                       │                    │
      ▼                       ▼                    ▼
 Summarizer           Toxicity Detection      RAG Chatbot
      │                       │                    │
      └───────────────► Sentence Transformers ◄───┘
                              │
                              ▼
                         SQLite Database
```

---

# 🧠 AI Modules

## Recommendation Engine

Uses user interactions such as

- Likes
- Bookmarks
- Reading History
- Categories

to recommend personalized articles.

---

## Semantic Search

Built using

- Sentence Transformers
- all-MiniLM-L6-v2

Each article is converted into dense vector embeddings for semantic similarity search.

---

## AI Summarizer

Uses

- Facebook BART Transformer

to generate concise summaries of lengthy blog articles.

---

## Toxicity Detection

Implements the

- Jigsaw Toxic Comment Classification Model

to automatically detect and moderate inappropriate user comments.

---

## RAG Chatbot (Work in Progress)

Pipeline

```
User Question
       │
       ▼
Embedding Model
       │
       ▼
Semantic Retriever
       │
       ▼
Relevant Blog Articles
       │
       ▼
Prompt Builder
       │
       ▼
Large Language Model
       │
       ▼
Final AI Response
```

The chatbot answers:

- Questions about blog articles
- General AI questions
- Context-aware queries using Retrieval-Augmented Generation

---

# 🛠️ Technology Stack

## Backend

- Python
- Django

## Frontend

- HTML5
- CSS3
- Bootstrap 5
- JavaScript

## Artificial Intelligence

- Hugging Face Transformers
- Sentence Transformers
- PyTorch
- Scikit-learn
- NumPy

## Database

- SQLite

## Version Control

- Git
- GitHub

---

# 📂 Project Structure

```
AI-TechBlog/
│
├── blog/
│   ├── ai/
│   ├── ml/
│   ├── services/
│   ├── templates/
│   ├── static/
│   └── models.py
│
├── dashboard/
├── media/
├── static/
├── templates/
├── manage.py
├── requirements.txt
└── README.md
```

---

# ⚙️ Installation

Clone the repository

```bash
git clone https://github.com/yourusername/RAG-Powered-AI-TechBlog.git
```

Navigate into the project

```bash
cd RAG-Powered-AI-TechBlog
```

Create a virtual environment

```bash
python -m venv venv
```

Activate it

Windows

```bash
venv\Scripts\activate
```

Linux/macOS

```bash
source venv/bin/activate
```

Install dependencies

```bash
pip install -r requirements.txt
```

Run migrations

```bash
python manage.py migrate
```

Start the server

```bash
python manage.py runserver
```

Open

```
http://127.0.0.1:8000
```

---

# 📸 Screenshots

Coming Soon

- Home Page
- AI Dashboard
- Recommendation Engine
- Summarizer
- Chatbot
- Comment Moderation

---

# 🎯 Future Enhancements

- ✅ Complete RAG Chatbot
- ✅ AI Agent with Tool Calling
- ✅ FAISS Vector Database
- ✅ PostgreSQL
- ✅ Docker Deployment
- ✅ AWS Deployment
- ✅ CI/CD using GitHub Actions
- ✅ REST API
- ✅ JWT Authentication
- ✅ Voice-enabled AI Assistant
- ✅ Multi-language Support

---

# 📚 Learning Outcomes

This project demonstrates practical implementation of

- Machine Learning
- Natural Language Processing
- Recommendation Systems
- Semantic Search
- Retrieval-Augmented Generation
- Django Full-Stack Development
- AI System Design
- Transformer Models
- Enterprise Software Engineering

---

# 👨‍💻 Author

**Sarthak Singhal**

Graduate Student | AI Engineer | Full Stack Developer

- LinkedIn: https://www.linkedin.com/in/sarthak-agrawal-097b591aa/
- GitHub: https://github.com/sarthak3248

---

# ⭐ If you found this project useful

Please consider giving it a ⭐ on GitHub!
