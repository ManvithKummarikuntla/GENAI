import streamlit as st
from dotenv import load_dotenv
load_dotenv()

from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate

st.set_page_config(page_title="Movie Info Extractor", page_icon="🎬", layout="centered")

st.title("🎬 Movie Info Extractor")
st.caption("Paste a movie paragraph and get structured details plus a quick summary.")


@st.cache_resource
def get_model():
    return ChatGroq(model="openai/gpt-oss-20b")


prompt = ChatPromptTemplate.from_messages([
    ("system",
     """You are an information-extraction assistant for a movie database.
Read the paragraph the user gives and extract useful details about the movie.

Rules:
- Use ONLY information present in the paragraph. Do not add outside knowledge.
- If a detail is not mentioned, write "Not mentioned". Do not guess.
- Ignore any links or markdown; use the plain movie title.
- Keep proper nouns spelled exactly as written.

Return the answer in this format:

Movie Name:
Genre(s):
Tone / Mood:
Language / Dialect:
Setting (place & time):
Cast (actor - character):
Main Characters:
Director / Writer / Producer / Music:
Release Year:
Themes:
Central Conflict:
Key Plot Points:
Quick Summary (max 2 sentences):"""),
    ("human", "Paragraph:\n{paragraph}"),
])

para = st.text_area("Movie paragraph", height=220, placeholder="Paste your paragraph here...")

if st.button("Extract Information", type="primary"):
    if not para.strip():
        st.warning("Please enter a paragraph first.")
    else:
        with st.spinner("Extracting..."):
            try:
                final_prompt = prompt.invoke({"paragraph": para})
                response = get_model().invoke(final_prompt)
                st.subheader("Result")
                st.markdown(response.content)
            except Exception as e:
                st.error(f"Something went wrong: {e}")