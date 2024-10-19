import streamlit as st
from dotenv import load_dotenv
import os
from groq import Groq

load_dotenv()

groq_api_key = os.getenv("GROQ_API_KEY")

client = Groq(api_key=groq_api_key)

topics = ['Geography', 'Health', 'Sports']

def llama_generate_question(topic):
    completion = client.chat.completions.create(
        model="llama-3.2-3b-preview",
        messages=[
            {
                "role": "user",
                "content": f"Generate a random question on the topic {topic}."
            }
        ],
        temperature=1,
        max_tokens=100,
        top_p=1,
        stream=True,
        stop=None,
    )
    
    question = ""
    for chunk in completion:
        question += chunk.choices[0].delta.content or ""
    return question


def llama_validate_answer(question, user_answer):
    completion = client.chat.completions.create(
        model="llama-3.2-3b-preview",
        messages=[
            {
                "role": "user",
                "content": f"Question: {question}\nUser Answer: {user_answer}\nEvaluate the answer and provide feedback."
            }
        ],
        temperature=1,
        max_tokens=200,
        top_p=1,
        stream=True,
        stop=None,
    )
    
    feedback = ""
    for chunk in completion:
        feedback += chunk.choices[0].delta.content or ""
    return feedback


st.title("Q&A Bot for Unimedix")

topic = st.selectbox("Select a topic", topics)

if st.button("Generate Question"):
    if topic:
        question = llama_generate_question(topic)
        st.session_state['question'] = question
        st.write(f"Generated Question: {question}")


if 'question' in st.session_state:
    answer = st.text_input("Your Answer")
    
    
    if st.button("Submit Answer"):
        feedback = llama_validate_answer(st.session_state['question'], answer)

        st.write(f"Question: {st.session_state['question']}")
        st.write(f"Your Answer: {answer}")
    
        st.write(f"Feedback: {feedback}")
        st.write(f"Feedback: {feedback}")