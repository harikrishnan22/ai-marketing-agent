from tools import recommend_product

def test_luxury_jewelry():
	assert(recommend_product("Luxury Jewelry") == "Premium Necklace Collection")

def test_budget_shopper():
	assert(recommend_product("Budget Shopper") == "Discounted Ring Collection")
