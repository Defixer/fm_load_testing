from constants import LEADS, CUSTOMERS, SITES, CONTACTS, OPPORTUNITIES, JOBS, ASSETS, CUSTOMER_INVOICES, PURCHASE_ORDERS, SUPPLIER_INVOICES, EVENTS, TASKS, NOTES, PLACEHOLDER_HEART, PLACEHOLDER_HEAVEN, PLACEHOLDER_HOLD, TAX_CODES, ACCOUNT_CODES
from constants import UPSERT

def get_request_template(module, user_id, action):
	template = None
	if module == LEADS:
		template = {
			"status": "new",
			"date_follow_up": None,
			"first_name": None,
			"last_name": None,
			"company": None,
			"job_title": None,
			"email_address": None,
			"phone": None,
			"address" : {
				"street": None,
		        "unit": None,
		        "level": None,
		        "city": None,
		        "state": None,
		        "country": None,
		        "zip": None
			},
			"notes": None
		}
	elif module == CUSTOMERS:
		template = {
			"first_name": None,
			"last_name": None,
			"company": None,
			"name": None,
			"email_address": None,			
			"address" : {
				"street": None,
		        "unit": None,
		        "level": None,
		        "city": None,
		        "state": None,
		        "country": None,
		        "zip": None
			},
			"phone": None
		}
	elif module == SITES:
		template = {
			"first_name": None,
			"last_name": None,
			"company": None,
			"customer_id": "",
			"address" : {
				"street": None,
		        "unit": None,
		        "level": None,
		        "city": None,
		        "state": None,
		        "country": None,
		        "zip": None
			},
			"tenant": None,
			"email_address": None
		}
	elif module == CONTACTS:
		template = {
			"first_name": None,
			"last_name": None,
			"company": None,
			"email_address": None,
			"phone": None,
			"address" : {
				"street": None,
		        "unit": None,
		        "level": None,
		        "city": None,
		        "state": None,
		        "country": None,
		        "zip": None
			},
			"notes": None
		}
	elif module == OPPORTUNITIES:
		template = {
			"customer_id": None,
			"site_id": None,
			"contact_id": None,
			"amount": None,
			"status": "prospecting",
			"forecast_close_date": None,
			"summary": None,
			"notes": None
		}
	elif module == JOBS:
		template = {
			"customer_id": None,
			"site_id": None,
			"priority": None,
			"type": None,
			"due_date": None,
			"estimated_timeframe": None,
			"billable": None,
			"po_number": None,
			"work_order_number": None,
			"address" : {
				"street": None,
		        "unit": None,
		        "level": None,
		        "city": None,
		        "state": None,
		        "country": None,
		        "zip": None
			},
			"review_required": None,
			"review_complete": None,
			"date_completed": None,
			"job_summary": None,
			"internal_notes": None
		}
	elif module == ASSETS:
		template = {
			"site_id": None,
			"serial_number": None,
			"asset_type_id": None,
			"attributes": None,
			"level": None,
			"location": None,
			"notes": None,
			"status": None
		}
	elif module == CUSTOMER_INVOICES:
		template = {
			"customer_id": None,
			"site_id": None,
			"job_id": None,
			"contact_id": None,
			"invoice_summary": None,
			"date_invoice": None,
			"date_due": None,
			"show_total_price_only": True,
			"show_labour_details": True,
			"lines": None
		}	
	elif module == PURCHASE_ORDERS:
		template = {
			"customer_id": "",
			"job_id": "",
			"contact_id": "",
			"po_date": None,
			"lines": None
		}
	elif module == SUPPLIER_INVOICES:
		template = {
			"purchase_order_id": None,
			"customer_id": None,
			"contact_id": None,
			"invoice_date": None,
			"invoice_due": None,
			"lines": None
		}
	elif 'LINES' in module:
		template = {
			"product_code": None,
    		"quantity": None,
    		"unit_amount": None,
    		"account_code": None,
    		"tax_code": "INPUT",
    		"discount_rate": None,
    		"department_id": "GUID"
		}
		if 'CI' in module:
			template['tax_code'] = "OUTPUT"
		elif ('PO' in module) or ('SI' in module):
			template['tax_code'] = "INPUT"
	elif module == TAX_CODES:
		template = {
			"name": None,
			"code": None,
			"rate": None
		}
	elif module == ACCOUNT_CODES:
		template = {
			"name": None,
			"code": None
		}
# 	elif module == constants.ACTIVITIES:
# 		mintemplate = {
# 			"module_id": None,
# 			"module_field_name": None,
# 			"note": None,
# 			"module": None,		
# 			"type": body[activity_num]	
# 		}
# 		if body[activity_num] != 2:
# 			template = {			
# 				"assigned_to": None, #user_id
# 				"subject": None,
# 				"module": None,
# 				"activity_date": None,
# 			}
# 			template.update(mintemplate)
	# elif module == ACCOUNT_CODES:
	# 	template = {

	# 	}
	if UPSERT in action:
		template['external_id'] = None
	return template