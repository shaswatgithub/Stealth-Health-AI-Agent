# 🕵️ Stealth Health AI Agent

An AI-powered wellness coaching assistant that personalizes health guidance through structured patient onboarding, adaptive daily check-ins, session memory, and protocol-grounded responses.

## 🚀 Overview

Stealth Health AI Agent is designed to simulate a personalized health coach. The system extracts structured patient information from unstructured onboarding text, adapts its behavior based on the user's protocol day, remembers previous interactions within a session, and answers wellness-related questions using a predefined protocol.

## ✨ Features

### 1. Patient Onboarding Extraction

The agent converts unstructured onboarding text into a structured patient profile.

**Input Example**

```text
I am Shaswat, 22 years old.
My goal is improving sleep.
I currently sleep 5 hours.
Put me on Day 5.
```

**Extracted Profile**

```json
{
  "name": "Shaswat",
  "age": 22,
  "primary_goal": "improving sleep",
  "sleep_hours": 5,
  "current_day": 5
}
```

---

### 2. Adaptive Daily Check-ins

The agent dynamically changes its coaching style based on protocol progression.

**Day 1**

* Welcome and introduction
* Goal review
* Habit baseline assessment

**Day 2–4**

* Progress tracking
* Habit consistency checks
* Accountability questions

**Day 5+**

* Goal-focused follow-up
* Barrier identification
* Long-term consistency coaching

---

### 3. Session Memory

The agent remembers previous user messages during the active session and can reference earlier check-ins for a more personalized experience.

---

### 4. Protocol-Grounded Responses

The assistant is restricted to answering questions using the provided wellness protocol.

If information is not present in the protocol, the agent responds:

```text
I couldn't find that in the protocol document.
```

This minimizes hallucinations and ensures reliable responses.

---

## 🛠 Tech Stack

* Python
* Streamlit
* Google Gemini 2.5 Flash
* Pydantic
* Streamlit Session State

---

## 📂 Project Structure

```text
stealth-health-ai-agent/
│
├── app.py
├── requirements.txt
├── README.md
└── .streamlit/
```

---

## ⚙️ Installation

Clone the repository:

```bash
git clone https://github.com/shaswatgithub/Stealth-Health-AI-Agent.git
cd Stealth-Health-AI-Agent
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Create Streamlit secrets:

```toml
GEMINI_API_KEY = "YOUR_GEMINI_API_KEY"
```

Run the application:

```bash
streamlit run app.py
```

---

## 🔗 URL-Based Personalization

The application supports onboarding through URL query parameters.

Example:

```text
https://your-app.streamlit.app/?raw_data=I am Shaswat, 22 years old. My goal is improving sleep. I currently sleep 5 hours. Put me on Day 5.
```

The agent automatically extracts and displays the patient profile.

---

## 🧪 Example Questions

* How much water should I drink?
* What are the sleep rules?
* I drank only 1 liter of water today.
* What did I tell you earlier?

---

## 📹 Deliverables

* Live Streamlit Application
* Public GitHub Repository
* Demo Video Walkthrough
* Technical Report

---

## 🔮 Future Improvements

* PDF-based protocol ingestion (RAG)
* Long-term user memory
* Habit analytics dashboard
* Progress visualization
* Multi-user support
* Vector database integration

---

## 👨‍💻 Author

**Shaswat**

Built as an AI Agent MVP demonstrating structured extraction, adaptive coaching, memory, and protocol-grounded reasoning.
