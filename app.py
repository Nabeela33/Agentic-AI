import streamlit as st
import pandas as pd
import openai
import os

# Load tasks from Excel
tasks_df = pd.read_excel("Task List.xlsx")
task_dict = {row["S.No"]: row["Task"] for idx, row in tasks_df.iterrows()}

# Let user select tasks
selected_tasks = st.multiselect(
    "Select tasks to execute:",
    options=[f"{no}: {task}" for no, task in task_dict.items()]
)

# Set OpenAI API key
openai.api_key = st.secrets["OPENAI_API_KEY"]

def interpret_task(task_description):
    """
    Use GPT-5-mini to interpret the task description and determine the required action.
    """
    prompt = f"Interpret the following task description and determine the required action:\n\n{task_description}\n\nAction:"
    response = openai.Completion.create(
        model="gpt-5-mini",
        prompt=prompt,
        temperature=0,
        max_tokens=100
    )
    action = response.choices[0].text.strip()
    return action

def execute_action(action):
    """
    Execute the action determined by GPT-5-mini.
    """
    if "read table" in action:
        # Placeholder for reading a table
        return "Reading table..."
    elif "join tables" in action:
        # Placeholder for joining tables
        return "Joining tables..."
    elif "display message" in action:
        # Placeholder for displaying a message
        return "Displaying message..."
    else:
        return "Action not recognized."

# Execute selected tasks
if selected_tasks:
    for item in selected_tasks:
        no, task = item.split(": ", 1)
        st.write(f"### Task {no}: {task}")
        action = interpret_task(task)
        result = execute_action(action)
        st.write(f"Action: {action}")
        st.write(f"Result: {result}")
