from tool_registry import TOOLS

def test_customer_lookup_registered():
	
	assert "get_customer_by_name" in TOOLS

def test_product_recommendation_registered():

	assert "recommend_product" in TOOLS
	
	
