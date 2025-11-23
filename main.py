import streamlit as st
from agent import InterviewAgent
from evaluation import evaluate_answers
from openai import OpenAI
from gtts import gTTS

client = OpenAI()

st.title("🧑‍💼 AI Interview Practice Partner")

# Sidebar Role Selection
role = st.sidebar.selectbox(
    "Select interview role",
    ["Software Engineer", "Data Analyst", "Sales"]
)

# Initialize session state agent
if "agent" not in st.session_state:
    st.session_state.agent = InterviewAgent(role)

agent = st.session_state.agent

# Load message history
if "messages" not in st.session_state:
    st.session_state.messages = []

st.subheader(f"Interview for: **{role}**")


# Display previous messages
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])


# ====================================================
# 1️⃣ VOICE INPUT (Speech → Text)
# ====================================================
st.write("🎤 Optional: Speak your answer:")

audio = st.audio_input("Record your answer")

user_msg = None

if audio is not None:
    st.write("⏳ Transcribing...")

    transcript = client.audio.transcriptions.create(
        file=audio,
        model="gpt-4o-mini-tts"
    )

    user_msg = transcript.text
    st.success(f"🗣️ You said: {user_msg}")


# ====================================================
# 2️⃣ TEXT INPUT (fallback)
# ====================================================
typed_msg = st.chat_input("Type your answer...")

if user_msg is None and typed_msg:
    user_msg = typed_msg


# ====================================================
# 3️⃣ Chat Handling
# ====================================================
if user_msg:
    st.session_state.messages.append({"role": "user", "content": user_msg})

    agent_reply = agent.respond(user_msg)

    st.session_state.messages.append({"role": "assistant", "content": agent_reply})

    with st.chat_message("assistant"):
        st.write(agent_reply)

    # Voice Output
    tts = gTTS(agent_reply)
    tts.save("response.mp3")
    st.audio("response.mp3")


# ====================================================
# 4️⃣ Feedback Generation
# ====================================================
if st.button("Generate Final Feedback"):
    transcript = agent.get_transcript()
    feedback = evaluate_answers(transcript)

    st.subheader("📊 Final Interview Feedback")
    st.write(feedback)

    # Voice output for feedback
    tts = gTTS(feedback)
    tts.save("feedback.mp3")
    st.audio("feedback.mp3")
