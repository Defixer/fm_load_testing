from datetime import datetime, timedelta
import uuid
import string
import constants
import logging
import sys
import random
import json
import pandas as pd
from constants import FETCH, CREATE, UPSERT, UPSERT_INSERT, UPSERT_UPDATE, UPDATE, SEARCH, REQUEST, RESPONSE, FM_DN
from constants import LEADS, CUSTOMERS, SITES, CONTACTS, OPPORTUNITIES, JOBS, ASSETS, CUSTOMER_INVOICES, PURCHASE_ORDERS, SUPPLIER_INVOICES, EVENTS, TASKS, NOTES, LINES_DESCRIPTION, PLACEHOLDER_HEART, PLACEHOLDER_HEAVEN, PLACEHOLDER_HOLD, TAX_CODES, ACCOUNT_CODES
from data_model import get_request_template
import os
import sys
import traceback
import resource
from textwrap import wrap

RECORD_ID = 'p'
test_data_file = "test_data.csv"
ID = 'id'
EXT_ID = 'external_id'
fm_data = "fm_data.csv"

def get_logger(logfile):
	#create logger
	log = logging.getLogger()	
	log.setLevel(logging.INFO)

	# create formatter and add it to the handlers
	formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

	# create file handler which logs even debug messages
	fh = logging.FileHandler(logfile)
	fh.setLevel(logging.INFO)
	fh.setFormatter(formatter)
	log.addHandler(fh)

	return log

def get_error_message(instance):
	exc_type, exc_obj, exc_tb = sys.exc_info() #error type, error object, error filename of the last stack traceback
	# fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1] #filename of the last stack traceback
	# print(exc_type, fname, exc_tb.tb_lineno) 
	exc_stacks = traceback.format_exc().split("File")
	instance.log.info("<ERROR FOUND>")
	for stack in exc_stacks:
		
		if "Traceback" in stack: #skips the exception stack with Traceback; no info needed there
			continue
		exc = tuple(stack.split("\n"))
		exc_0, exc_1, exc_error = exc[:3]		
		exc_error = exc_error.strip() #strips "blank" data of whitespaces resulting to empty string
		if exc_error == "": #guarantees that exception error is never empty
			exc_error = str(exc_type)
		exc_0 = tuple(exc_0.split(","))
		exc_file, exc_line, exc_func = exc_0
		exc_file = exc_file.split("/")[-1].strip("\"") #removes unaesthetical double qoute on file name
		exc_func = "{}, {}".format(exc_func.strip(), exc_1.strip()) #removes whitespaces to the function where the exception occurred
		instance.log.info("\t({}, {}, {}, {})".format(exc_file, exc_line, exc_func, exc_error))
	instance.log.info("</ERROR FOUND>\n")

def log_req_res(data, instance):	
	response_text = None
	if len(data[RESPONSE].text) > 300:
		response_text = "{} ..".format(data[RESPONSE].text[:300])
	else:
		response_text = json.loads(data[RESPONSE].text)
		response_text = prettify(response_text)
	header = "{} {} | Username: {} Password: {}".format(data["action"].title(), data["module"].title(), instance.username, instance.password)
	req = "{} Request: {}".format(data['action'], prettify(data[REQUEST]))
	res = "{} Response | Code: {} | Response Msg: {}".format(data['action'], data[RESPONSE], response_text)
	instance.log.info("\n\n{}\n{}\n{}\n".format(header, req, res))

def get_date_formats(): #dashes are required for date or it'll throw Bad Request
	date_formats = {}
	date_formats['current_date'] = datetime.now().strftime("%Y-%m-%d")
	date_formats['current_time_micro'] = datetime.now().strftime("%H:%M:%S.%f")
	date_formats['current_time'] = datetime.now().strftime("%H:%M:%S")
	date_formats['next_day_date'] = (datetime.strptime(date_formats['current_date'], '%Y-%m-%d') + timedelta(days=1)).strftime("%Y-%m-%d")

	return date_formats

def get_headers(instance):
	headers = {}
	headers['auth'] = (instance.username, instance.password)
	headers['params'] = {
		'Content-Type': 'application/json',
		'Accept':'application/json',
		'Client-Id': instance.client_id
	}
	return headers

def set_data(module, action, request, response):
	data = {
		"module": module,
		"action": action,
		REQUEST: request,
		RESPONSE: response
	}

	return data

def fetch(module, action, instance):
	headers = get_headers(instance)	
	url = "/{}".format(module.lower())
	request = "{}{}".format(FM_DN, url) #Request URL of the module	
	response = instance.client.get(url, auth=headers['auth'], headers=headers['params'])
	data = set_data(module, action, request, response)
	return data

def create(module, action, instance):
	headers = get_headers(instance)
	url = "/{}".format(module.lower())
	number_of_records = random.randint(1,3) #picks between 1-3 [inclusive] number of records to be created
	request = set_independent_request(module, action, number_of_records, instance)	
	response = instance.client.post(url, auth=headers['auth'], headers=headers['params'], json=request)
	data = set_data(module, action, request, response)
	return data

def update(module, action, instance):
	headers = get_headers(instance)
	url = "/{}".format(module.lower())
	request = create_update_request(module, action, instance)
	response = instance.client.put(url, auth=headers['auth'], headers=headers['params'], json=request)
	data = set_data(module, action, request, response)
	return data

def create_update_request(module, action, instance):
	request = []
	api_data_df = get_api_data(module, action, instance)
	# api_data_df.to_csv(fm_data, sep=',', encoding='utf-8', index=False)
	ids = None

	if action == UPDATE:
		up_id = ID
		ids = api_data_df[up_id].dropna().tolist()
		request = process_update(ids, up_id, module, action, api_data_df, instance)		
		return request
	elif UPSERT in action:
		up_id = EXT_ID
		ids = api_data_df[up_id].dropna().tolist()
		request = process_upsert(ids, up_id, module, instance, instance.user_id, api_data_df, action)				
		return request

def process_update(ids, up_id, module, action, df, instance):
	request = []
	record_id = random.choice(ids)
	raw_body = get_request_template(module, instance.user_id, action)
	number_of_items = len(raw_body)
	while number_of_items > 2:
		field_name = random.choice(list(raw_body.keys()))
		if is_independent_field(module, field_name):
			raw_body.pop(field_name)
		number_of_items = number_of_items - 1
	raw_body = traverse_dict(raw_body, module, action, instance)
	raw_body = remove_data_placeholders(module, raw_body)
	raw_body[up_id] = record_id
	request.append(raw_body)

	'''
		just to check what have been updated
	'''
	show_updates(up_id, record_id, raw_body, request, df, instance) 
	return request

def is_independent_field(module, field_name):
	if field_name in ['name', 'company']:
		return False
	return True

def show_updates(up_id, record_id, raw_body, request, api_data_df, instance):
	field_list = [x for x in raw_body]
	orig_data = api_data_df.loc[api_data_df[up_id]==record_id, field_list].values.tolist()
	original = orig_data[0]
	updated = request[0]
	i = 0 
	for field in field_list:
		this_log = "{}: {} -> {}".format(field, original[i], updated[field])
		instance.log.info(this_log)
		i += 1

def search(module, action, instance):
	search_module = set_search_endpoint(module, action, instance)
	data = fetch(search_module, action, instance)
	return data

def set_search_endpoint(module, action, instance):
	api_filter = "?next_token=&"
	# data_df = pd.read_csv(test_data_file)
	api_data_df = get_api_data(module, action, instance)
	raw_body = get_request_template(module, instance.user_id, action)
	field_name = None
	while (field_name is None) or (field_name == "notes") or (field_name == "address"): #try-catch 'notes' and 'address' for a while
		try:
			field_name = random.choice(list(raw_body.keys()))
		except:
			pass
		
	field_value = get_random_data(field_name, api_data_df, instance)
	endpoint = "{}{}{}={}".format(module.lower(), api_filter, field_name, field_value)
	return endpoint

def upsert(module, action, instance):	
	headers = get_headers(instance)
	url = "/{}/upsert".format(module.lower())
	subtask = random.choice([UPSERT_INSERT, UPSERT_UPDATE])
	request = None	
	if subtask == UPSERT_INSERT:
		number_of_records = random.randint(1,3)
		request = set_independent_request(module, subtask, number_of_records, instance)	
	elif subtask == UPSERT_UPDATE:
		request = create_update_request(module, subtask, instance)
	
	response = instance.client.post(url, auth=headers['auth'], headers=headers['params'], json=request)
	
	data = set_data(module, subtask, request, response)
	return data

def traverse_dict(d, module, action, instance): 	
	for name, value in d.items(): #iterates dict 'd' until non-dict 'value' is found
		if isinstance(value, dict):
			traverse_dict(value, module, action, instance)
		elif isinstance(value, list):
			test_data = get_test_data(d, name, value, module, action, instance)
			d[name].append(test_data)
		else:
			d[name] = get_test_data(d, name, value, module, action, instance)
	return d

def prettify(this_json): #returns a pretty-print json	
	return json.dumps(this_json, indent=4)

def set_independent_request(module, action, number_of_records, instance):
	request = []
	for i in range(number_of_records):
		raw_body = {}
		raw_body = get_request_template(module, instance.user_id, action)
		raw_body = traverse_dict(raw_body, module, action, instance)
		raw_body = remove_data_placeholders(module, raw_body)
		request.append(raw_body)
	return request

def remove_data_placeholders(module, raw_body):
	if module in [CUSTOMERS, SITES]:
		for element in ['first_name', 'last_name', 'company']:
			raw_body.pop(element)
	elif module in [CONTACTS]:
		raw_body.pop('company')
	return raw_body

def rand_num(n, pad, datatype):
	range_start = 0
	if '!' not in pad:
		range_start = 10**(n-1) #** is exponent; 10^(n-1)
	range_end = (10**n)-1 #** is exponent; (10^n)-1

	random_number = random.randint(range_start, range_end)
	if 'f' in datatype: #creates random n-decimal float (nf)
		random_number = round(random.uniform(range_start, range_end), int(datatype[0])) #int(datatype[0]) converts first char of datatype into int
	return random_number

def rand_alpha(n):
	return ''.join(random.choice(string.ascii_uppercase) for x in range(n))

def get_random_data(header, data_df, instance):	
	random_item = None	
	# data_df = pd.read_csv(test_data_file)

	#drops all NaN values and converts the DataFrame into a list
	data_list = data_df[header].dropna().tolist()

	try:
		#choose random item in the list
		random_item = random.choice(data_list) 
	except IndexError:
		instance.log.info("<ERROR FOUND>".format())
		instance.log.info("Empty \'{}\' list".format(header))
		instance.log.info("</ERROR FOUND>\n")
	return random_item

def get_assets(test_data_file, number_of_items, instance):
	attributes = {}
	data_df = pd.read_csv(test_data_file)

	for i in range(number_of_items):
		name = get_random_data(ASSETS, data_df, instance)
		value = str(rand_num(4,'!padded', 'd')) #picks number from 0-9999
		attributes[name] = value
		# attributes.append(asset)

	return attributes

def append_lines_desc(lines, test_data_file, instance):
	data_df = pd.read_csv(test_data_file)
	for line in lines:
		line['description'] = get_random_data(LINES_DESCRIPTION, data_df, instance)
	return lines

def get_lines(test_data_file, number_of_items, module, instance):
	submodule_list = module.split("_")
	submodule = "{}{}_LINES".format(submodule_list[0][0], submodule_list[1][0]) #gets the first character of submodule in the list
	lines = set_independent_request(submodule, CREATE, number_of_items, instance)
	lines = append_lines_desc(lines, test_data_file, instance)

	return lines

def process_upsert(ids, up_id, module, instance, user_id, df, action):
	request = None
	number_of_records = random.randint(1,3)
	if not ids: #check if list 'ids' is empty
		request = set_independent_request(module, action, number_of_records, instance) #set_independent_request
	else: 
		request = random.choice([set_independent_request(module, action, number_of_records, instance), 
								process_update(ids, up_id, module, action, df, instance)])

	return request

def get_api_data(module, action, instance):
	data = fetch(module, action, instance)
	response_text = data[RESPONSE].text
	response_body = json.loads(response_text)
	api_data_json = response_body["data"]
	api_data_df = pd.DataFrame.from_dict(api_data_json)
	return api_data_df

def get_name(header, test_data_file, instance):
	data_df = pd.read_csv(test_data_file)
	name = get_random_data(header, data_df, instance)
	return name

def get_phone():
	phone = {
		"home": "",
		"mobile": "",
		"work": ""
	}
	odds = random.randint(0,2)
	if odds > 0:
		for i in range(odds): #randomly removes either 1 or 2 phone numbers
			phone.pop(random.choice(list(phone.keys())))
	for name, number in list(phone.items()):
		for i in range(3):
			number += str(rand_num(3,'padded', 'd')) #picks number between 100-999
			number_list = wrap(number, 3) #splits phone number into 3-character each
		phone[name] = "-".join(number_list) #combine phone number with "-"
	return phone	

def get_record_id(module, instance):
	data = fetch(module, FETCH, instance)
	response_data = json.loads(data[RESPONSE].text)
	records = response_data['data']
	record = random.choice(records)
	return record['id']

def get_tax_code_name(header, test_data_file, instance):
	data_df = pd.read_csv(test_data_file)
	tax_code_name = get_random_data(header, data_df, instance)
	return tax_code_name

def get_test_data(d, field_name, field_value, module, action, instance):
	data = field_value
	date_formats = get_date_formats()	
	global test_data_file
	if field_name in ['first_name', 'last_name', 'company']:				
		data = get_name(field_name.upper(), test_data_file, instance)
		if 'company' in d:
			if 'name' in d:
				d['name'] = d['company']
	elif field_name == 'tenant':
		data = "{} {}".format(d['first_name'], d['last_name'])
	elif field_name in ['customer_id', 'site_id', 'contact_id', 'job_id', 'purchase_order_id']:
		this_module = "{}s".format(field_name.split("_id")[0]).upper()
		data = get_record_id(this_module, instance)
	elif field_name == 'phone':
		data = get_phone()
	elif field_name == 'email_address':
		website = ""
		if 'name' in d:
			website = 'name'
		else:
			website = 'company'
		email = "{}{}@{}.com".format(d['first_name'][0], d['last_name'], d[website]).lower()
		data = [email]
	elif field_name in ['asset_type_id']:
		data = str(uuid.uuid4()) #generates random UUID
	elif any(field in field_name for field in ['notes', 'summary']): #if field_name has 'notes' or 'summary' anywhere
		placeholders = [PLACEHOLDER_HEART, PLACEHOLDER_HEAVEN, PLACEHOLDER_HOLD]
		data = random.choice(placeholders)
	elif 'city' in field_name:
		data = "Makati" 
	elif 'state' in field_name:
		data = "MKT"
	elif 'country' in field_name:
		data = "PH"
	elif field_name == 'date_follow_up':
		#create date as "YYYY-MM-DD HH:MM:SS"
		data = "{} {}".format(date_formats['next_day_date'], date_formats['current_time'])
	elif field_name in ['forecast_close_date', 'due_date', 'date_invoice', 'date_due', 'po_date', 'invoice_date', 'invoice_due']:
		data = date_formats['next_day_date']		
	elif field_name == 'date_completed':
		if d['review_complete'] == 1:
			data = d['due_date']	
		else:
			data = ""
	elif 'street' in field_name:
		data = str(rand_alpha(3)) #creates random 3-letter word
	elif ('unit' in field_name) or (field_name == 'account_code'):
		data = str(rand_num(3,'padded', 'd')) #picks number between 100-999
		if '_amount' in field_name:
			data = str(rand_num(5,'!padded', '2f')) #picks number between 0.00-99999.99
	elif field_name == 'amount':
		data = str(rand_num(5,'!padded', '2f')) #picks number between 0.00-99999.99
	elif field_name in ['addr_level', 'quantity', 'discount_rate']:
		data = str(rand_num(2,'!padded', 'd')) #picks number between 0-99	
	elif field_name in ['zip', 'estimated_timeframe']:
		data = str(rand_num(4,'padded', 'd')) #picks number 1000-9999
	elif field_name in ['work_order_number']:
		data = str(rand_num(6, 'padded', 'd')) #picks number from 100000-999999
	elif field_name in ['po_number']:
		data = str(rand_num(8, 'padded', 'd')) #picks number from 10000000-99999999
	elif field_name == "serial_number":
		data = rand_num(9, 'padded', 'd') #picks number from 10000000-99999999
	elif field_name in ['billable', 'review_required', 'review_complete']:
		data = random.randint(0,1) #picks number from 0-1
		if 'review_required' in d: #review_complete should always be 0 if review_required is 0
			if 'review_required' == 0:
				data = d[review_required]
	elif field_name == 'product_code':
		data = "ELEC{}".format(rand_num(3,'padded','d')) #picks number between 100-999
	elif field_name == 'location':
		data = "{} {} {} {}".format(rand_alpha(3), rand_num(3,'padded', 'd'), rand_num(2,'!padded', 'd'), "Makati")	
	elif field_name == 'company':
		data = "{0}-{0}".format("p{}_test{}".format(module[:2], rand_num(6, '!padded', 'd')))
	elif field_name == 'priority':
		data = random.choice(['Low', 'Normal', 'High', 'Urgent'])
	elif field_name == 'type':
		data = random.choice(['simple_job', 'project'])	
	elif field_name == 'level':
		if module == ASSETS:
			data = random.choice(["level_one", "level_two", "level_three", "level_four"])
		else:
			data = str(random.randint(1,4)) #picks number from 1-4
	elif field_name == 'attributes':
		number_of_items = random.randint(1, 10)
		data = get_assets(test_data_file, number_of_items, instance)
	elif field_name == 'lines':
		number_of_items = random.randint(1, 1)
		data = get_lines(test_data_file, number_of_items, module, instance)
	elif field_name == "job_title":		
		data_df = pd.read_csv(test_data_file)
		data = get_random_data('JOB_TITLE', data_df, instance)
	elif field_name == "status":
		if module == ASSETS:
			data = "pass"
	elif (field_name == "external_id") and (UPSERT in action) and (field_value == None):
		data = str(uuid.uuid4()) #generates random UUID
	elif field_name == 'name':
		if module == CUSTOMERS:
			data = get_name(field_name.upper(), test_data_file, instance)
			if 'company' in d:
				if 'name' in d:
					d['name'] = d['company']
		elif module in [TAX_CODES, ACCOUNT_CODES]:
			header = module.split("_")[1]
			data = get_tax_code_name(header, test_data_file, instance)
	elif field_name == 'code':
		if 'name' in d:
			tax_code_name = d['name'].split(" ")
			data = ""
			for initial in tax_code_name:
				abbrev = initial[0]
				if abbrev.isalpha() and abbrev.isupper(): 
					data += abbrev
			data += str(rand_num(6,'padded','d')) #picks number between 100000-999999
	elif field_name == 'rate':
		data = str(rand_num(2,'!padded','d')) #picks number between 1-99
	return data