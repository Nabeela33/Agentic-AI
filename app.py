import streamlit as st
import pandas as pd
from openai import OpenAI
from datetime import datetime

st.title("Dynamic Agentic AI POC (New OpenAI API)")

# --- Load tasks dynamically from Excel ---
tasks_df = pd.read_excel("Task List.xlsx")
task_dict = {row["S.No"]: row["Task"] for idx, row in tasks_df.iterrows()}

# --- Streamlit multiselect to choose tasks ---
selected_tasks = st.multiselect(
    "Select tasks to execute:",
    options=[f"{no}: {task}" for no, task in task_dict.items()]
)

# --- Initialize OpenAI client ---
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# --- Placeholder tool functions ---
def read_table(table_name):
    return pd.DataFrame({"col1": [1,2,3], "col2": ["A","B","C"]})

def join_tables(table1, table2):
    return pd.DataFrame({"joined_col": [1,2,3]})

def display_message(msg):
    return msg

# --- GPT-based task interpreter ---
def interpret_task(task_text):
    """
    Uses GPT-5-mini to decide what action to perform for a given task description.
    """
    prompt = f"""
    You are an agent. The user provides the following task description:
    \"\"\"{task_text}\"\"\"
    
    Decide what action to perform and provide it as a JSON with:
    {{
      "action": "<action_name>",   # e.g., read_table, join_tables, display_message
      "parameters": "<any_parameters_needed>"
    }}
    """
    
    response = client.chat.completions.create(
        model="gpt-5-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=0
    )
    
    # GPT output as string
    action_text = response.choices[0].message.content.strip()
    
    try:
        # Convert GPT output to dictionary safely
        import json
        action_dict = json.loads(action_text)
        return action_dict
    except:
        # Fallback if GPT output is not valid JSON
        return {"action": "display_message", "parameters": task_text}

# --- Executor ---
def execute_action(action_dict):
    action = action_dict.get("action")
    params = action_dict.get("parameters")

    if action == "read_table":
        df = read_table(params)
        return df
    elif action == "join_tables":
        df = join_tables(params.get("table1"), params.get("table2"))
        return df
    elif action == "display_message":
        return display_message(params)
    else:
        return f"Unknown action: {action}"

# --- Run selected tasks ---
if selected_tasks:
    st.subheader("Results:")
    for item in selected_tasks:
        no, task = item.split(": ", 1)
        st.write(f"### Task {no}: {task}")
        action_dict = interpret_task(task)
        result = execute_action(action_dict)
        
        # Display result
        if isinstance(result, pd.DataFrame):
            st.dataframe(result)
        else:
            st.write(result)
