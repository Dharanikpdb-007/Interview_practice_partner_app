import openai
import random
from questions import QUESTION_BANK

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
        return "That's all the questions I have. Would you like your feedback now?"

    def analyze_user_message(self, message):
        """Agentic behaviour to categorize user type."""
        msg = message.lower()
        if len(msg.strip()) < 3:
            return "confused"
        if "quick" in msg or "short" in msg:
            return "efficient"
        if len(msg.split()) > 40:
            return "chatty"
        if any(k in msg for k in ["asdf", "??!!", "fsdf", "nonsense"]):
            return "edge"
        return "normal"

    def respond(self, user_msg):
        self.history.append({"user": user_msg})

        persona = self.analyze_user_message(user_msg)

        if persona == "confused":
            reply = "I sense you're unsure. Could you tell me more about your experience?"
        elif persona == "efficient":
            reply = "Sure, I’ll keep things concise. Here's your next question: " + self.next_question()
        elif persona == "chatty":
            reply = "Thanks for the detailed response! To keep us on track, here's the next question: " + self.next_question()
        elif persona == "edge":
            reply = "That seems off-topic. Let's refocus. " + self.next_question()
        else:
            reply = "Thanks! Here's the next question: " + self.next_question()

        self.history.append({"assistant": reply})
        return reply

    def get_transcript(self):
        return "\n".join([f"User: {h['user']}\nAgent: {h.get('assistant','')}" for h in self.history])
