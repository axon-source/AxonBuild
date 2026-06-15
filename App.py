import streamlit as st
from crewai import Agent, Task, Crew, Process
from langchain_openai import ChatOpenAI
import time

# UI Setup
st.set_page_config(page_title="AxonBuild", page_icon="⚡", layout="wide")

# Custom Styling
st.markdown("""
<style>
.main-title { text-align: center; color: #007BFF; font-size: 50px; font-weight: bold; }
.stApp { background-color: #0E1117; }
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="main-title">⚡ AXONBUILD AI</div>', unsafe_allow_html=True)
st.sidebar.title("AxonBuild Control")

# Engine Logic
def run_axon_engine(task_desc):
    # API Key check
    if "OPENAI_KEY" not in st.secrets:
        st.error("OPENAI_KEY not found in Streamlit Secrets!")
        return None
    
    api_key = st.secrets["OPENAI_KEY"]
    llm = ChatOpenAI(model="gpt-4o-mini", openai_api_key=api_key)
    
    coder = Agent(
        role='Senior Engineer',
        goal='Write clean, efficient code.',
        backstory="Expert Python Developer.",
        llm=llm
    )
    
    reviewer = Agent(
        role='Quality Auditor',
        goal='Critically review code for bugs.',
        backstory="Senior QA Lead.",
        llm=llm
    )
    
    code_task = Task(description=task_desc, agent=coder, expected_output="Production ready Python code")
    review_task = Task(description="Critically review the code above.", agent=reviewer, expected_output="Refined and safe code")
    
    crew = Crew(agents=[coder, reviewer], tasks=[code_task, review_task], process=Process.sequential)
    return crew.kickoff()

# Main Interface
user_input = st.text_area("What do you want AxonBuild to build?", placeholder="Example: Create a calculator app...")

if st.button("🚀 Deploy AxonBuild"):
    if not user_input:
        st.warning("Please provide a task!")
    else:
        with st.status("Initializing AxonBuild Engine...", expanded=True) as status:
            st.write("🕵️‍♂️ Agents assigned...")
            result = run_axon_engine(user_input)
            st.write("✅ Process Complete!")
            status.update(label="Build Complete!", state="complete", expanded=False)
        
        if result:
            st.balloons()
            st.success("AxonBuild has finished the job!")
            st.code(result, language='python')
