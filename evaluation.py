from openai import OpenAI
client = OpenAI()

def evaluate_answers(conversation_history):

    prompt = f"""
    You are an HR expert. Evaluate the candidate's interview performance.

    Assess:
    - Communication quality
    - Technical depth
    - Professionalism
    - Strengths
    - Weaknesses
    - Clear improvement suggestions

    Transcript:
    {conversation_history}
    """

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}]
    )

    return response.choices[0].message.content
