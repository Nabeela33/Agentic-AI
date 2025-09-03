import streamlit as st
import pandas as pd
from datetime import datetime
import re

st.title("Dynamic Agentic AI POC")

# Load Excel tasks dynamically
tasks_df = pd.read_excel("Task List.xlsx")
task_dict = {row["S.No"]: row["Task"] for idx, row in tasks_df.iterrows()}

# Let user select tasks
selected_tasks = st.multiselect(
    "Select tasks to execute:",
    options=[f"{no}: {task}" for no, task in task_dict.items()]
)

def dynamic_agent(task_text):
    """
    Interpret the task text and generate a result dynamically.
    """
    task_lower = task_text.lower()
    results = []

    # Detect math expressions
    math_expressions = re.findall(r"\d+[\+\-\*/]\d+", task_text.replace(" ", ""))
    if math_expressions:
        for expr in math_expressions:
            try:
                results.append(f"{expr} = {eval(expr)}")
            except:
                results.append(f"Could not evaluate {expr}")

    # Detect keywords for text display
    elif any(k in task_lower for k in ["hello", "greet"]):
        results.append("Hello World!")
    elif "time" in task_lower or "timestamp" in task_lower:
        results.append(f"Current Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    else:
        # Generic fallback: just display the task itself
        results.append(f"Task: {task_text}")

    return results

# Execute selected tasks
if selected_tasks:
    st.subheader("Results:")
    for item in selected_tasks:
        no, task = item.split(": ", 1)
        #st.write(f"### Task {no}: {task}")
        outputs = dynamic_agent(task)
        for out in outputs:
            st.write(out)
