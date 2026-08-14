# 🌍 TravelSwarm: Autonomous Multi-Agent Travel Orchestrator

[![Python](https://img.shields.io/badge/Python-3.11-blue.svg?style=flat\&logo=python)](https://www.python.org/)
[![LangGraph](https://img.shields.io/badge/Orchestration-LangGraph-orange.svg)](https://github.com/langchain-ai/langgraph)
[![Groq](https://img.shields.io/badge/LLM-Groq%20Llama--3.3--70B-green.svg)](https://groq.com/)
[![FastAPI](https://img.shields.io/badge/Backend-FastAPI-009688.svg?logo=fastapi)](https://fastapi.tiangolo.com/)
[![PostgreSQL](https://img.shields.io/badge/Database-PostgreSQL-336791.svg?logo=postgresql)]
[![Docker](https://img.shields.io/badge/Deployment-Docker-2496ED.svg?logo=docker)](https://www.docker.com/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

> **TravelSmarter. Plan Faster. TravelBetter.**

TravelSwarm is an **autonomous multi-agent AI travel planning system** that coordinates specialized AI agents to research flights, discover accommodations, build itineraries, and generate a complete travel plan.

Instead of manually switching between flight websites, hotel platforms, search engines, and itinerary planners, TravelSwarm orchestrates the entire workflow through a **LangGraph state graph**.

---

## 📌 Overview

TravelSwarm is an end-to-end AI application built around a **multi-agent architecture**.

A user's travel request is processed through a sequence of specialized agents:

```text
User Request
     │
     ▼
┌─────────────────────┐
│   Flight Agent      │
│  AviationStack API  │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│    Hotel Agent      │
│    Tavily Search    │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│  Itinerary Agent    │
│  Groq Llama 3.3 70B │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│    Final Agent      │
│  Groq Llama 3.3 70B │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│ Structured Trip Plan│
│      + PDF          │
└─────────────────────┘
```

The application combines **LLM reasoning, external APIs, web search, persistent graph state, and a web interface** into a single travel orchestration platform.

---

# ✨ Key Features

### 🤖 Multi-Agent Orchestration

Built using **LangGraph**, TravelSwarm separates responsibilities across specialized agents instead of relying on a single LLM call.

* ✈️ Flight Agent
* 🏨 Hotel Agent
* 🗺️ Itinerary Agent
* 🧠 Final Response Agent

Each agent performs a specific task and passes structured state to the next stage.

---

### ⚡ High-Speed LLM Inference

TravelSwarm uses **Groq Cloud** with:

```text
llama-3.3-70b-versatile
```

The model is used for tasks such as:

* Natural-language travel request understanding
* Entity extraction
* Destination interpretation
* Structured data generation
* Itinerary planning
* Final response generation

---

### ✈️ Live Flight Discovery

The Flight Agent integrates with **AviationStack** to retrieve flight-related information such as:

* Flight schedules
* Airlines
* Departure information
* Arrival information
* Airports
* Terminal information
* Gate information when available

---

### 🏨 Real-Time Hotel & Accommodation Search

The Hotel Agent uses **Tavily Search** to discover relevant accommodation options based on the user's requirements.

The search can consider:

* Destination
* Budget
* Hotel ratings
* Location
* Available accommodation information
* Travel preferences

---

### 🧠 Persistent Agent Memory

TravelSwarm uses **PostgreSQL** with LangGraph's PostgreSQL checkpointing system.

This allows the application to persist:

* Graph state
* Conversation threads
* Agent execution state
* Previous workflow information

This makes the multi-agent system capable of maintaining state across sessions.

---

### 🌐 Full-Stack Web Application

The frontend is built using:

* HTML
* CSS
* JavaScript
* Jinja2 templates

The backend uses:

* FastAPI
* Pydantic
* Uvicorn

The application exposes both a user-friendly web interface and REST API endpoints.

---

### 📄 PDF Travel Plans

After completing the agent workflow, TravelSwarm generates a structured travel plan that can be exported as a downloadable PDF.

The generated plan can contain:

* Flight information
* Hotel recommendations
* Daily itinerary
* Travel details
* Destination information

---

### 🐳 Dockerized Deployment

TravelSwarm is fully containerized using Docker and can be deployed to platforms such as:

* Render
* AWS
* Railway
* Any Docker-compatible cloud VM

---

# 🏗️ System Architecture

```text
                              ┌──────────────────────────┐
                              │       User Prompt        │
                              └────────────┬─────────────┘
                                           │
                                           ▼
                              ┌──────────────────────────┐
                              │    FastAPI Application   │
                              │       /api/travel        │
                              └────────────┬─────────────┘
                                           │
                                           ▼
══════════════════════════════ LANGGRAPH STATE GRAPH ══════════════════════════════

       ┌───────────────────┐
       │   Flight Agent    │
       │                   │
       │  AviationStack    │
       └─────────┬─────────┘
                 │
                 ▼
       ┌───────────────────┐
       │    Hotel Agent    │
       │                   │
       │   Tavily Search   │
       └─────────┬─────────┘
                 │
                 ▼
       ┌───────────────────┐
       │  Itinerary Agent  │
       │                   │
       │ Groq Llama 3.3    │
       └─────────┬─────────┘
                 │
                 ▼
       ┌───────────────────┐
       │    Final Agent    │
       │                   │
       │ Groq Llama 3.3    │
       └─────────┬─────────┘
                 │
                 ▼
══════════════════════════════════════════════════════════════════════════════════

                              ┌──────────────────────────┐
                              │       PostgreSQL         │
                              │   State Checkpointing    │
                              │   Thread Memory/History  │
                              └────────────┬─────────────┘
                                           │
                                           ▼
                              ┌──────────────────────────┐
                              │   Structured Trip Plan   │
                              │          + PDF           │
                              └──────────────────────────┘
```

---

# 🛠️ Tech Stack

| Domain                  | Technology                        |
| ----------------------- | --------------------------------- |
| **Language**            | Python 3.11                       |
| **Agent Orchestration** | LangGraph                         |
| **LLM Framework**       | LangChain Core                    |
| **LLM Provider**        | Groq                              |
| **LLM Model**           | Llama 3.3 70B Versatile           |
| **Flight API**          | AviationStack                     |
| **Web Search**          | Tavily Search API                 |
| **Database**            | PostgreSQL                        |
| **Graph Checkpointing** | LangGraph PostgreSQL Checkpointer |
| **Database Pooling**    | psycopg-pool                      |
| **Backend**             | FastAPI                           |
| **Server**              | Uvicorn                           |
| **Frontend**            | HTML, CSS, JavaScript, Jinja2     |
| **Validation**          | Pydantic                          |
| **Observability**       | LangSmith                         |
| **Containerization**    | Docker                            |
| **Deployment**          | Render                            |

---


# 🚀 Getting Started

## 1. Prerequisites

Make sure you have the following installed:

* Python `3.11+`
* Git
* PostgreSQL
* Docker *(optional)*

You will also need API keys for:

* Groq
* Tavily
* AviationStack
* LangSmith *(optional)*

---

## 2. Clone the Repository

```bash
git clone https://github.com/your-username/TravelSwarm.git

cd TravelSwarm
```

---

## 3. Create a Virtual Environment

### Windows

```bash
python -m venv travel_env

travel_env\Scripts\activate
```

### macOS / Linux

```bash
python3 -m venv travel_env

source travel_env/bin/activate
```

---

## 4. Install Dependencies

```bash
pip install -r requirements.txt
```

---

# 🔐 Environment Variables

Create a `.env` file in the project root.

```env
# Database
DATABASE_URL=postgresql://postgres:your_password@localhost:5432/agent_memory

# LLM
GROQ_API_KEY=gsk_your_groq_api_key

# Search
TAVILY_API_KEY=tvly-your_tavily_api_key

# Flight API
AVIATIONSTACK_API_KEY=your_aviationstack_api_key

# Default Airport
DEFAULT_ORIGIN_IATA=LHE

# LangSmith - Optional
LANGCHAIN_TRACING_V2=true
LANGCHAIN_ENDPOINT=https://api.smith.langchain.com
LANGCHAIN_API_KEY=your_langsmith_api_key
LANGCHAIN_PROJECT=TravelSwarm
```

---

# ▶️ Running Locally

Start the FastAPI development server:

```bash
uvicorn app:app --host 127.0.0.1 --port 8000 --reload
```

Open the application:

```text
http://127.0.0.1:8000
```

Interactive API documentation:

```text
http://127.0.0.1:8000/docs
```

---
---

