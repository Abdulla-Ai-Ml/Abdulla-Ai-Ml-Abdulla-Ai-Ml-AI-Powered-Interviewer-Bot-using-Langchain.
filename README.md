# 🤖 AI-Powered Audio Interview Bot

An **AI-driven interview assistant** that conducts interviews through **audio recording**, generates questions based on a given role & job description, transcribes answers, evaluates candidate performance, and stores results in a CSV file.

This project uses:
- **[LangChain](https://www.langchain.com/)** for LLM prompt chaining
- **[Groq API](https://groq.com/)** for fast LLM responses (LLaMA models) and Whisper transcription
- **[Streamlit](https://streamlit.io/)** for an interactive web UI
- **[audio-recorder-streamlit](https://pypi.org/project/audio-recorder-streamlit/)** for in-browser audio recording

---

## ✨ Features
- 🎤 **Audio Recording:** Candidate answers questions verbally.
- 📝 **Speech-to-Text:** Transcribes audio answers using Groq's Whisper model.
- 🤖 **AI-Generated Questions:** LLaMA-based question generation tailored to the job description.
- 📊 **Automated Evaluation:** AI evaluates answers using a scoring rubric.
- 💾 **CSV Data Logging:** Stores candidate info, questions, audio paths, transcriptions, and evaluation results.
- 🧪 **Mock Mode:** Test without API calls.
- 🎈 **Interactive UI:** Built in Streamlit with easy navigation between questions.
- 

---

---

## 🛠️ Tools & Libraries

| Tool / Library | Purpose |
|----------------|---------|
| **[Streamlit](https://streamlit.io/)** | UI framework for web app |
| **[LangChain](https://python.langchain.com/)** | Prompt management & LLM chaining |
| **[Groq Python SDK](https://pypi.org/project/groq/)** | Connect to Groq LLaMA models and Whisper transcription |
| **[langchain-groq](https://pypi.org/project/langchain-groq/)** | LangChain integration for Groq models |
| **[dotenv](https://pypi.org/project/python-dotenv/)** | Load `.env` variables securely |
| **[audio-recorder-streamlit](https://pypi.org/project/audio-recorder-streamlit/)** | In-browser audio recording |
| **CSV module (Python)** | Saving structured results |

---

## 📋 Requirements

### Python Version
- **Python 3.9+** is recommended.

### Install Dependencies

pip install streamlit langchain langchain-groq groq python-dotenv audio-recorder-streamlit





<img src="https://github.com/user-attachments/assets/17115b08-6208-4d5e-a579-da54b6ab4a7c" alt="Untitled1">
<img src="https://github.com/user-attachments/assets/099028cc-2790-4b78-9654-752b752c7197" alt="Untitled2">
<img src="https://github.com/user-attachments/assets/c78331a3-f5bc-47c8-abc1-962abc46690c" alt="Untitled4">
<img src="https://github.com/user-attachments/assets/f0c83f5b-5b01-404a-9ad2-53a0121fd0df" alt="Untitled5">
<img src="https://github.com/user-attachments/assets/d066ae80-5f07-444e-815a-4db6306fec14" alt="Untitled6">




