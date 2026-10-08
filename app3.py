import streamlit as st
import requests

# =========================================================
# PAGE CONFIG
# =========================================================

st.set_page_config(
    page_title="Keerthi's Chatbot",
    page_icon="🤖",
    layout="centered"
)

# =========================================================
# API SETTINGS
# =========================================================

# Put your NEW Gemini API key here
GEMINI_API_KEY = "PASTE_YOUR_NEW_API_KEY_HERE"

MODEL_NAME = "gemini-3.5-flash-lite"

API_URL = (
    f"https://generativelanguage.googleapis.com/"
    f"v1beta/models/{MODEL_NAME}:generateContent"
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
            #dceeff 0%,
            #f8f1df 50%,
            #eaf6ff 100%
        );
    }

    .block-container {
        max-width: 900px;
        padding-top: 2rem;
        padding-bottom: 5rem;
    }

    .robot {
        text-align: center;
        font-size: 60px;
        animation: floating 3s ease-in-out infinite;
    }

    @keyframes floating {
        0% { transform: translateY(0px); }
        50% { transform: translateY(-8px); }
        100% { transform: translateY(0px); }
    }

    .title {
        text-align: center;
        color: #172554;
        font-size: 42px;
        font-weight: 800;
    }

    .subtitle {
        text-align: center;
        color: #475569;
        font-size: 17px;
        margin-bottom: 25px;
    }

    .welcome {
        background: white;
        border-radius: 20px;
        padding: 25px;
        text-align: center;
        margin-bottom: 25px;
        box-shadow: 0 8px 25px rgba(30,64,175,0.10);
    }

    .welcome h2 {
        color: #172554;
    }

    .welcome p {
        color: #475569;
        font-size: 16px;
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
        background: white !important;
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
# WELCOME MESSAGE
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
# GEMINI FUNCTION
# =========================================================

def ask_gemini(conversation):

    headers = {
        "Content-Type": "application/json",
        "x-goog-api-key": GEMINI_API_KEY
    }

    contents = []

    for message in conversation:

        role = "user" if message["role"] == "user" else "model"

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

    if response.status_code != 200:

        try:
            error_data = response.json()
            error_message = error_data.get(
                "error",
                {}
            ).get(
                "message",
                "Unknown API error"
            )
        except Exception:
            error_message = response.text

        raise Exception(
            f"{response.status_code}: {error_message}"
        )

    result = response.json()

    return result["candidates"][0]["content"]["parts"][0]["text"]


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

    # Display user message
    with st.chat_message("user", avatar="👤"):
        st.markdown(user_input)

    # Generate AI response
    with st.chat_message("assistant", avatar="🤖"):

        try:

            answer = ask_gemini(
                st.session_state.messages
            )

            st.markdown(answer)

            st.session_state.messages.append(
                {
                    "role": "assistant",
                    "content": answer
                }
            )

        except Exception as error:

            error_text = str(error)

            if "401" in error_text:

                st.error(
                    "🔐 API key problem. "
                    "Please create a new Gemini API key."
                )

            elif "403" in error_text:

                st.error(
                    "🚫 Your API key does not have "
                    "permission to use the Gemini API."
                )

            elif "404" in error_text:

                st.error(
                    "⚠️ The selected Gemini model is "
                    "not available for this API key."
                )

            elif "429" in error_text:

                st.warning(
                    "⏳ API limit reached. "
                    "Please wait and try again."
                )

            elif "503" in error_text:

                st.warning(
                    "⏳ Gemini is temporarily busy. "
                    "Please try again."
                )

            else:

                st.error(
                    "❌ Something went wrong."
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
