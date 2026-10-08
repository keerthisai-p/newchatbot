import streamlit as st
from google import genai

# =========================================================
# PAGE CONFIGURATION
# =========================================================

st.set_page_config(
    page_title="Keerthi's Chatbot",
    page_icon="🤖",
    layout="centered"
)

# =========================================================
# GOOGLE GEMINI API
# =========================================================

# Paste your NEW Google AI Studio API key here.
# Never share your API key publicly.

GOOGLE_API_KEY = "AQ.Ab8RN6KhbsEBSlEr6zJdyJieXXHlnMyAJkPXpGcdIUa53Eeuog"

MODEL_NAME = "gemini-3.5-flash-lite"

client = genai.Client(
    api_key=GOOGLE_API_KEY
)

# =========================================================
# CUSTOM CSS
# =========================================================

st.markdown(
    """
    <style>

    /* -------------------------------------------------
       MAIN APPLICATION
    ------------------------------------------------- */

    .stApp {
        background:
            linear-gradient(
                135deg,
                #dceeff 0%,
                #f8f1df 50%,
                #eaf6ff 100%
            );
        min-height: 100vh;
    }

    .block-container {
        max-width: 900px;
        padding-top: 2rem;
        padding-bottom: 5rem;
    }

    /* -------------------------------------------------
       HEADER
    ------------------------------------------------- */

    .robot-icon {
        text-align: center;
        font-size: 60px;
        margin-bottom: 0px;
        animation: robotFloat 3s ease-in-out infinite;
    }

    @keyframes robotFloat {

        0% {
            transform: translateY(0px);
        }

        50% {
            transform: translateY(-8px);
        }

        100% {
            transform: translateY(0px);
        }
    }

    .main-title {
        text-align: center;
        color: #172554 !important;
        font-size: 42px !important;
        font-weight: 800 !important;
        margin-top: 0px;
        margin-bottom: 5px;
    }

    .subtitle {
        text-align: center;
        color: #475569 !important;
        font-size: 17px !important;
        margin-bottom: 25px;
    }

    /* -------------------------------------------------
       WELCOME CARD
    ------------------------------------------------- */

    .welcome-card {
        background: rgba(255, 255, 255, 0.90);
        border: 1px solid #d6e4f0;
        border-radius: 20px;
        padding: 25px;
        margin-bottom: 25px;
        text-align: center;
        box-shadow: 0px 8px 25px rgba(30, 64, 175, 0.10);
    }

    .welcome-heading {
        color: #172554 !important;
        font-size: 23px !important;
        font-weight: 700 !important;
        margin-bottom: 10px;
    }

    .welcome-description {
        color: #475569 !important;
        font-size: 16px !important;
        line-height: 1.6;
    }

    /* -------------------------------------------------
       CHAT AREA
    ------------------------------------------------- */

    [data-testid="stChatMessage"] {
        border-radius: 18px;
        padding: 12px;
        margin-bottom: 12px;
        box-shadow: 0px 5px 15px rgba(15, 23, 42, 0.08);
    }

    /* User message */
    [data-testid="stChatMessage"]:has(
        [data-testid="chatAvatarIcon-user"]
    ) {
        background: #dbeafe;
    }

    /* Assistant message */
    [data-testid="stChatMessage"]:has(
        [data-testid="chatAvatarIcon-assistant"]
    ) {
        background: #fff7df;
    }

    /* Chat text */
    [data-testid="stChatMessage"] p {
        color: #172033 !important;
        font-size: 16px !important;
        line-height: 1.6 !important;
    }

    /* -------------------------------------------------
       CHAT INPUT
    ------------------------------------------------- */

    [data-testid="stChatInput"] {
        background: transparent !important;
    }

    [data-testid="stChatInput"] textarea {
        background: #ffffff !important;
        color: #172033 !important;
        border: 2px solid #93c5fd !important;
        border-radius: 15px !important;
        font-size: 16px !important;
    }

    [data-testid="stChatInput"] textarea::placeholder {
        color: #64748b !important;
    }

    /* -------------------------------------------------
       CLEAR BUTTON
    ------------------------------------------------- */

    .stButton > button {
        width: 100%;
        border-radius: 12px;
        background: #dbeafe !important;
        color: #172554 !important;
        border: 1px solid #93c5fd !important;
        font-weight: 700;
        padding: 10px;
        transition: 0.25s;
    }

    .stButton > button:hover {
        background: #bfdbfe !important;
        transform: translateY(-2px);
    }

    /* -------------------------------------------------
       FOOTER
    ------------------------------------------------- */

    .footer-text {
        text-align: center;
        color: #64748b !important;
        font-size: 13px !important;
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

if "interaction_id" not in st.session_state:
    st.session_state.interaction_id = None

# =========================================================
# HEADER
# =========================================================

st.markdown(
    '<div class="robot-icon">🤖</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="main-title">Keerthi\'s Chatbot</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">Your friendly AI assistant ✨</div>',
    unsafe_allow_html=True
)

# =========================================================
# WELCOME CARD
# =========================================================

if not st.session_state.messages:

    st.markdown(
        """
        <div class="welcome-card">
            <div class="welcome-heading">
                👋 Hello!
            </div>
            <div class="welcome-description">
                Welcome to Keerthi's Chatbot.<br>
                Ask me anything and I'll try my best to help you!
            </div>
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
        st.session_state.interaction_id = None

        st.rerun()

# =========================================================
# DISPLAY PREVIOUS MESSAGES
# =========================================================

for message in st.session_state.messages:

    if message["role"] == "user":

        with st.chat_message(
            "user",
            avatar="👤"
        ):
            st.markdown(message["content"])

    else:

        with st.chat_message(
            "assistant",
            avatar="🤖"
        ):
            st.markdown(message["content"])

# =========================================================
# CHAT INPUT
# =========================================================

user_input = st.chat_input(
    "Type your message here..."
)

# =========================================================
# SEND MESSAGE
# =========================================================

if user_input:

    # -----------------------------------------------------
    # DISPLAY USER MESSAGE
    # -----------------------------------------------------

    st.session_state.messages.append(
        {
            "role": "user",
            "content": user_input
        }
    )

    with st.chat_message(
        "user",
        avatar="👤"
    ):
        st.markdown(user_input)

    # -----------------------------------------------------
    # GENERATE GEMINI RESPONSE
    # -----------------------------------------------------

    with st.chat_message(
        "assistant",
        avatar="🤖"
    ):

        try:

            # First message
            if st.session_state.interaction_id is None:

                interaction = client.interactions.create(
                    model=MODEL_NAME,
                    input=user_input
                )

            # Continue existing conversation
            else:

                interaction = client.interactions.create(
                    model=MODEL_NAME,
                    previous_interaction_id=(
                        st.session_state.interaction_id
                    ),
                    input=user_input
                )

            # Save interaction ID
            st.session_state.interaction_id = interaction.id

            # Get generated text
            assistant_response = interaction.output_text

            if not assistant_response:

                assistant_response = (
                    "Sorry, I couldn't generate a response."
                )

            # Display response
            st.markdown(assistant_response)

            # Save response
            st.session_state.messages.append(
                {
                    "role": "assistant",
                    "content": assistant_response
                }
            )

        except Exception as error:

            error_text = str(error)

            # Authentication error
            if (
                "401" in error_text
                or "UNAUTHENTICATED" in error_text
            ):

                st.error(
                    "🔐 Authentication failed. "
                    "Please check your Gemini API key."
                )

            # Model error
            elif (
                "404" in error_text
                or "NOT_FOUND" in error_text
            ):

                st.error(
                    "⚠️ The Gemini model is not available "
                    "for this API key or project."
                )

            # Server busy
            elif (
                "503" in error_text
                or "UNAVAILABLE" in error_text
            ):

                st.warning(
                    "⏳ Gemini is temporarily busy. "
                    "Please try again in a few seconds."
                )

            # Other errors
            else:

                st.error(
                    "❌ Something went wrong. "
                    "Please check your internet connection, "
                    "API key, and installed packages."
                )

            # Remove failed user message
            if (
                st.session_state.messages
                and
                st.session_state.messages[-1]["role"] == "user"
            ):

                st.session_state.messages.pop()

# =========================================================
# FOOTER
# =========================================================

st.markdown(
    '<div class="footer-text">'
    'Powered by Google Gemini AI • Built with Streamlit 💙'
    '</div>',
    unsafe_allow_html=True
)