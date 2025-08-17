"""
AI-Powered Interview Bot
------------------------
Modular, clean, and extendable architecture.
Supports: Audio recording, AI question generation, evaluation, and CSV logging.

Author: Abdullah Siddiqui (Refactored with modular best practices)
"""

import os
import csv
import streamlit as st
from dotenv import load_dotenv
from audio_recorder_streamlit import audio_recorder
from groq import Groq

# ====== CONFIGURATION & ENVIRONMENT ====== #
load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
if not GROQ_API_KEY:
    st.error("❌ GROQ_API_KEY not found in environment. Please configure it before running.")
    st.stop()

groq_client = Groq(api_key=GROQ_API_KEY)

# ====== HELPERS ====== #
def save_audio(audio_bytes, filename):
    """Save recorded audio to file."""
    os.makedirs("audios", exist_ok=True)
    path = os.path.join("audios", filename)
    with open(path, "wb") as f:
        f.write(audio_bytes)
    return path

def transcribe_audio_file(audio_path, model="whisper-large-v3"):
    """Transcribe audio file using Groq Whisper API."""
    with open(audio_path, "rb") as f:
        transcription = groq_client.audio.transcriptions.create(file=f, model=model)
    return transcription.text.strip()

# ====== AI CHAINS ====== #
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from langchain_groq import ChatGroq

def get_llm(model="Llama3-8b-8192"):
    """Initialize Groq LLM."""
    return ChatGroq(groq_api_key=GROQ_API_KEY, model_name=model)

def greeting_chain(candidate_name):
    prompt = PromptTemplate(
        input_variables=["candidate_name"],
        template="""You are a friendly AI interviewer named 'Santosh'.
Warmly greet {candidate_name}, introduce yourself, and explain the interview process.
Keep it professional and approachable in 2–3 sentences."""
    )
    return LLMChain(llm=get_llm(), prompt=prompt).run(candidate_name=candidate_name)

def question_chain(role, description):
    prompt = PromptTemplate(
        input_variables=["role", "description"],
        template="""As an expert recruiter, generate 5 interview questions for a {role} position.
Job Description: {description}
Provide only the questions, numbered, no extra commentary."""
    )
    return LLMChain(llm=get_llm(), prompt=prompt).run(role=role, description=description)

def evaluation_chain(role, qa_text, rubric=None):
    rubric = rubric or """
1. Technical accuracy (0–5)
2. Communication clarity (0–3)
3. Problem-solving ability (0–2)
"""
    prompt = PromptTemplate(
        input_variables=["role", "qa_text", "rubric"],
        template="""You are an expert recruiter evaluating a {role} interview.

Candidate's responses:
{qa_text}

Scoring Rubric:
{rubric}

Return format:
Final Score: #/10
Overall Feedback: ...
Recommendation: Consider/Reject"""
    )
    return LLMChain(llm=get_llm(), prompt=prompt).run(role=role, qa_text=qa_text, rubric=rubric)

# ====== DATA STORAGE ====== #
def save_results_csv(candidate_name, role, responses, eval_result, file_path="interview_results.csv"):
    file_exists = os.path.isfile(file_path)
    with open(file_path, mode="a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        if not file_exists:
            writer.writerow(["Candidate Name", "Role", "Question", "Audio File", "Transcribed Answer", "Evaluation Summary"])
        for q, data in responses.items():
            writer.writerow([candidate_name, role, q, data["audio"], data["text"], eval_result])

# ====== MOCK DATA MODE (NO API) ====== #
USE_MOCK = False
def mock_questions():
    return [f"Mock Question {i}" for i in range(1, 6)]

def mock_eval():
    return "Final Score: 7/10\nOverall Feedback: Good performance.\nRecommendation: Consider"

# ====== UI LOGIC ====== #
def main():
    st.title("🤖 AI-Powered Interview Bot")

    # Session state init
    for key, value in {
        "questions": [],
        "current_question": 0,
        "responses": {},
        "interview_complete": False,
        "greeting_done": False,
        "greeting_text": "",
        "candidate_name": "",
        "role": "",
        "description": ""
    }.items():
        if key not in st.session_state:
            st.session_state[key] = value

    # Candidate name
    if not st.session_state.candidate_name:
        name = st.text_input("Enter your name")
        if st.button("Submit Name") and name.strip():
            st.session_state.candidate_name = name.strip()
            st.rerun()
        return

    # Greeting
    if not st.session_state.greeting_done:
        st.session_state.greeting_text = greeting_chain(st.session_state.candidate_name) if not USE_MOCK else "Hello mock candidate!"
        st.session_state.greeting_done = True
        st.rerun()

    st.info(st.session_state.greeting_text)

    # Role details
    with st.expander("Enter Role Details", expanded=True):
        st.session_state.role = st.text_input("Job Title", st.session_state.role)
        st.session_state.description = st.text_area("Job Description", st.session_state.description, height=100)
        if st.button("Start Interview"):
            if st.session_state.role.strip() and st.session_state.description.strip():
                st.session_state.questions = (
                    mock_questions() if USE_MOCK else
                    [q.strip() for q in question_chain(st.session_state.role, st.session_state.description).splitlines() if q.strip()]
                )
                st.session_state.current_question = 0
                st.session_state.responses.clear()
                st.session_state.interview_complete = False
                st.rerun()
            else:
                st.warning("Please enter both job title and description.")

    # Interview Q&A
    if st.session_state.questions and not st.session_state.interview_complete:
        idx = st.session_state.current_question
        q_text = st.session_state.questions[idx]
        st.subheader(f"Question {idx+1} / {len(st.session_state.questions)}")
        st.markdown(f"**{q_text}**")

        audio_bytes = audio_recorder(text="Click to Record / Stop", icon_size="2x")
        if audio_bytes:
            safe_name = st.session_state.candidate_name.replace(" ", "_")
            filename = f"{safe_name}_Q{idx+1}.wav"
            audio_path = save_audio(audio_bytes, filename)
            transcription = "Mock transcription" if USE_MOCK else transcribe_audio_file(audio_path)
            st.session_state.responses[q_text] = {"audio": audio_path, "text": transcription}
            st.success("✅ Answer recorded and transcribed.")
            st.info(transcription)

        if q_text in st.session_state.responses:
            col1, col2 = st.columns(2)
            if idx > 0 and col1.button("Previous Question"):
                st.session_state.current_question -= 1
                st.rerun()
            if idx < len(st.session_state.questions) - 1 and col2.button("Next Question"):
                st.session_state.current_question += 1
                st.rerun()
            elif idx == len(st.session_state.questions) - 1 and col2.button("Finish Interview"):
                st.session_state.interview_complete = True
                st.rerun()

    # Evaluation
    if st.session_state.interview_complete:
        qa_pairs = [f"Q{i+1}: {q}\nA: {data['text']}" for i, (q, data) in enumerate(st.session_state.responses.items())]
        combined_text = "\n\n".join(qa_pairs)
        eval_result = mock_eval() if USE_MOCK else evaluation_chain(st.session_state.role, combined_text)
        st.subheader("📊 Final Interview Evaluation")
        st.text(eval_result)
        save_results_csv(st.session_state.candidate_name, st.session_state.role, st.session_state.responses, eval_result)
        st.balloons()

if __name__ == "__main__":
    main()
