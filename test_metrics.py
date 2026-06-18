from metrics import (calculate_roas, calculate_ctr, calculate_conversion_rate)

def test_roas():	
	assert calculate_roas(6000, 1000)  == 6

def test_ctr():
	assert calculate_ctr(2500, 50000) == 5

def test_conversion_rate():
	assert calculate_conversion_rate(100, 2500) == 4

