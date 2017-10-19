import sys, json, requests
from flask import Flask, request, render_template
import botresponse as botResp, random, botinput as botInp


application = Flask(__name__, instance_relative_config=True, static_url_path='')
application.config.from_object('config')
application.config.from_pyfile('config.py', silent=True)  # Config for local development is found at: instance/config.py. This will overwrite configs in the previous line. The instance folder is ignored in .gitignore, so it won't be deployed to Heroku, in effect applying the production configs.

app = application


@app.route('/', methods=['GET'])
def indexPage():
	return render_template('index.html')

@app.route('/fb', methods=['GET'])
def handle_verification():
	print "Handling Verification."
	if request.args.get('hub.verify_token', '') == app.config['FAceBOOK_OWN_WEBHOOK_VERIFY_TOKEN']:
		print "Webhook verified!"
		return request.args.get('hub.challenge', '')
	else:
		print "Wrong verification token!"
		return "Wrong validation token"


@app.route('/fb', methods=['POST'])
def handle_message():
	data = request.get_json()
	print "json from fb ",data

	if data["object"] == "page":
		for entry in data["entry"]:
			for messaging_event in entry["messaging"]:
				if messaging_event.get("message"): 
					sender_id = messaging_event["sender"]["id"]        
					recipient_id = messaging_event["recipient"]["id"]  
					message_text = messaging_event["message"]["text"]  
					send_message_response(sender_id, parse_user_message(message_text)) 

	return "ok"


def send_message(sender_id, message_text):
	r = requests.post(app.config['FACEBOOK_BASE_URL']+"/me/messages",
		params={"access_token": app.config['FACEBOOK_PAGE_ACCESS_TOKEN']},
		headers={"Content-Type": "application/json"}, 
		data=json.dumps({
		"recipient": {"id": sender_id},
		"message": {"text": message_text}
	}))

def send_message_response(sender_id, message_text):
	send_message(sender_id, message_text)
	
def parse_user_message(user_text):
	if user_text in botInp.GREETING:
		return getOneOf(botResp.GREETING)
	elif user_text in botInp.BAD_WORDS:
		return getOneOf(botResp.BAD_WORDS_RESPONSES)
	

def getOneOf(arr):
    rand_idx = random.randint(0,len(arr) - 1)
    return arr[rand_idx]

if __name__ == '__main__':
	if len(sys.argv) == 2:
		app.run(port=int(sys.argv[1]))
	else:
		app.run()