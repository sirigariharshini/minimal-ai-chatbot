import streamlit as st
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage

# Load environment variables
load_dotenv()

# -----------------------------
# Page Configuration
# -----------------------------
st.set_page_config(
    page_title="Minimal AI Chatbot",
    page_icon="🤖",
    layout="centered"
)

# -----------------------------
# Title
# -----------------------------
st.title("🤖 Minimal AI Chatbot")
st.caption("Powered by LangChain + Groq")

# -----------------------------
# Initialize LLM
# -----------------------------
llm = ChatGroq(
    model="openai/gpt-oss-20b",
    temperature=0
)

# -----------------------------
# System Prompt
# -----------------------------
SYSTEM_PROMPT = """
You are a helpful AI assistant.
Give clear and accurate answers.
Explain technical concepts in a simple way.
Keep responses concise unless the user asks for more detail.
"""

# -----------------------------
# Initialize Chat History
# -----------------------------
if "messages" not in st.session_state:
    st.session_state.messages = []

# -----------------------------
# Sidebar
# -----------------------------
with st.sidebar:

    st.title("🤖 AI Chatbot")

    st.markdown("---")

    st.subheader("⚙️ Settings")

    st.write("**Model**")
    st.code("openai/gpt-oss-20b")

    st.markdown("---")

    if st.button("🗑️ Clear Chat", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

    st.markdown("---")

    st.subheader("✨ Features")

    st.write("✅ LangChain")
    st.write("✅ Groq LLM")
    st.write("✅ Conversation Memory")
    st.write("✅ Streaming Responses")
    st.write("✅ Clear Chat")

    st.markdown("---")

    st.caption("Built with Python + Streamlit")

# -----------------------------
# Display Previous Messages
# -----------------------------
if not st.session_state.messages:

    st.markdown(
        """
        ### 👋 Welcome!

        I'm your AI assistant. Ask me anything.

        """
    )

    st.markdown("---")
# -----------------------------
# User Input
# -----------------------------
prompt = st.chat_input("Ask me anything...")

if prompt:

    # Display user message
    with st.chat_message("user"):
        st.markdown(prompt)

    # Save user message
    st.session_state.messages.append({
        "role": "user",
        "content": prompt
    })

    # -----------------------------
    # Convert Chat History
    # -----------------------------
    messages = [
        SystemMessage(content=SYSTEM_PROMPT)
    ]

    for message in st.session_state.messages:

        if message["role"] == "user":
            messages.append(
                HumanMessage(content=message["content"])
            )

        elif message["role"] == "assistant":
            messages.append(
                AIMessage(content=message["content"])
            )

    # -----------------------------
    # Get AI Response
    # -----------------------------
    with st.chat_message("assistant"):

        response_text = ""
        message_placeholder = st.empty()

        try:

            for chunk in llm.stream(messages):

                if chunk.content:
                    response_text += str(chunk.content)

                    message_placeholder.markdown(response_text)

        except Exception as e:

            st.error(f"Something went wrong: {e}")

    # -----------------------------
    # Save AI Response
    # -----------------------------
    if response_text:

        st.session_state.messages.append({
            "role": "assistant",
            "content": response_text
        })
