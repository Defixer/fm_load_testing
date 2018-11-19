from locust import HttpLocust, TaskSet, task
import json
import random
from locust.events import request_failure

client_secret = "/Users/crmonlinegraph/Documents/Scripts/fm_load_testing/client_secret.json"
user_creds = "/Users/crmonlinegraph/Documents/Scripts/fm_load_testing/client_secret.json"

class UserBehavior(TaskSet):
	def on_start(self):
		""" on_start is called when a Locust start before 
			any task is scheduled
		"""
		self.set_environment_variables()


	def set_environment_variables(self):
		global client_secret
		with open(client_secret) as file:
			data = json.load(file)
		self.user_id = data['user_id'] #get from Manage Users > click on User > get the alphanumeric code in URL bar; also available in Local Storage of Developer Tools
		self.client_id = data['client_id'] #get from Developer Tools (F12) > Application tab > Storage > Local Storage > site instance > current_client json

	# @task(1) #n in all @task(n) is the ratio of how each function will run in the given swarm	
	# def access_homepage(self):
	# 	headers = {'oauth-token': self.token}
	# 	self.client.get("/", headers=headers)

	# @task(1)
	# def fetch_accounts(self):
	# 	headers = {'oauth-token': self.token}
	# 	response = self.client.get("/rest/v10/Accounts", headers=headers)

	@task(1)
	def fetch_leads(self):
		login_creds = (self.auth_username, self.auth_password)
		headers = {'Content-Type': 'application/json',
					'Client-Id': self.client_id}
		full_result = "/leads"
		filtered_result = "/leads?page=1&first_name=&last_name&company&date_follow_up&status&email_address"
		response = self.client.get(full_result, auth=login_creds, headers=headers)
		# print("{}".format(response.json()))
	@task(1)
		
class WebsiteUser(HttpLocust): #min_wait & max_wait (in milliseconds; default 1000 if not declared); simulated user to wait before executing each task
	host = 'https://uatapi.fieldmagic.co'
	task_set = UserBehavior
	min_wait = 5000
	max_wait = 10000