from openai import OpenAI
from questions import QUESTION_BANK

client = OpenAI()

class InterviewAgent:

    def __init__(self, role):
        self.role = role.lower()
        self.questions = QUESTION_BANK.get(self.role, [])
        self.index = 0
        self.history = []

    def next_question(self):
        if self.index < len(self.questions):
            q = self.questions[self.index]
            self.index += 1
            return q
        return "That's all the questions. Would you like your final feedback?"

    def analyze_user_message(self, message):
        msg = message.lower()
        if len(msg.strip()) < 3:
            return "confused"
        if "short" in msg or "quick" in msg:
            return "efficient"
        if len(msg.split()) > 40:
            return "chatty"
        if any(k in msg for k in ["asdf", "??!!", "nonsense"]):
            return "edge"
        return "normal"

    def respond(self, user_msg):
        self.history.append({"user": user_msg})

        persona = self.analyze_user_message(user_msg)

        if persona == "confused":
            reply = "I sense you're unsure. Could you tell me more about your experience?"
        elif persona == "efficient":
            reply = "Understood. I'll keep it short. " + self.next_question()
        elif persona == "chatty":
            reply = "Thank you for the detailed response! Here's the next question: " + self.next_question()
        elif persona == "edge":
            reply = "That seems off-topic. Let's get back to the interview. " + self.next_question()
        else:
            reply = "Thanks! Here's the next question: " + self.next_question()

        self.history.append({"assistant": reply})
        return reply

    def get_transcript(self):
        return "\n".join([f"User: {h['user']}\nAgent: {h.get('assistant','')}" for h in self.history])
