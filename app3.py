import streamlit as st
import requests

# =========================================================
# PAGE SETTINGS
# =========================================================

st.set_page_config(
    page_title="Keerthi's Chatbot",
    page_icon="🤖",
    layout="centered"
)

# =========================================================
# API KEY
# =========================================================

# For testing, paste your NEW Gemini API key here.
# Do NOT paste your API key into this chat.

GEMINI_API_KEY = "PASTE_YOUR_NEW_API_KEY_HERE"

MODEL = "gemini-3.5-flash"

API_URL = (
    "https://generativelanguage.googleapis.com/"
    f"v1beta/models/{MODEL}:generateContent"
)

# =========================================================
# CSS
# =========================================================

st.markdown(
    """
    <style>

    .stApp {
        background: linear-gradient(
            135deg,
            #dceeff,
            #fff8e7,
            #eaf6ff
        );
    }

    .block-container {
        max-width: 900px;
        padding-top: 2rem;
        padding-bottom: 5rem;
    }

    .robot {
        text-align: center;
        font-size: 58px;
        animation: float 3s ease-in-out infinite;
    }

    @keyframes float {
        0% {
            transform: translateY(0);
        }

        50% {
            transform: translateY(-8px);
        }

        100% {
            transform: translateY(0);
        }
    }

    .title {
        text-align: center;
        font-size: 42px;
        font-weight: 800;
        color: #172554;
        margin-bottom: 5px;
    }

    .subtitle {
        text-align: center;
        color: #475569;
        font-size: 17px;
        margin-bottom: 25px;
    }

    .welcome {
        background: rgba(255,255,255,0.9);
        border-radius: 20px;
        padding: 25px;
        text-align: center;
        margin-bottom: 25px;
        box-shadow: 0 8px 25px rgba(30,64,175,0.12);
    }

    .welcome h2 {
        color: #172554;
        margin-bottom: 10px;
    }

    .welcome p {
        color: #475569;
        font-size: 16px;
        line-height: 1.6;
    }

    [data-testid="stChatMessage"] {
        border-radius: 18px;
        margin-bottom: 12px;
    }

    [data-testid="stChatMessage"] p {
        color: #172033 !important;
        font-size: 16px !important;
        line-height: 1.6 !important;
    }

    [data-testid="stChatInput"] textarea {
        background-color: white !important;
        color: #172033 !important;
        border: 2px solid #93c5fd !important;
        border-radius: 15px !important;
    }

    [data-testid="stChatInput"] textarea::placeholder {
        color: #64748b !important;
    }

    .stButton > button {
        width: 100%;
        border-radius: 12px;
        background: #dbeafe !important;
        color: #172554 !important;
        border: 1px solid #93c5fd !important;
        font-weight: 700;
    }

    .footer {
        text-align: center;
        color: #64748b;
        font-size: 13px;
        margin-top: 25px;
    }

    </style>
    """,
    unsafe_allow_html=True
)

# =========================================================
# SESSION STATE
# =========================================================

if "messages" not in st.session_state:
    st.session_state.messages = []

# =========================================================
# HEADER
# =========================================================

st.markdown(
    '<div class="robot">🤖</div>',
    unsafe_allow_html=True
)

st.markdown(
    "<div class='title'>Keerthi's Chatbot</div>",
    unsafe_allow_html=True
)

st.markdown(
    "<div class='subtitle'>Your friendly AI assistant ✨</div>",
    unsafe_allow_html=True
)

# =========================================================
# WELCOME
# =========================================================

if not st.session_state.messages:

    st.markdown(
        """
        <div class="welcome">
            <h2>👋 Hello!</h2>
            <p>
                Welcome to Keerthi's Chatbot.<br>
                Ask me anything and I'll try my best to help you!
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )

# =========================================================
# CLEAR CHAT
# =========================================================

if st.session_state.messages:

    if st.button("🗑️ Clear Chat"):

        st.session_state.messages = []

        st.rerun()

# =========================================================
# DISPLAY CHAT HISTORY
# =========================================================

for message in st.session_state.messages:

    if message["role"] == "user":

        with st.chat_message("user", avatar="👤"):
            st.markdown(message["content"])

    else:

        with st.chat_message("assistant", avatar="🤖"):
            st.markdown(message["content"])

# =========================================================
# GEMINI API FUNCTION
# =========================================================

def get_gemini_response(messages):

    headers = {
        "Content-Type": "application/json",
        "x-goog-api-key": GEMINI_API_KEY
    }

    contents = []

    for message in messages:

        if message["role"] == "user":
            role = "user"
        else:
            role = "model"

        contents.append(
            {
                "role": role,
                "parts": [
                    {
                        "text": message["content"]
                    }
                ]
            }
        )

    data = {
        "contents": contents
    }

    response = requests.post(
        API_URL,
        headers=headers,
        json=data,
        timeout=60
    )

    # -----------------------------------------------------
    # API ERROR
    # -----------------------------------------------------

    if response.status_code != 200:

        try:
            error_data = response.json()

            error_message = (
                error_data
                .get("error", {})
                .get("message", "Unknown Gemini API error")
            )

        except Exception:

            error_message = response.text

        raise Exception(
            f"HTTP {response.status_code}: {error_message}"
        )

    # -----------------------------------------------------
    # SUCCESS
    # -----------------------------------------------------

    result = response.json()

    try:

        return (
            result["candidates"][0]
            ["content"]["parts"][0]["text"]
        )

    except Exception:

        raise Exception(
            "Gemini returned an unexpected response."
        )


# =========================================================
# CHAT INPUT
# =========================================================

user_input = st.chat_input(
    "Type your message here..."
)

if user_input:

    # Save user message
    st.session_state.messages.append(
        {
            "role": "user",
            "content": user_input
        }
    )

    # Show user message
    with st.chat_message("user", avatar="👤"):

        st.markdown(user_input)

    # Generate response
    with st.chat_message("assistant", avatar="🤖"):

        try:

            answer = get_gemini_response(
                st.session_state.messages
            )

            st.markdown(answer)

            # Save AI response
            st.session_state.messages.append(
                {
                    "role": "assistant",
                    "content": answer
                }
            )

        except Exception as error:

            # IMPORTANT:
            # Show the actual error instead of hiding it.

            st.error(
                f"❌ Gemini API Error:\n\n{error}"
            )

            # Remove failed user message
            if st.session_state.messages:

                st.session_state.messages.pop()

# =========================================================
# FOOTER
# =========================================================

st.markdown(
    """
    <div class="footer">
        Powered by Google Gemini AI • Built with Streamlit 💙
    </div>
    """,
    unsafe_allow_html=True
)
