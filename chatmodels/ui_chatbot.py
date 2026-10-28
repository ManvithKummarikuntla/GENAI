from dotenv import load_dotenv
load_dotenv()

import streamlit as st
from langchain_groq import ChatGroq
from langchain_core.messages import SystemMessage, AIMessage, HumanMessage

st.set_page_config(page_title="AI Chatbot", page_icon="🤖", layout="centered")

MODES = {
    "teacher": {
        "label": "Teacher Mode",
        "icon": "🎓",
        "desc": "Clear, patient and responsible answers that help you learn.",
        "prompt": "You are a teaching agent and you need to reply responsiblily",
    },
    "funny": {
        "label": "Funny Mode",
        "icon": "😂",
        "desc": "Witty, playful replies that keep the conversation light.",
        "prompt": "You are a funny agent can give reply in funny way",
    },
}

# ---------- Styling ----------
st.markdown(
    """
    <style>
    .stApp {
        background: linear-gradient(135deg, #0f172a 0%, #1e1b4b 55%, #312e81 100%);
    }
    #MainMenu, footer {visibility: hidden;}

    .hero-title {
        text-align: center;
        font-size: 2.6rem;
        font-weight: 800;
        background: linear-gradient(90deg, #a78bfa, #60a5fa, #34d399);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.2rem;
    }
    .hero-sub {
        text-align: center;
        color: #cbd5e1;
        font-size: 1.05rem;
        margin-bottom: 2rem;
    }
    .mode-card {
        background: rgba(255, 255, 255, 0.07);
        border: 1px solid rgba(255, 255, 255, 0.15);
        border-radius: 18px;
        padding: 1.4rem 1rem 0.6rem 1rem;
        text-align: center;
        backdrop-filter: blur(8px);
        min-height: 170px;
    }
    .mode-icon {font-size: 2.6rem;}
    .mode-name {color: #f1f5f9; font-size: 1.25rem; font-weight: 700; margin: 0.3rem 0;}
    .mode-desc {color: #cbd5e1; font-size: 0.92rem;}

    .stButton > button {
        width: 100%;
        border-radius: 12px;
        border: none;
        color: white;
        font-weight: 600;
        padding: 0.6rem 1rem;
        background: linear-gradient(90deg, #7c3aed, #2563eb);
    }
    .stButton > button:hover {
        filter: brightness(1.15);
        color: white;
    }

    [data-testid="stChatMessage"] {
        background: rgba(255, 255, 255, 0.06);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 16px;
        padding: 0.8rem 1rem;
    }
    [data-testid="stChatMessage"] p {color: #f1f5f9;}

    [data-testid="stSidebar"] {
        background: rgba(15, 23, 42, 0.9);
    }
    [data-testid="stSidebar"] * {color: #e2e8f0;}
    </style>
    """,
    unsafe_allow_html=True,
)

# ---------- Session state ----------
if "mode" not in st.session_state:
    st.session_state.mode = None
if "messages" not in st.session_state:
    st.session_state.messages = []
if "llm" not in st.session_state:
    st.session_state.llm = ChatGroq(model="openai/gpt-oss-20b")


def select_mode(key):
    st.session_state.mode = key
    st.session_state.messages = [SystemMessage(content=MODES[key]["prompt"])]


def change_mode():
    st.session_state.mode = None
    st.session_state.messages = []


# ---------- Screen 1: choose AI model / mode ----------
if st.session_state.mode is None:
    st.markdown('<div class="hero-title">🤖 AI Chatbot</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="hero-sub">Choose your AI mode to get started</div>',
        unsafe_allow_html=True,
    )

    cols = st.columns(2, gap="large")
    for col, (key, m) in zip(cols, MODES.items()):
        with col:
            st.markdown(
                f"""
                <div class="mode-card">
                    <div class="mode-icon">{m['icon']}</div>
                    <div class="mode-name">{m['label']}</div>
                    <div class="mode-desc">{m['desc']}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )
            st.button(
                f"Select {m['label']}",
                key=f"select_{key}",
                on_click=select_mode,
                args=(key,),
            )

# ---------- Screen 2: chat ----------
else:
    m = MODES[st.session_state.mode]

    with st.sidebar:
        st.markdown(f"### {m['icon']} {m['label']}")
        st.caption(m["desc"])
        st.button("🔄 Change mode", on_click=change_mode)

    st.markdown(
        f'<div class="hero-title">{m["icon"]} {m["label"]}</div>',
        unsafe_allow_html=True,
    )
    st.markdown(
        '<div class="hero-sub">Ask me anything below</div>',
        unsafe_allow_html=True,
    )

    for message in st.session_state.messages:
        if isinstance(message, HumanMessage):
            with st.chat_message("user", avatar="🧑"):
                st.write(message.content)
        elif isinstance(message, AIMessage):
            with st.chat_message("assistant", avatar="🤖"):
                st.write(message.content)

    prompt = st.chat_input("Type your message...")

    if prompt:
        with st.chat_message("user", avatar="🧑"):
            st.write(prompt)
        st.session_state.messages.append(HumanMessage(content=prompt))

        response = st.session_state.llm.invoke(st.session_state.messages)

        with st.chat_message("assistant", avatar="🤖"):
            st.write(response.content)
        st.session_state.messages.append(AIMessage(content=response.content))