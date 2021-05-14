import email
import smtplib
from datetime import datetime
import requests
import schedule
import time

def send_email():
	def create_session_info(center, session):
		return {"name": center["name"],
				"date": session["date"],
				"capacity": session["available_capacity"],
				"pincode": center["pincode"],
				"age_limit": session["min_age_limit"]}
	
	def get_sessions(data):
		for center in data["centers"]:
			for session in center["sessions"]:
					yield create_session_info(center, session)
				
	def is_available(session):
		return session["capacity"] > 0
	
	def is_eighteen_plus(session):
		return session["age_limit"] == 18
	
	def get_for_seven_days(start_date):
		url = "https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/calendarByDistrict"
		params = {"district_id": 770, "date": start_date.strftime("%d-%m-%Y")}
		headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0"}
		resp = requests.get(url, params=params, headers=headers)
		data = resp.json()
		return [session for session in get_sessions(data) if is_eighteen_plus(session) and is_available(session)]
	
	def create_output(session_info):
		return f"Pincode: {session_info['pincode']}\nOn date: {session_info['date']} - {session_info['name']} has a capacity of ({session_info['capacity']}) slots available."
	
	print(get_for_seven_days(datetime.today()))
	content = "\n\n".join([create_output(session_info) for session_info in get_for_seven_days(datetime.today())])
	username = ""
	password = ""
	
	if not content:
		print("No availability")
	else:
		email_msg = email.message.EmailMessage()
		email_msg["Subject"] = "Vaccine Slots Available!!"
		email_msg["From"] = "aryan.sce19@sot.pdpu.ac.in"
		email_msg["To"] = "aryan.sce19@sot.pdpu.ac.in"
		email_msg.set_content("District: Ahmedabad Corporation\n\n"+content)
		
		with smtplib.SMTP(host='smtp.gmail.com', port='587') as server:
			server.starttls()
			server.login("aryan.sce19@sot.pdpu.ac.in", "Abc123&#")
			server.send_message(email_msg, "aryan.sce19@sot.pdpu.ac.in","aryan.sce19@sot.pdpu.ac.in")
			


schedule.every(0.2).minutes.do(send_email)

while True:
		# Checks whether a scheduled task 
		# is pending to run or not
		schedule.run_pending()
		time.sleep(1)
	