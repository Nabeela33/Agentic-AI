import openai
import pandas as pd
import streamlit as st

# Configure API key
openai.api_key = "YOUR_OPENAI_API_KEY"

# Load tasks from Excel
tasks_df = pd.read_excel("tasks.xlsx")

# Simple Agent Function
def simple_agent(task):
    # Ask GPT what to do
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
    
    response = openai.ChatCompletion.create(
        model="gpt-5-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=0,
    )
    
    return response.choices[0].message.content

# Streamlit UI
st.title("Agentic AI POC")

for idx, row in tasks_df.iterrows():
    task = row["Task"]
    decision = simple_agent(task)
    st.write(f"Agent Decision for Task {idx+1}: {decision}")
    
    # Execute action
    import json
    try:
        action_data = json.loads(decision)
        if action_data["action"] == "print_hello":
            print("Hello World")  # prints to terminal
            st.code("Hello World", language="text")
        elif action_data["action"] == "show_message":
            st.success(action_data.get("content", "This is a default Streamlit message!"))
        else:
            st.warning("Unknown action.")
    except Exception as e:
        st.error(f"Error: {e}")
