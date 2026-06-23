import sys
from core.config import BASE_DIR

sys.path.insert(0, str(BASE_DIR))

import streamlit as st

from agents.mcp_agent.agent_runtime_llm import run_agent

st.title("MCP Marketing Agent")

request = st.text_area(
	"Request",
	"Create a campaign for Alice and assess its performance."
)

if st.button("Run Agent"):

	with st.spinner("Running agent..."):

		result = run_agent(request)

	st.subheader("Response")
	st.write(result["response"])

	st.subheader("Response")
	st.json(result["context"])

	st.subheader("Plan")
	st.json(result["plan"])
