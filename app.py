import streamlit as st
import pandas as pd
from datetime import datetime
import re

# Load tasks from Excel
tasks_df = pd.read_excel("Task List.xlsx")

st.title("Agentic AI POC")

# Convert tasks to a dictionary
task_dict = {row["S.No"]: row["Task"] for idx, row in tasks_df.iterrows()}

# Streamlit user prompt
user_prompt = st.text_input("Enter your instruction for the agent:")

def simple_agent(prompt, tasks):
    """
    Map user prompt to Excel tasks dynamically.
    """
    prompt = prompt.lower()
    results = []

    for task_no, task_text in tasks.items():
        task_lower = task_text.lower()

        # Match keywords dynamically
        if any(k in prompt for k in ["hello", "greet"]) and "hello" in task_lower:
            results.append(f"Task {task_no}: Hello World!")
        elif any(k in prompt for k in ["time", "timestamp"]) and "timestamp" in task_lower:
            results.append(f"Task {task_no}: Current Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        elif any(k in prompt for k in ["10 times 10", "calculate 10*10"]) and "10 times 10" in task_lower:
            results.append(f"Task {task_no}: 10 times 10 = {10*10}")
        # Generic math detection using regex
        elif re.search(r"\d+\s*[\+\-\*/]\s*\d+", prompt):
            expression = re.search(r"\d+\s*[\+\-\*/]\s*\d+", prompt).group()
            try:
                result = eval(expression)
                results.append(f"Task {task_no}: {expression} = {result}")
            except:
                results.append(f"Task {task_no}: Could not evaluate {expression}")
        else:
            results.append(f"Task {task_no}: Task '{task_text}' skipped (no match)")

    return results

if user_prompt:
    output_results = simple_agent(user_prompt, task_dict)
    for res in output_results:
        st.write(res)


