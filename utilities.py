from datetime import datetime, timedelta
import random, string, uuid

UPSERT = 'UPSERT'

def get_date_names():
	date_names = {}
	date_names['current_date'] = datetime.now().strftime("%Y-%m-%d")
	date_names['current_time_micro'] = datetime.now().strftime("%H:%M:%S.%f")
	date_names['current_time'] = datetime.now().strftime("%H:%M:%S")
	date_names['next_day_date'] = (datetime.strptime(date_names['current_date'], '%Y-%m-%d') + timedelta(days=1)).strftime("%Y-%m-%d")

	return date_names

def create_lead_payload(loop, user_id, RECORD_ID, flag):
	payload = []
	for i in range(loop):
		lead_request = {}
		if flag == UPSERT:
			lead_request['external_id'] = str(uuid.uuid4())

		date_names = get_date_names()
		first_name = "{}L FN_test".format(RECORD_ID)
		last_name = "_{} {}".format(date_names['current_date'],date_names['current_time_micro'])
		single_lead_request = {
			"status": "new",
			"date_follow_up": "{} {}".format(date_names['next_day_date'], date_names['current_time']),
			"first_name": first_name,
			"last_name": last_name,
			"user_id": str(user_id) #assign to
		}
		lead_request.update(single_lead_request)		
		payload.append(lead_request)
	return payload