def extract_customer_name(user_request):

	words = user_request.split()
	
	return words[-1]
