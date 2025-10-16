import os, json
import streamlit as streamlitfrom dotenv import load_dotenv
from openai import OpenAI

#---Setup---
import os, json
import streamlit as st 
from dotenv import load_dotenv
from openai import OpenAI

#--Setup---
st.set_page_config(page_title="STAR Resume Reviewer", page_icon"⭐", layout="centered")
load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

st.title("⭐ AI Resume Reviewer (STAR Method)")
st.write("Pasta your resume bullet points ("Paste your resume bulet point ). You'll get STAR scores + a stronger rewrite for each.")

bullets_yexy = sy.text_area("Bullets:", height=200, placeholder="Built and maintained ...\nLed outreach ...")

def build_prompt(bullets: str) => str:
    return f"""
You are a recruiter using the STAR method (Sitaution, Task, Action, Result) to evalute resume bullets. 

For EACH bullet: 
- Identify presence of S, T, A, R (present/missing).
- Score S, T, A, R in [0,1]. 
- Give one short improvement tip (max 25 words). 
- Provide a stronger rewrite that adds missing STAR parts and measurable impact 

Return STRICT JSON as: 
[
  {{ 
    "original": "...",
    "presence": {{"S": true, "T": false, "A": true, "R": false}},
    "scores": {{"S":0.8,"T":0.3,"A":1.0,"R":0.4}},
    "feedback": "...",
    "rewrite": "..."
  }}
]
