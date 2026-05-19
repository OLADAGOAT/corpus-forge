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

st.header("Next Features")
st.write("- Add code review report")
st.write("- Add architecture/control-flow report")