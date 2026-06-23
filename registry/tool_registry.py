from tools.tools import (
	get_customer_by_name, 
	get_purchase_history,
	get_campaign_history,
	get_product_catalog, 
	recommend_product, 
	choose_channel, 
	generate_campaign,
	save_campaign,
	get_campaign_benchmarks,
	predict_campaign_performance,
	retrieve_similar_campaigns
)

TOOLS = {
	"get_customer_by_name": {
		"function": get_customer_by_name, 
		"inputs": ["customer_name"],
		"outputs": ["customer", "segment"]
	},

	"get_purchase_history": {
		"function": get_purchase_history, 
		"inputs": ["customer"],
		"outputs": ["purchase_history"]
	},

	"get_campaign_history": {
		"function": get_campaign_history,
		"inputs": ["customer"],
		"outputs": ["campaign_history"]
	},

	"get_product_catalog": {
		"function": get_product_catalog,
		"inputs": ["segment"],
		"outputs": ["product_catalog"]
	},

	"recommend_product": {
		"function": recommend_product,
		"inputs": [
			"customer", "purchase_history", "campaign_history", "product_catalog"
		],
		"outputs": ["product"]
	},
	
	"choose_channel": {
		"function": choose_channel, 
		"inputs": [
			"customer", "purchase_history", "product"
		],
		"outputs": ["channel"]
	},

	"retrieve_similar_campaigns": {
		"function": retrieve_similar_campaigns,
		"inputs": [
			"customer",
			"product",
			"segment"
		],
		"outputs": [
			"similar_campaigns"
		]
	},

	"generate_campaign": {
        	"function": generate_campaign,
		"inputs": [
			"customer", "product", "segment", "channel", "similar_campaigns", "feedback"
		],
		"outputs": [
			"subject", "message", "cta"
		]
	},
	
	"save_campaign": {
		"function": save_campaign,
		"inputs": [
			"customer",
			"product",
			"channel",
			"subject",
			"message"
		],
		"outputs": [
			"campaign_saved"
		]
	},

	"get_campaign_benchmarks": {
		"function": get_campaign_benchmarks,
		"inputs": [
			"segment",
			"channel"
		],
		"outputs": [
			"campaign_benchmarks"
		]
	},

	"predict_campaign_performance": {
		"function": predict_campaign_performance, "inputs": [
			"customer", "product", "channel", "message", "campaign_benchmarks"
		],
		"outputs": [
			"predicted_ctr", "predicted_conversion_rate", "predicted_roas"
		]
	}
 }
