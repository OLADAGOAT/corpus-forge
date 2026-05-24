from pathlib import Path
from datetime import datetime

import streamlit as st
from pypdf import PdfReader
from dotenv import load_dotenv
import google.generativeai as genai
import os


load_dotenv(override=True)

DATA_DIR = Path("data")
DATA_DIR.mkdir(exist_ok=True)

ARTIFACTS_DIR = Path("artifacts")
ARTIFACTS_DIR.mkdir(exist_ok=True)

SUPPORTED_TYPES = ["txt", "md", "pdf", "py", "js"]

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

if GOOGLE_API_KEY:
    genai.configure(api_key=GOOGLE_API_KEY)


def log_journal(action):
    """Append an action to JOURNAL.md with a timestamp."""
    journal_file = Path("JOURNAL.md")
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    entry = f"\n- **{timestamp}**: {action}"

    if journal_file.exists():
        current_content = journal_file.read_text(encoding="utf-8")
        journal_file.write_text(current_content + entry, encoding="utf-8")
    else:
        header = "# Corpus Forge Journal\n\n### Runtime Actions"
        journal_file.write_text(header + entry, encoding="utf-8")


def save_uploaded_file(uploaded_file):
    file_path = DATA_DIR / uploaded_file.name

    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())

    return file_path


def delete_document(file_path):
    if file_path.exists():
        file_path.unlink()


def read_txt_or_code(file_path):
    try:
        return file_path.read_text(encoding="utf-8")
    except Exception:
        return file_path.read_text(encoding="latin-1")


def read_pdf(file_path):
    text = ""

    reader = PdfReader(str(file_path))

    for page in reader.pages:
        page_text = page.extract_text()
        if page_text:
            text += page_text + "\n"

    return text


def read_document(file_path):
    suffix = file_path.suffix.lower()

    if suffix in [".txt", ".md", ".py", ".js"]:
        return read_txt_or_code(file_path)

    if suffix == ".pdf":
        return read_pdf(file_path)

    return ""


def list_documents():
    files = []

    for file_path in DATA_DIR.iterdir():
        if file_path.is_file():
            files.append(file_path)

    return files


def update_usage(response):
    st.session_state.request_count += 1

    try:
        st.session_state.token_usage += response.usage_metadata.total_token_count
    except Exception:
        pass


def ask_ai(question, corpus_text):
    if not GOOGLE_API_KEY:
        return "Missing GOOGLE_API_KEY. Add it inside your .env file."

    model = genai.GenerativeModel("gemini-3.1-flash-lite-preview")

    prompt = f"""
You are an AI assistant for a document corpus.

Answer the user's question using ONLY the corpus below.
If the answer is not in the corpus, say: "I could not find this information in the selected documents."

Corpus:
{corpus_text[:12000]}

Question:
{question}
"""

    response = model.generate_content(prompt)
    update_usage(response)

    return response.text


def generate_flashcards(corpus_text):
    if not GOOGLE_API_KEY:
        return "Missing GOOGLE_API_KEY. Add it inside your .env file."

    model = genai.GenerativeModel("gemini-3.1-flash-lite-preview")

    prompt = f"""
You are helping a student revise from selected documents.

Create 5 useful flashcards using ONLY the corpus below.

Format exactly like this:

1. Q: question
   A: answer

2. Q: question
   A: answer

3. Q: question
   A: answer

4. Q: question
   A: answer

5. Q: question
   A: answer

Corpus:
{corpus_text[:12000]}
"""

    response = model.generate_content(prompt)
    update_usage(response)

    return response.text


def generate_quiz(corpus_text):
    if not GOOGLE_API_KEY:
        return "Missing GOOGLE_API_KEY. Add it inside your .env file."

    model = genai.GenerativeModel("gemini-3.1-flash-lite-preview")

    prompt = f"""
You are helping a student revise from selected documents.

Create a 5-question quiz using ONLY the corpus below.

Each question must have:
- 4 answer choices: A, B, C, D
- the correct answer
- a short explanation

Format exactly like this:

1. Question: question here
   A. option
   B. option
   C. option
   D. option
   Correct answer: A/B/C/D
   Explanation: short explanation

2. Question: question here
   A. option
   B. option
   C. option
   D. option
   Correct answer: A/B/C/D
   Explanation: short explanation

Corpus:
{corpus_text[:12000]}
"""

    response = model.generate_content(prompt)
    update_usage(response)

    return response.text


def generate_code_review(corpus_text):
    if not GOOGLE_API_KEY:
        return "Missing GOOGLE_API_KEY. Add it inside your .env file."

    model = genai.GenerativeModel("gemini-3.1-flash-lite-preview")

    prompt = f"""
You are reviewing source code from a selected corpus.

Use ONLY the code/text below.

Create a simple code review report with these sections:

# Code Review Report 

## 1. Summary
Briefly explain what the code seems to do.

## 2. Strengths
List what is good or clear.

## 3. Problems or Risks
List bugs, weak parts, missing checks, or confusing code.

## 4. Suggested Improvements
Give practical improvements.

## 5. Beginner-Friendly Explanation
Explain the code in simple student-friendly language.

Corpus:
{corpus_text[:12000]}
"""

    response = model.generate_content(prompt)
    update_usage(response)

    return response.text


def generate_architecture_report(corpus_text):
    if not GOOGLE_API_KEY:
        return "Missing GOOGLE_API_KEY. Add it inside your .env file."

    model = genai.GenerativeModel("gemini-3.1-flash-lite-preview")

    prompt = f"""
You are analyzing a selected software/document corpus.

Use ONLY the corpus below.

Create an Architecture and Control-Flow Report with these sections:

# Architecture and Control-Flow Report

## 1. System Overview
Explain what the system or code appears to do.

## 2. Main Components
List the main files, functions, modules, or sections.

## 3. Data Flow
Explain how data moves through the system.

## 4. Control Flow
Explain the order of execution or user workflow.

## 5. Important Dependencies
Mention important libraries, APIs, or external tools used.

## 6. Weaknesses or Missing Parts
List missing features, risks, or unclear design parts.

## 7. Beginner-Friendly Explanation
Explain the architecture simply for a student presentation.

Corpus:
{corpus_text[:12000]}
"""

    response = model.generate_content(prompt)
    update_usage(response)

    return response.text


st.set_page_config(page_title="Corpus Forge", layout="wide")

st.title("Corpus Forge")
st.write("A simple AI-ready corpus management web application.")

if "request_count" not in st.session_state:
    st.session_state.request_count = 0

if "token_usage" not in st.session_state:
    st.session_state.token_usage = 0

st.sidebar.header("Document Upload")

uploaded_files = st.sidebar.file_uploader(
    "Upload documents",
    type=SUPPORTED_TYPES,
    accept_multiple_files=True
)

if uploaded_files:
    for uploaded_file in uploaded_files:
        save_uploaded_file(uploaded_file)
        log_journal(f"Document uploaded: {uploaded_file.name}")

    st.sidebar.success("Files uploaded successfully.")

st.sidebar.header("AI Usage")
st.sidebar.write(f"Requests: {st.session_state.request_count}")
st.sidebar.write(f"Estimated tokens: {st.session_state.token_usage}")

st.header("Available Documents")

documents = list_documents()

if not documents:
    st.info("No documents uploaded yet.")
else:
    st.subheader("Manage Documents")

    for file_path in documents:
        col1, col2 = st.columns([4, 1])

        with col1:
            st.write(file_path.name)

        with col2:
            if st.button("Delete", key=f"delete_{file_path.name}"):
                delete_document(file_path)
                log_journal(f"Document deleted: {file_path.name}")
                st.success(f"{file_path.name} deleted.")
                st.rerun()

    selected_documents = st.multiselect(
        "Select active documents",
        documents,
        format_func=lambda file_path: file_path.name
    )

    combined_text = ""

    if selected_documents:
        st.subheader("Selected Corpus Preview")

        for file_path in selected_documents:
            st.write(f"### {file_path.name}")

            content = read_document(file_path)
            combined_text += content + "\n\n"

            preview = content[:1500]

            if preview.strip():
                st.text_area(
                    f"Preview of {file_path.name}",
                    preview,
                    height=200
                )
            else:
                st.warning("Could not read this file.")

        st.subheader("Corpus Stats")

        st.write(f"Active documents: {len(selected_documents)}")
        st.write(f"Total characters: {len(combined_text)}")
        st.write(f"Estimated words: {len(combined_text.split())}")

        st.header("Ask Questions About Selected Documents")

        question = st.text_input("Ask a question")

        if st.button("Ask AI"):
            if not question.strip():
                st.warning("Please enter a question.")
            else:
                with st.spinner("Thinking..."):
                    answer = ask_ai(question, combined_text)
                    log_journal(f"User asked AI: {question[:50]}")

                st.subheader("AI Answer")
                st.write(answer)

        st.header("Generate Flashcards")

        if st.button("Generate Flashcards"):
            with st.spinner("Creating flashcards..."):
                flashcards = generate_flashcards(combined_text)
                log_journal("Flashcards generated")

            st.subheader("Flashcards")
            st.write(flashcards)

            flashcard_file = ARTIFACTS_DIR / "flashcards.md"
            flashcard_file.write_text(flashcards, encoding="utf-8")

            st.success("Flashcards saved to artifacts/flashcards.md")

        st.header("Generate Quiz")

        if st.button("Generate Quiz"):
            with st.spinner("Creating quiz..."):
                quiz = generate_quiz(combined_text)
                log_journal("Quiz generated")

            st.subheader("Quiz")
            st.write(quiz)

            quiz_file = ARTIFACTS_DIR / "quiz.md"
            quiz_file.write_text(quiz, encoding="utf-8")

            st.success("Quiz saved to artifacts/quiz.md")

        st.header("Generate Code Review Report")

        if st.button("Generate Code Review Report"):
            with st.spinner("Reviewing code..."):
                code_review = generate_code_review(combined_text)
                log_journal("Code review report generated")

            st.subheader("Code Review Report")
            st.write(code_review)

            code_review_file = ARTIFACTS_DIR / "code_review.md"
            code_review_file.write_text(code_review, encoding="utf-8")

            st.success("Code review saved to artifacts/code_review.md")

        st.header("Generate Architecture / Control-Flow Report")

        if st.button("Generate Architecture Report"):
            with st.spinner("Creating architecture report..."):
                architecture_report = generate_architecture_report(combined_text)
                log_journal("Architecture/control-flow report generated")

            st.subheader("Architecture / Control-Flow Report")
            st.write(architecture_report)

            architecture_file = ARTIFACTS_DIR / "architecture_report.md"
            architecture_file.write_text(architecture_report, encoding="utf-8")

            st.success("Architecture report saved to artifacts/architecture_report.md")

st.header("Project Status")
st.write(
    "Core features implemented: upload, delete, document selection, AI Q&A, "
    "flashcards, quiz, code review, architecture/control-flow report, "
    "usage tracking, and journal logging."
)