import streamlit as st
import pandas as pd
from datetime import datetime
import re

st.title("Dynamic Agentic AI POC - Task Selector")

# Load Excel dynamically
tasks_df = pd.read_excel("Task List.xlsx")
task_dict = {row["S.No"]: row["Task"] for idx, row in tasks_df.iterrows()}

# Let user select tasks
selected_tasks = st.multiselect(
    "Select tasks to execute:",
    options=[f"{no}: {task}" for no, task in task_dict.items()]
)

# Example tool functions (can expand later)
def read_table_from_gcp(table_name):
    # Placeholder function for reading GCP table
    return pd.DataFrame({"col1": [1,2,3], "col2": ["a","b","c"]})

def join_tables(table1, table2):
    # Placeholder function for joining tables
    return pd.DataFrame({"joined_col": [1,2,3]})

def display_message(msg):
    return msg

# Dynamic interpreter
def interpret_and_execute(task_text):
    """
    Decide the operation based on the task description.
    Currently uses basic keyword parsing. 
    Can be replaced with LLM later.
    """
    task_lower = task_text.lower()
    results = []

    # Detect GCP table read
    if "read table" in task_lower or "retrieve" in task_lower:
        table_name = task_text.split()[-1]  # simple example
        df = read_table_from_gcp(table_name)
        results.append(df)

    # Detect join
    elif "join" in task_lower:
        results.append(join_tables("table1","table2"))

    # Detect display message
    elif "display" in task_lower or "message" in task_lower:
        results.append(display_message(task_text))

    else:
        results.append(f"Task: '{task_text}' - operation not recognized")

    return results

# Execute selected tasks dynamically
if selected_tasks:
    st.subheader("Results:")
    for item in selected_tasks:
        no, task = item.split(": ", 1)
        st.write(f"### Task {no}: {task}")
        outputs = interpret_and_execute(task)
        for out in outputs:
            if isinstance(out, pd.DataFrame):
                st.dataframe(out)
            else:
                st.write(out)
