import html

import streamlit as st
from dotenv import load_dotenv
load_dotenv()

from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from pydantic import BaseModel
from typing import List, Optional
from langchain_core.output_parsers import PydanticOutputParser


# Schema
class Movie(BaseModel):
    title: str
    release_year: Optional[int]
    genere: List[str]
    director: Optional[str]
    cast: List[str]
    rating: Optional[float]
    summary: str


parser = PydanticOutputParser(pydantic_object=Movie)

prompt = ChatPromptTemplate.from_messages([
    ("system", """
        Extract Movie information from the paragraph
        {format_instructions}
    """),
    ("human", "{paragraph}")
])


@st.cache_resource
def get_model():
    return ChatGroq(model="openai/gpt-oss-20b")


# ---------------------------------------------------------------- UI setup
st.set_page_config(page_title="Movie Info Extractor", page_icon="🎬", layout="centered")

st.markdown(
    """
    <style>
    .block-container { max-width: 820px; padding-top: 2.5rem; padding-bottom: 4rem; }
    #MainMenu, footer { visibility: hidden; }

    .hero {
        text-align: center;
        padding: 2.2rem 1.5rem;
        border-radius: 22px;
        background: linear-gradient(135deg, #6d28d9 0%, #db2777 55%, #f59e0b 100%);
        color: #fff;
        box-shadow: 0 18px 40px -18px rgba(219, 39, 119, 0.55);
        margin-bottom: 1.8rem;
    }
    .hero h1 { margin: 0; font-size: 2.3rem; font-weight: 800; letter-spacing: -0.5px; color: #fff; }
    .hero p  { margin: .5rem 0 0; font-size: 1.02rem; opacity: .92; color: #fff; }

    .section-label {
        font-size: .78rem; font-weight: 700; letter-spacing: .12em;
        text-transform: uppercase; opacity: .65; margin: 1.3rem 0 .45rem;
    }

    div[data-testid="stTextArea"] textarea {
        border-radius: 14px; font-size: 1rem; line-height: 1.55; padding: 1rem;
    }
    div[data-testid="stButton"] > button {
        width: 100%; border: 0; border-radius: 14px; padding: .8rem 1rem;
        font-weight: 700; font-size: 1.02rem; color: #fff;
        background: linear-gradient(135deg, #6d28d9, #db2777);
        transition: transform .15s ease, box-shadow .15s ease;
    }
    div[data-testid="stButton"] > button:hover {
        transform: translateY(-2px); color: #fff;
        box-shadow: 0 12px 24px -10px rgba(219, 39, 119, .7);
    }

    .card {
        border-radius: 20px; padding: 1.7rem 1.8rem; margin-top: 1.4rem;
        background: rgba(127, 127, 127, 0.08);
        border: 1px solid rgba(127, 127, 127, 0.22);
    }
    .movie-title { font-size: 2rem; font-weight: 800; margin: 0 0 .7rem; line-height: 1.15; }

    .meta { display: flex; flex-wrap: wrap; gap: .55rem; margin-bottom: .4rem; }
    .meta-item {
        padding: .38rem .85rem; border-radius: 12px; font-size: .9rem; font-weight: 600;
        background: rgba(127, 127, 127, 0.14);
    }
    .rating { background: linear-gradient(135deg, #f59e0b, #f97316); color: #fff; }

    .pill {
        display: inline-block; padding: .32rem .85rem; margin: 0 .4rem .45rem 0;
        border-radius: 999px; font-size: .88rem; font-weight: 600;
    }
    .pill-genre { background: rgba(109, 40, 217, .18); border: 1px solid rgba(109, 40, 217, .45); }
    .pill-cast  { background: rgba(219, 39, 119, .15); border: 1px solid rgba(219, 39, 119, .40); }

    .summary {
        font-size: 1.04rem; line-height: 1.7; padding: 1rem 1.2rem;
        border-left: 4px solid #db2777; border-radius: 0 12px 12px 0;
        background: rgba(127, 127, 127, 0.08);
    }
    .muted { opacity: .6; font-style: italic; }
    </style>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    """
    <div class="hero">
        <h1>🎬 Movie Info Extractor</h1>
        <p>Paste any movie paragraph and get clean, structured details in seconds.</p>
    </div>
    """,
    unsafe_allow_html=True,
)

st.markdown('<div class="section-label">Your paragraph</div>', unsafe_allow_html=True)
para = st.text_area(
    "Paragraph",
    height=210,
    placeholder="Paste a movie description here...",
    label_visibility="collapsed",
)

extract = st.button("✨ Extract Information")


# ---------------------------------------------------------------- Rendering
def esc(value) -> str:
    return html.escape(str(value))


def render_movie(m: Movie):
    meta = []
    if m.release_year:
        meta.append(f'<span class="meta-item">📅 {esc(m.release_year)}</span>')
    if m.director:
        meta.append(f'<span class="meta-item">🎬 {esc(m.director)}</span>')
    if m.rating is not None:
        meta.append(f'<span class="meta-item rating">⭐ {esc(m.rating)}</span>')

    genres = "".join(f'<span class="pill pill-genre">{esc(g)}</span>' for g in m.genere) \
        or '<span class="muted">Not mentioned</span>'
    cast = "".join(f'<span class="pill pill-cast">{esc(c)}</span>' for c in m.cast) \
        or '<span class="muted">Not mentioned</span>'

    st.markdown(
        f"""
        <div class="card">
            <div class="movie-title">{esc(m.title)}</div>
            <div class="meta">{"".join(meta)}</div>

            <div class="section-label">Genre</div>
            <div>{genres}</div>

            <div class="section-label">Cast</div>
            <div>{cast}</div>

            <div class="section-label">Summary</div>
            <div class="summary">{esc(m.summary)}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


# ---------------------------------------------------------------- Logic
if extract:
    if not para.strip():
        st.warning("Please paste a paragraph first.")
    else:
        with st.spinner("Reading the paragraph..."):
            try:
                final_prompt = prompt.invoke({
                    "paragraph": para,
                    "format_instructions": parser.get_format_instructions(),
                })
                response = get_model().invoke(final_prompt)
            except Exception as e:
                st.error(f"Something went wrong: {e}")
                st.stop()

        try:
            render_movie(parser.parse(response.content))
        except Exception:
            # If the output can't be parsed, show the model's raw response instead
            st.markdown('<div class="section-label">Result</div>', unsafe_allow_html=True)
            st.code(response.content, language="json")