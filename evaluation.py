import openai

def evaluate_answers(conversation_history):
    """Generates final feedback on communication, clarity, depth and improvement points."""
    
    prompt = f"""
    You are an HR expert. Evaluate the candidate's interview performance based on the transcript below.
    Provide structured feedback with:
    - Communication quality
    - Technical depth
    - Professionalism
    - Strong points
    - Weak points
    - Clear improvement suggestions
    
    Transcript:
    {conversation_history}

    Return the feedback in clean bullet-point format.
    """

    response = openai.ChatCompletion.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}]
    )
    
    return response["choices"][0]["message"]["content"]
