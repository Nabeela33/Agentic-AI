import os
from openai import OpenAI

import streamlit as st
from openai import OpenAI

# Load API key from Streamlit secrets
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

def simple_agent(task):
    prompt = f"""
    You are an agent. The task is: {task}.
    Choose one action:
    - print_hello → print 'Hello World'
    - show_message → display a message on Streamlit
    Respond in JSON format:
    {{
        "action": "<action_name>",
        "content": "<message_if_any>"
    }}
    """

    response = client.chat.completions.create(
        model="gpt-4o-mini",  # use an available model
        messages=[{"role": "user", "content": prompt}],
        temperature=0,
    )

    return response.choices[0].message.content

