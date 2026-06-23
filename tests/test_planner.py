from planner import create_plan

def test_campaign_plan():

	plan = create_plan(
	"Create a campaign for Alice"
	)

	assert isinstance(plan, dict)
	
	assert plan["customer_lookup"] is True

	assert plan["campaign_generation"] is True
