import streamlit as st
from agent import InterviewAgent
from evaluation import evaluate_answers

st.title("🧑‍💼 AI Interview Practice Partner")

# ---------------------------
# Sidebar – role selection
# ---------------------------
role = st.sidebar.selectbox(
    "Select interview role",
    ["Software Engineer", "Data Analyst", "Sales"]
)

# Initialize agent only once
if "agent" not in st.session_state:
    st.session_state.agent = InterviewAgent(role)

agent = st.session_state.agent

# ---------------------------
# Chat Message History Display
# ---------------------------
if "messages" not in st.session_state:
    st.session_state.messages = []

st.subheader(f"Interview for: **{role}**")

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])


# ==================================================
# 1️⃣ VOICE INPUT (Speech → Text)
# ==================================================
st.write("🎤 **Optional: Speak your answer**")

audio = st.audio_input("Record your answer here")

user_msg = None  # will store final message (voice or text)

if audio is not None:
    import openai

    st.write("🔄 Transcribing speech...")

    transcript = openai.audio.transcriptions.create(
        file=audio,
        model="gpt-4o-mini-tts"
    )

    user_msg = transcript.text
    st.success(f"🗣️ You said: **{user_msg}**")


# ==================================================
# 2️⃣ TEXT INPUT (fallback-based)
# ==================================================
typed_msg = st.chat_input("Your answer here...")

# Voice input has higher priority; use typed input only if voice wasn’t used
if user_msg is None and typed_msg:
    user_msg = typed_msg


# ==================================================
# Chat Handling
# ==================================================
if user_msg:
    # Log user message
    st.session_state.messages.append({"role": "user", "content": user_msg})

    # Get agent response
    agent_reply = agent.respond(user_msg)

    st.session_state.messages.append({"role": "assistant", "content": agent_reply})

    # Display assistant reply
    with st.chat_message("assistant"):
        st.write(agent_reply)

    # ==================================================
    # 3️⃣ VOICE OUTPUT (Text → Speech)
    # ==================================================
    from gtts import gTTS

    tts = gTTS(agent_reply)
    tts.save("response.mp3")
    st.audio("response.mp3")


# ==================================================
# Generate Final Feedback Button
# ==================================================
if st.button("Generate Final Feedback"):
    transcript = agent.get_transcript()
    feedback = evaluate_answers(transcript)

    st.subheader("📊 Final Interview Feedback")
    st.write(feedback)

    # Also speak the feedback
    from gtts import gTTS

    tts = gTTS(feedback)
    tts.save("feedback.mp3")
    st.audio("feedback.mp3")
