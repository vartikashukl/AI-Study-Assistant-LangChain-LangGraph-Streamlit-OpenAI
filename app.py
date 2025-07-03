import streamlit as st
from dotenv import load_dotenv
from utils.pdf_loader import load_and_split
from langgraph_pipeline import create_graph_pipeline

load_dotenv()

st.title("📘 AI Study Assistant (Gemini + LangGraph)")

uploaded_file = st.file_uploader("Upload PDF", type="pdf")
query = st.text_input("Ask a question")
topic = st.text_input("Topic for Quiz")

if uploaded_file:
    with open("data/input.pdf", "wb") as f:
        f.write(uploaded_file.read())

    docs = load_and_split("data/input.pdf")
    full_text = " ".join([doc.page_content for doc in docs])

    if st.button("Run Assistant"):
        pipeline = create_graph_pipeline()
        result = pipeline.invoke({
            "content": full_text,
            "question": query,
            "topic": topic
        })

        st.subheader("Summary")
        st.write(result.get("summary"))

        st.subheader("Answer")
        st.write(result.get("answer"))

        st.subheader("Quiz")
        st.text(result.get("quiz"))