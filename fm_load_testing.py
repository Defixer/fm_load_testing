from locust import HttpLocust, TaskSet, task
from locust.events import request_failure
import json
import random
import csv
import logging
import utilities

UPSERT = 'UPSERT'
CREATE = 'CREATE'
client_secret = "/Users/crmonlinegraph/Documents/Scripts/fm_load_testing/client_secret.json"
user_creds = "/Users/crmonlinegraph/Documents/Scripts/fm_load_testing/user_creds.csv"
RECORD_ID = 'p'
USER_CREDENTIALS = None


class FM_load_testing(TaskSet):
	def on_start(self):
		""" on_start is called when a Locust start before 
			any task is scheduled
		"""
		self.set_global_variables()
		if len(USER_CREDENTIALS) > 0:
			self.username, self.password = USER_CREDENTIALS.pop() #removes username/password from USER_CREDENTIALS list after being hatched


	def set_global_variables(self):
		global client_secret, HEADER
		with open(client_secret) as file:
			data = json.load(file)
		self.user_id = data['user_id'] #get from Manage Users > click on User > get the alphanumeric code in URL bar; also available in Local Storage of Developer Tools
		self.client_id = data['client_id'] #get from Developer Tools (F12) > Application tab > Storage > Local Storage > site instance > current_client json

	### LEADS
	# @task(1) #@task(n) where n is the ratio of how each function will run in the given swarm	
	# def fetch_leads(self):
	# 	login_creds = (self.username, self.password)
		# headers = {'Content-Type': 'application/json',
		# 		'Accept':'application/json',
		# 		'Client-Id': self.client_id
		# }	
	# 	full_result = "/leads"
	# 	filtered_result = "/leads?page=1&first_name=&last_name&company&date_follow_up&status&email_address"
	# 	logging.info("Fetch Leads | Username: {}\tPassword: {}".format(self.username, self.password))
	# 	response = self.client.get(full_result, auth=login_creds, headers=headers)	

	# @task(1)
	# def create_lead(self):
	# 	login_creds = (self.username, self.password)	
	# 	headers = {'Content-Type': 'application/json',
	# 		'Accept':'application/json',
	# 		'Client-Id': self.client_id
	# 	}	
	# 	payload = utilities.create_lead_payload(1, self.user_id, RECORD_ID, CREATE)
	# 	logging.info("Assigned to: {}\tClient-Id: {}".format(self.user_id, self.client_id))
	# 	logging.info("Create Lead | Payload: {} | Username: {}\tPassword: {}".format(payload, self.username, self.password))
	# 	response = self.client.post("/leads", auth=login_creds, headers=headers, json=payload)	
	# 	logging.info(response)

	# @task(1)
	# def upsert_leads(self):
	# 	login_creds = (self.username, self.password)	
	# 	headers = {'Content-Type': 'application/json',
	# 		'Accept':'application/json',
	# 		'Client-Id': self.client_id
	# 	}	
	# 	payload = utilities.create_lead_payload(3, self.user_id, RECORD_ID, UPSERT)
	# 	logging.info("Assigned to: {}\tClient-Id: {}".format(self.user_id, self.client_id))
	# 	logging.info("Upsert Lead | Payload: {} | Username: {}\tPassword: {}".format(payload, self.username, self.password))
	# 	response = self.client.post("/leads", auth=login_creds, headers=headers, json=payload)	
	# 	logging.info(response)		

		
class FM_User(HttpLocust): #min_wait & max_wait (in milliseconds; default 1000 if not declared); simulated user to wait before executing each task
	host = 'https://uatapi.fieldmagic.co'
	task_set = FM_load_testing
	min_wait = 5000 #minimum of n millisec before executing a task per user
	max_wait = 10000 #maximum of n millisec before executing a task per user

	def __init__(self): #fetch username/password from csv file
		super(FM_User, self).__init__()
		global USER_CREDENTIALS
		if (USER_CREDENTIALS == None):
			with open(user_creds, 'rb') as file:
				reader = csv.reader(file)
				USER_CREDENTIALS = list(reader)