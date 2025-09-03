import streamlit as st
import pandas as pd
from datetime import datetime
import re

# Load tasks from Excel
tasks_df = pd.read_excel("Task List.xlsx")

st.title("Agentic AI POC - Task Selector")

# Convert tasks to a dictionary
task_dict = {row["S.No"]: row["Task"] for idx, row in tasks_df.iterrows()}

# Display tasks for selection
selected_tasks = st.multiselect(
    "Select the tasks to execute:",
    options=[f"{no}: {task}" for no, task in task_dict.items()]
)

def execute_task(task_text):
    """
    Executes a task based on its text.
    """
    task_lower = task_text.lower()
    results = []

    if "hello" in task_lower:
        results.append("Hello World!")
    elif "timestamp" in task_lower:
        results.append(f"Current Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    elif "10 times 10" in task_lower:
        results.append(f"10 times 10 = {10*10}")
    # Generic math detection using regex
    elif re.search(r"\d+\s*[\+\-\*/]\s*\d+", task_lower):
        expression = re.search(r"\d+\s*[\+\-\*/]\s*\d+", task_lower).group()
        try:
            result = eval(expression)
            results.append(f"{expression} = {result}")
        except:
            results.append(f"Could not evaluate {expression}")
    else:
        results.append(f"Task '{task_text}' not recognized.")

    return results

# Execute selected tasks
if selected_tasks:
    st.subheader("Results:")
    for item in selected_tasks:
        no, task = item.split(": ", 1)
        task_no = int(no)
        st.write(f"### Task {task_no}: {task}")
        output = execute_task(task)
        for res in output:
            st.write(res)
