from tools import get_customer_segments, get_customer_profile

def test_customer_segments():

	segments = get_customer_segments()

	assert "Luxury Jewelry" in segments
	assert "Budget Shopper" in segments
	assert "Wedding Shopper" in segments

def test_customer_row_count():
	
	profile = get_customer_profile("Alice")

	assert len(profile) == 1
