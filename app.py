import streamlit as st
from agent_runtime import run_agent
from tools import save_campaign
import plotly.express as px
import pandas as pd

st.title("AI Marketing Agent")

user_request = st.text_input(
	"Request",
	"Create a campaign for Alice and assess its performance."
	)

if st.button("Run Agent"):
	
	st.session_state["result"] = run_agent(user_request)

if "result" in st.session_state:
	
	result = st.session_state["result"]
	context = result["context"]
	customer = context.get("customer", [])

	tab1, tab2, tab3 = st.tabs(
		[
			"Campaign",
			"Performance",
			"Agent Reasoning"
		]
	)
	
	# TAB 1: Campaign
	with tab1:

		if customer:
			st.subheader("Customer")
	
			customer_fields = {
				"name": "Customer",
				"segment": "Segment",
				"last_purchase": "Last Purchase"
			}

			for key, label in customer_fields.items():
				st.write(f"**{label}:** {customer[key]}")
	
		campaign_fields = {
			"subject": "Subject",
			"message": "Message"
		}
	
		if any(field in context for field in campaign_fields):
	
			st.subheader("Campaign")

			for key, label in campaign_fields.items():
				if key in context:
					st.write(f"**{label}:**")
					st.write(context[key])

		if "campaign_history" in context:

				st.subheader("Campaign History")

				st.dataframe(
					context["campaign_history"]
				)

		if "subject" in context and "message" in context:
		
			st.divider()

			if st.button("Save Campaign"):

				save_result = save_campaign(
					customer=context["customer"],
					product=context["product"],
					channel=context["channel"],
					subject=context["subject"],
					message=context["message"]
				)

				st.success("Campaign saved successfully!")

	# TAB 2: Performance
	with tab2:
	
		prediction_fields = {
			"predicted_ctr": ("CTR", "{}%"),
			"predicted_conversion_rate": ("Conversion Rate", "{}%"),
			"predicted_roas": ("ROAS", "{}")
		}


		available_predictions = [
			(key, label, fmt)
			for key, (label, fmt) in prediction_fields.items()
			if key in context
		]

		if available_predictions:
	
			cols = st.columns(len(available_predictions))

			for col, (key, label, fmt) in zip(cols, available_predictions):
				col.metric(label, fmt.format(context[key]))

		if available_predictions and "campaign_benchmarks" in context:

			benchmark = context["campaign_benchmarks"]

			df = pd.DataFrame(
				{
					"Metric": [
						"CTR",
						"Conversion",
						"ROAS"
					],

					"Historical": [
						benchmark["ctr"],
						benchmark["conversion_rate"],
						benchmark["roas"]
					],

					"Predicted": [
						context["predicted_ctr"],
						context["predicted_conversion_rate"],
						context["predicted_roas"]
					]
				}
			)

			fig = px.bar(
				df,
				x="Metric",
				y=["Historical", "Predicted"],
				barmode="group",
				title="Predicted vs Historical Performance"
			)

			st.plotly_chart(fig)

		if "campaign_history" in context:

			history = pd.DataFrame(
				context["campaign_history"]
			)

			if "channel" in history.columns:

				channel_count = (
					history
					.groupby("channel")
					.size()
					.reset_index(name="campaigns")
				)

				fig = px.bar(
					channel_count,
					x="channel",
					y="campaigns",
					title="Campaigns by Channel"
				)

				st.plotly_chart(fig)

	# TAB 3: Reasoning
	with tab3:
		
		st.subheader("Raw Plan")
	
		for i, step in enumerate(result["raw_plan"]["steps"], start=1):
			st.write(f"{i}. {step}")

		st.subheader("Expanded Plan")
	
		for i, step in enumerate(result["expanded_plan"], start=1):
			st.write(f"{i}. {step}")
