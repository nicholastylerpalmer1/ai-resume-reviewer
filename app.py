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

Bullets:
{bullets}
""".strip()

if st.button("Analyze"):
    if not bullets_text.strip():
        st.warning("Add ar least one bullet")
    else:
        with st.spinner("Reviewing..."):
            prompt = build_prompt(bullets_text.strip())

            resp = client.responses.create(
                model="gpt-4.1-mini",
                temperature=0.3,
                input=prompt,
            )

            raw = resp.output_text

            try:
                data = json.loads(raw)
            except json.JSONDecodeError:
                st.error("Model did not reutrn valid JSON. Showing raw output below.")
                st.code(raw, language="json")
                st.stop()

# Render results
for i, item in enumerate(data, start=1):
    st.markdown(f"### Bullet {i}")
    st.markdown(f"**Original:** {item['original']}")
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("S", f"{item['scores']['S']:.2f}")
    c2.metric("T", f"{item['scores']['T']:.2f}")
    c3.metric("A", f"{item['scores']['A']:.2f}")
    c4.metric("R", f"{item['scores']['R']:.2f}")

    pres = item.get ("presence", {})
    st.caption(
        f"Presence → S: {pres.get('S')}, T: {pres.get('T')}, A: {pres.get('A')}, R: {pres.get('R')}"
    )
    st.write("**Feedback:** " + item["feedback"])
    st.success("**Rewrite:** " + item["rewrite"])
    st.divider()

# Overall averages 
if data:
    avgS = sum(x["scores"]["S"] for x in data)/len(data)
    avgT = sum(x["scores"]["T"] for x in data)/len(data)
    avgA = sum(x["scores"]["A"] for x in data)/len(data)
    avgR = sum(x["scores"]["R"] for x in data)/len(data)
    st.markdown("### Overall STAR Averages")
    a1, a2, a3, a4 = st.columns(4)
    a1.metric("S avg", f"{avgS:.2f}")
    a2.metric("T avg", f"{avgT:.2f}")
    a3.metric("A avg", f"{avgA:.2f}")
    a4.metric("R avg", f"{avgR:.2f}")
    
