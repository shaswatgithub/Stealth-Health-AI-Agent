import streamlit as st
import json
import os
from pydantic import BaseModel, Field
import google.generativeai as genai

# ==========================================
# GEMINI SETUP
# ==========================================

import os
import google.generativeai as genai
import streamlit as st

GEMINI_API_KEY = st.secrets["GEMINI_API_KEY"]

genai.configure(api_key=GEMINI_API_KEY)
if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY not found")

genai.configure(api_key=GEMINI_API_KEY)

model = genai.GenerativeModel("gemini-2.5-flash")
# ==========================================
# REFERENCE PROTOCOL
# ==========================================

REFERENCE_PROTOCOL = """
WELLNESS PROTOCOL RULES & DOS/DON'TS:

1. Hydration:
Drink exactly 3 Liters of water daily.
Avoid caffeine after 2:00 PM.

2. Sleep:
Maintain a strict 8-hour sleep window.
No screens 45 minutes before bed.

3. Activity:
Minimum 8,000 steps per day.
Light stretching for 10 minutes every morning.

4. Tracking:
Log meals within 30 minutes of consumption.

5. Habit Recovery:
Never skip two days in a row.
Consistency beats perfection.
"""

# ==========================================
# PATIENT PROFILE
# ==========================================

class PatientProfile(BaseModel):
    name: str = Field(default="Valued Patient")
    age: int = 25
    primary_goal: str = "General Wellness"
    sleep_hours: float = 7.0
    current_day: int = 1

# ==========================================
# STREAMLIT PAGE
# ==========================================

st.set_page_config(
    page_title="AI Health Coach",
    page_icon="🧘",
    layout="centered"
)

st.title("🧘 AI Health Coach MVP")
st.caption("Personalized wellness coaching agent")

# ==========================================
# SESSION MEMORY
# ==========================================

if "messages" not in st.session_state:
    st.session_state.messages = []

if "profile" not in st.session_state:
    st.session_state.profile = None

# ==========================================
# PARSE PROFILE FROM URL
# ==========================================

query_params = st.query_params

if "raw_data" in query_params and st.session_state.profile is None:

    raw_text = query_params["raw_data"]

    extraction_prompt = f"""
Extract patient information.

Return ONLY valid JSON.

Schema:

{{
    "name": "",
    "age": 0,
    "primary_goal": "",
    "sleep_hours": 0,
    "current_day": 1
}}

Text:

{raw_text}
"""

    try:

        response = model.generate_content(
            extraction_prompt
        )

        json_text = response.text.strip()

        json_text = json_text.replace("```json", "")
        json_text = json_text.replace("```", "")
        json_text = json_text.strip()

        profile_data = json.loads(json_text)

        st.session_state.profile = PatientProfile(
            **profile_data
        )

    except Exception as e:
        st.error(f"Profile extraction failed: {e}")

# ==========================================
# DEFAULT PROFILE
# ==========================================

if st.session_state.profile is None:

    st.session_state.profile = PatientProfile(
        name="Guest",
        age=25,
        primary_goal="General Fitness",
        sleep_hours=7,
        current_day=1
    )

profile = st.session_state.profile

# ==========================================
# SIDEBAR
# ==========================================

st.sidebar.title("Patient State")

st.sidebar.json(profile.model_dump())

st.sidebar.success(
    f"Protocol Day {profile.current_day}"
)

# ==========================================
# RESEARCH EXTRACTION RESULT
# ==========================================

st.subheader("📋 Research Extraction Results")

st.json(profile.model_dump())

# ==========================================
# DAY-SPECIFIC CONTEXT
# ==========================================

if profile.current_day == 1:

    day_context = f"""
Day 1 Introduction.

Welcome the patient warmly.

Review goal:
{profile.primary_goal}

Introduce hydration and sleep habits.
"""

elif profile.current_day >= 5:

    day_context = f"""
Day {profile.current_day} Follow-Up.

Ask about progress.

Focus on:
{profile.primary_goal}

Reference previous answers if available.
"""

else:

    day_context = f"""
Day {profile.current_day}

Continue accountability and habit tracking.
"""

# ==========================================
# SYSTEM PROMPT
# ==========================================

system_prompt = f"""
You are a warm, clear health coach.

Patient Name:
{profile.name}

Age:
{profile.age}

Goal:
{profile.primary_goal}

Timeline Context:
{day_context}

STRICT RULES:

1. Use ONLY the protocol below for protocol questions.

2. If answer is not found inside protocol,
say:

"I couldn't find that in the protocol document."

3. Be supportive but concise.

PROTOCOL:

{REFERENCE_PROTOCOL}
"""

# ==========================================
# CHAT HISTORY
# ==========================================

for msg in st.session_state.messages:

    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# ==========================================
# CHAT INPUT
# ==========================================

user_input = st.chat_input(
    "Ask your coach or log today's progress..."
)

if user_input:

    with st.chat_message("user"):
        st.markdown(user_input)

    st.session_state.messages.append(
        {
            "role": "user",
            "content": user_input
        }
    )

    conversation = system_prompt + "\n\n"

    recent_history = st.session_state.messages[-6:]

    for msg in recent_history:

        conversation += (
            f"{msg['role']}: "
            f"{msg['content']}\n"
        )

    try:

        response = model.generate_content(
            conversation,
            generation_config={
                "temperature": 0.2
            }
        )

        response_text = response.text

    except Exception as e:

        response_text = (
            f"Error generating response: {e}"
        )

    with st.chat_message("assistant"):
        st.markdown(response_text)

    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": response_text
        }
    )