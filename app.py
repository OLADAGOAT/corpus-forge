import os
from pathlib import Path

import streamlit as st
from pypdf import PdfReader


DATA_DIR = Path("data")
DATA_DIR.mkdir(exist_ok=True)

SUPPORTED_TYPES = ["txt", "md", "pdf", "py", "js"]


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


st.set_page_config(page_title="Corpus Forge", layout="wide")

st.title("Corpus Forge")
st.write("A simple AI-ready corpus management web application.")

st.sidebar.header("Document Upload")

uploaded_files = st.sidebar.file_uploader(
    "Upload documents",
    type=SUPPORTED_TYPES,
    accept_multiple_files=True
)

if uploaded_files:
    for uploaded_file in uploaded_files:
        save_uploaded_file(uploaded_file)

    st.sidebar.success("Files uploaded successfully.")

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
                st.success(f"{file_path.name} deleted.")
                st.rerun()

    selected_documents = st.multiselect(
        "Select active documents",
        documents,
        format_func=lambda file_path: file_path.name
    )

    if selected_documents:
        st.subheader("Selected Corpus Preview")

        combined_text = ""

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

st.header("Next Features")
st.write("- Add AI question answering")
st.write("- Add flashcard generation")
st.write("- Add quiz generation")
st.write("- Add token/request usage tracking")