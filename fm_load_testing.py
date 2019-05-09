from locust import HttpLocust, TaskSet, task
from locust.events import request_failure
import json
import random
import csv
import utilities
from constants import FETCH, CREATE, UPDATE, UPSERT, UPSERT_INSERT, UPSERT_UPDATE, SEARCH, REQUEST, RESPONSE, FM_DN
from constants import LEADS, CUSTOMERS, SITES, CONTACTS, OPPORTUNITIES, JOBS, ASSETS, CUSTOMER_INVOICES, PURCHASE_ORDERS, SUPPLIER_INVOICES, EVENTS, TASKS, NOTES, TAX_CODES, ACCOUNT_CODES
from utilities import prettify
import pandas as pd
import time

client_secret = "client_secret.json"
user_creds = "user_creds.csv"
logfile = "locustfile.log"
fm_data = "fm_data.csv"
USER_CREDENTIALS = None

class FM_load_testing(TaskSet):
	log = utilities.get_logger(logfile)

	def on_start(self):
		""" on_start is called when a Locust start before 
			any task is scheduled
		"""
		self.set_global_variables()
		# if len(USER_CREDENTIALS) > 0:
		# 	self.username, self.password = USER_CREDENTIALS.pop() #removes username/password from USER_CREDENTIALS list after being hatched		
		# 	self.log.info("Created: {} | {}".format(self.username, self.password))


	def set_global_variables(self):
		global client_secret
		with open(client_secret) as file:
			data = json.load(file)
		self.user_id = data['user_id'] #get from Manage Users > click on User > get the alphanumeric code in URL bar; also available in Local Storage of Developer Tools
		self.client_id = data['client_id'] #get from API Keys > client_id
		self.username = data['username']
		self.password = data['password']

	# FETCH
	@task(1) #@task(n) where n is the ratio of how each function will run in the given swarm	
	def fetch_leads(self):
		try :			
			data = utilities.fetch(LEADS, FETCH, self)
			utilities.log_req_res(data, self)
		except:
			utilities.get_error_message(self)
			
	@task(1)	
	def fetch_customers(self):
		try :			
			data = utilities.fetch(CUSTOMERS, FETCH, self)
			utilities.log_req_res(data, self)
		except:
			utilities.get_error_message(self)
	
	@task(1)	
	def fetch_sites(self):
		try :			
			data = utilities.fetch(SITES, FETCH, self)
			utilities.log_req_res(data, self)
		except:
			utilities.get_error_message(self)

	@task(1)	
	def fetch_contacts(self):
		try :			
			data = utilities.fetch(CONTACTS, FETCH, self)
			utilities.log_req_res(data, self)
		except:
			utilities.get_error_message(self)

	@task(1)	
	def fetch_opportunities(self):
		try :			
			data = utilities.fetch(OPPORTUNITIES, FETCH, self)
			utilities.log_req_res(data, self)
		except:
			utilities.get_error_message(self)

	@task(1)	
	def fetch_jobs(self):
		try :			
			data = utilities.fetch(JOBS, FETCH, self)
			utilities.log_req_res(data, self)
		except:
			utilities.get_error_message(self)

	@task(1)	
	def fetch_assets(self):
		try :			
			data = utilities.fetch(ASSETS, FETCH, self)
			utilities.log_req_res(data, self)
		except:
			utilities.get_error_message(self)

	@task(1)	
	def fetch_customer_invoices(self):
		try :			
			data = utilities.fetch(CUSTOMER_INVOICES, FETCH, self)
			utilities.log_req_res(data, self)
		except:
			utilities.get_error_message(self)

	@task(1)	
	def fetch_purchase_orders(self):
		try :			
			data = utilities.fetch(PURCHASE_ORDERS, FETCH, self)
			utilities.log_req_res(data, self)
		except:
			utilities.get_error_message(self)

	@task(1)	
	def fetch_supplier_invoices(self):
		try :			
			data = utilities.fetch(SUPPLIER_INVOICES, FETCH, self)
			utilities.log_req_res(data, self)
		except:
			utilities.get_error_message(self)

	@task(1)
	def fetch_tax_codes(self):
		try :			
			data = utilities.fetch(TAX_CODES, FETCH, self)
			utilities.log_req_res(data, self)
		except:
			utilities.get_error_message(self)

	@task(1)
	def fetch_account_codes(self):
		try:
			data = utilities.fetch(ACCOUNT_CODES, FETCH, self)
			utilities.log_req_res(data, self)
		except:
			utilities.get_error_message(self)

	# CREATE	
	@task(1) #@task(n) where n is the ratio of how each function will run in the given swarm	
	def create_leads(self):
		try :			
			data = utilities.create(LEADS, CREATE, self)
			utilities.log_req_res(data, self)
		except:
			utilities.get_error_message(self)
			
	@task(1)	
	def create_customers(self):
		try :			
			data = utilities.create(CUSTOMERS, CREATE, self)
			utilities.log_req_res(data, self)
		except:
			utilities.get_error_message(self)
	
	@task(1)	
	def create_sites(self):
		try :			
			data = utilities.create(SITES, CREATE, self)
			utilities.log_req_res(data, self)
		except:
			utilities.get_error_message(self)

	@task(1)	
	def create_contacts(self):
		try :			
			data = utilities.create(CONTACTS, CREATE, self)
			utilities.log_req_res(data, self)
		except:
			utilities.get_error_message(self)

	@task(1)	
	def create_opportunities(self):
		try :			
			data = utilities.create(OPPORTUNITIES, CREATE, self)
			utilities.log_req_res(data, self)
		except:
			utilities.get_error_message(self)

	@task(1)	
	def create_jobs(self):
		try :			
			data = utilities.create(JOBS, CREATE, self)
			utilities.log_req_res(data, self)
		except:
			utilities.get_error_message(self)

	@task(1)	
	def create_assets(self):
		try :			
			data = utilities.create(ASSETS, CREATE, self)
			utilities.log_req_res(data, self)
		except:
			utilities.get_error_message(self)

	@task(1)	
	def create_customer_invoices(self):
		try :			
			data = utilities.create(CUSTOMER_INVOICES, CREATE, self)
			utilities.log_req_res(data, self)
		except:
			utilities.get_error_message(self)

	@task(1)	
	def create_purchase_orders(self):
		try :			
			data = utilities.create(PURCHASE_ORDERS, CREATE, self)
			utilities.log_req_res(data, self)
		except:
			utilities.get_error_message(self)

	@task(1)	
	def create_supplier_invoices(self):
		try :			
			data = utilities.create(SUPPLIER_INVOICES, CREATE, self)
			utilities.log_req_res(data, self)
		except:
			utilities.get_error_message(self)

	@task(1)	
	def create_tax_codes(self):
		try :			
			data = utilities.create(TAX_CODES, CREATE, self)
			utilities.log_req_res(data, self)
		except:
			utilities.get_error_message(self)

	@task(1)	
	def create_account_codes(self):
		try :			
			data = utilities.create(ACCOUNT_CODES, CREATE, self)
			utilities.log_req_res(data, self)
		except:
			utilities.get_error_message(self)

	# UPDATE
	@task(1)	
	def update_leads(self):
		try :			
			data = utilities.update(LEADS, UPDATE, self)
			utilities.log_req_res(data, self)
		except:
			utilities.get_error_message(self)
			
	@task(1)	
	def update_customers(self):
		try :			
			data = utilities.update(CUSTOMERS, UPDATE, self)
			utilities.log_req_res(data, self)
		except:
			utilities.get_error_message(self)
	
	@task(1)	
	def update_sites(self):
		try :			
			data = utilities.update(SITES, UPDATE, self)
			utilities.log_req_res(data, self)
		except:
			utilities.get_error_message(self)

	@task(1)	
	def update_contacts(self):
		try :			
			data = utilities.update(CONTACTS, UPDATE, self)
			utilities.log_req_res(data, self)
		except:
			utilities.get_error_message(self)

	@task(1)	
	def update_opportunities(self):
		try :			
			data = utilities.update(OPPORTUNITIES, UPDATE, self)
			utilities.log_req_res(data, self)
		except:
			utilities.get_error_message(self)

	@task(1)	
	def update_jobs(self):
		try :			
			data = utilities.update(JOBS, UPDATE, self)
			utilities.log_req_res(data, self)
		except:
			utilities.get_error_message(self)

	@task(1)	
	def update_assets(self):
		try :			
			data = utilities.update(ASSETS, UPDATE, self)
			utilities.log_req_res(data, self)
		except:
			utilities.get_error_message(self)

	@task(1)	
	def update_customer_invoices(self):
		try :			
			data = utilities.update(CUSTOMER_INVOICES, UPDATE, self)
			utilities.log_req_res(data, self)
		except:
			utilities.get_error_message(self)

	@task(1)	
	def update_purchase_orders(self):
		try :			
			data = utilities.update(PURCHASE_ORDERS, UPDATE, self)
			utilities.log_req_res(data, self)
		except:
			utilities.get_error_message(self)

	@task(1)	
	def update_supplier_invoices(self):
		try :			
			data = utilities.update(SUPPLIER_INVOICES, UPDATE, self)
			utilities.log_req_res(data, self)
		except:
			utilities.get_error_message(self)

	@task(1)	
	def update_tax_codes(self):
		try :			
			data = utilities.update(TAX_CODES, UPDATE, self)
			utilities.log_req_res(data, self)
		except:
			utilities.get_error_message(self)

	@task(1)	
	def update_account_codes(self):
		try :			
			data = utilities.update(ACCOUNT_CODES, UPDATE, self)
			utilities.log_req_res(data, self)
		except:
			utilities.get_error_message(self)
	
	# SEARCH
	@task(1)	
	def search_leads(self):
		try :			
			data = utilities.search(LEADS, SEARCH, self)
			utilities.log_req_res(data, self)
		except:
			utilities.get_error_message(self)
			
	@task(1)	
	def search_customers(self):
		try :			
			data = utilities.search(CUSTOMERS, SEARCH, self)
			utilities.log_req_res(data, self)
		except:
			utilities.get_error_message(self)
	
	@task(1)	
	def search_sites(self):
		try :			
			data = utilities.search(SITES, SEARCH, self)
			utilities.log_req_res(data, self)
		except:
			utilities.get_error_message(self)

	@task(1)	
	def search_contacts(self):
		try :			
			data = utilities.search(CONTACTS, SEARCH, self)
			utilities.log_req_res(data, self)
		except:
			utilities.get_error_message(self)

	@task(1)	
	def search_opportunities(self):
		try :			
			data = utilities.search(OPPORTUNITIES, SEARCH, self)
			utilities.log_req_res(data, self)
		except:
			utilities.get_error_message(self)

	@task(1)	
	def search_jobs(self):
		try :			
			data = utilities.search(JOBS, SEARCH, self)
			utilities.log_req_res(data, self)
		except:
			utilities.get_error_message(self)

	@task(1)	
	def search_assets(self):
		try :			
			data = utilities.search(ASSETS, SEARCH, self)
			utilities.log_req_res(data, self)
		except:
			utilities.get_error_message(self)

	@task(1)	
	def search_customer_invoices(self):
		try :			
			data = utilities.search(CUSTOMER_INVOICES, SEARCH, self)
			utilities.log_req_res(data, self)
		except:
			utilities.get_error_message(self)

	@task(1)	
	def search_purchase_orders(self):
		try :			
			data = utilities.search(PURCHASE_ORDERS, SEARCH, self)
			utilities.log_req_res(data, self)
		except:
			utilities.get_error_message(self)

	@task(1)	
	def search_supplier_invoices(self):
		try :			
			data = utilities.search(SUPPLIER_INVOICES, SEARCH, self)
			utilities.log_req_res(data, self)
		except:
			utilities.get_error_message(self)

	@task(1)	
	def search_tax_codes(self):
		try :			
			data = utilities.search(TAX_CODES, SEARCH, self)
			utilities.log_req_res(data, self)
		except:
			utilities.get_error_message(self)

	@task(1)	
	def search_account_codes(self):
		try :			
			data = utilities.search(ACCOUNT_CODES, SEARCH, self)
			utilities.log_req_res(data, self)
		except:
			utilities.get_error_message(self)

	# # UPSERT
	# @task(1)
	# def upsert_lead(self):
	# 	try :			
	# 		data = utilities.upsert(LEADS, UPSERT, self)
	# 		utilities.log_req_res(data, self)
	# 	except:
	# 		utilities.get_error_message(self)
			
	# @task(1)	
	# def upsert_customers(self):
	# 	try :			
	# 		data = utilities.upsert(CUSTOMERS, UPSERT, self)
	# 		utilities.log_req_res(data, self)
	# 	except:
	# 		utilities.get_error_message(self)
	
	# @task(1)	
	# def upsert_sites(self):
	# 	try :			
	# 		data = utilities.upsert(SITES, UPSERT, self)
	# 		utilities.log_req_res(data, self)
	# 	except:
	# 		utilities.get_error_message(self)

	# @task(1)	
	# def upsert_contacts(self):
	# 	try :			
	# 		data = utilities.upsert(CONTACTS, UPSERT, self)
	# 		utilities.log_req_res(data, self)
	# 	except:
	# 		utilities.get_error_message(self)

	# @task(1)	
	# def upsert_opportunities(self):
	# 	try :			
	# 		data = utilities.upsert(OPPORTUNITIES, UPSERT, self)
	# 		utilities.log_req_res(data, self)
	# 	except:
	# 		utilities.get_error_message(self)

	# @task(1)	
	# def upsert_jobs(self):
	# 	try :			
	# 		data = utilities.upsert(JOBS, UPSERT, self)
	# 		utilities.log_req_res(data, self)
	# 	except:
	# 		utilities.get_error_message(self)

	# @task(1)	
	# def upsert_assets(self):
	# 	try :			
	# 		data = utilities.upsert(ASSETS, UPSERT, self)
	# 		utilities.log_req_res(data, self)
	# 	except:
	# 		utilities.get_error_message(self)

	# @task(1)	
	# def upsert_customer_invoices(self):
	# 	try :			
	# 		data = utilities.upsert(CUSTOMER_INVOICES, UPSERT, self)
	# 		utilities.log_req_res(data, self)
	# 	except:
	# 		utilities.get_error_message(self)

	# @task(1)	
	# def upsert_purchase_orders(self):
	# 	try :			
	# 		data = utilities.upsert(PURCHASE_ORDERS, UPSERT, self)
	# 		utilities.log_req_res(data, self)
	# 	except:
	# 		utilities.get_error_message(self)

	# @task(1)	
	# def upsert_supplier_invoices(self):
	# 	try :			
	# 		data = utilities.upsert(SUPPLIER_INVOICES, UPSERT, self)
	# 		utilities.log_req_res(data, self)
	# 	except:
	# 		utilities.get_error_message(self)
		
class FM_User(HttpLocust): #min_wait & max_wait (in milliseconds; default 1000 if not declared); simulated user to wait before executing each task
	host = FM_DN
	task_set = FM_load_testing
	min_wait = 3000 #minimum of n millisec before executing a task per user
	max_wait = 5000 #maximum of n millisec before executing a task per user

	# def __init__(self): #fetch username/password from csv file
	# 	super(FM_User, self).__init__()
	# 	global USER_CREDENTIALS, log
	# 	if (USER_CREDENTIALS == None):
	# 		with open(user_creds, 'rb') as file:
	# 			reader = csv.reader(file)
	# 			USER_CREDENTIALS = list(reader)