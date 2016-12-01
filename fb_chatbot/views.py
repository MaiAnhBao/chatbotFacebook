import json, requests, random, re
from django.shortcuts import render
from django.views import generic
from django.http.response import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.template import Context, loader
from .config import configParams
from .message import Message
from .models import MessageDB
# Create your views here.

cfg = configParams()

PAGE_ACCESS_TOKEN = cfg.PAGE_ACCESS_TOKEN
VERIFY_TOKEN = cfg.VALIDATION_TOKEN

def index(request):
	return HttpResponse("Bonjour, le monde")

def error404(request):
	template = loader.get_template('404.html')
	context = Context({"message":"All: %s" % request,})
	return HttpResponse(content=template.render(context), content_type='text/html;charset=utf8', status=404)

def post_facebook_message(send_message):
	print("Message send: ", send_message)
	post_message_url = 'https://graph.facebook.com/v2.6/me/messages?access_token=%s'%PAGE_ACCESS_TOKEN	
#	response_msg = json.dumps({"recipient":{"id":fbid},"message":{"text":received_message}})
# 	print("Send message: ",response_msg)
	try:
		r = requests.post(post_message_url, headers = {"Content-Type": "application/json"},data=send_message)
		print(r.json())
		err = r.raise_for_status()
	except requests.exceptions.Timeout:
		print("Timeout")
	except requests.exceptions.TooManyRedirects:
		print("Too many redirects")
	except requests.exceptions.HTTPError as e:
		print("Http Error Exception")
		print(e)
	except requests.exceptions.RequestException as e:
		print("What is an error?")
		print(e)
	if not err and r.status_code == 200:
		print(r.json())
		
class FbBotView(generic.View):
	def get(self, request, *args, **kwargs):
		try:
			if self.request.GET['hub.mode'] == 'subscribe' and self.request.GET['hub.verify_token'] == VERIFY_TOKEN:
				return HttpResponse(self.request.GET['hub.challenge'])
			else:
				return HttpResponse("Bonjour, erreur jeton invalide")
		except Exception as e:
			print(e)
			return HttpResponse("<p align=center style='font-size:20px'>Cannot get the value token</p>")
	@method_decorator(csrf_exempt)
	def dispatch(self, request, *args, **kwargs):
		return generic.View.dispatch(self,request,*args,**kwargs)

	def post(self,request,*args,**kwargs):
		incoming_message = json.loads(self.request.body.decode('utf-8'))
		print("incoming message", incoming_message)		
		for entry in incoming_message['entry']:
			if 'message' not in entry['messaging']:
				sender_user_id = entry['messaging']['sender']['id']
				print("Blah Blah")
				sendTextMessage(sender_user_id, "blah blah")
			for message in entry['messaging']:
				receivedMsg = message['message']['text']
				sender_user_id = message['sender']['id']
				print("============> Message received: ",receivedMsg)
				print("============> who send?",sender_user_id)
# 				print("recipient ", message['recipient']['id'])
				if receivedMsg:
					if 'hello ' in receivedMsg or 'hi ' in receivedMsg:
						sendGreetingMessage(sender_user_id)
					elif 'image' in receivedMsg:						
# 						response_msg.makeAttachmentMessage('http://google.com','image')
						sendAttachmentMessage(sender_user_id, 'image')
					elif 'typing on' in receivedMsg:
						sendTypingMessage(sender_user_id,"typing_on")
					else:
						sendTextMessage(sender_user_id, "How do you turn this on? Robinhood? lumberjack")
		return HttpResponse()


def sendGreetingMessage(userId):
	print("Send Greeting Message function")
	greeting_lst = ['Hello', 'Hi', 'Hola']
	
# 	user_details_url = "https://graph.facebook.com/v2.6/%s"%userId
# 	user_details_params = {'fields':'first_name,last_name,profile_pic', 'access_token':PAGE_ACCESS_TOKEN}
# 	user_details = requests.get(user_details_url,user_details_params).json()
# 	print(json.dump(user_details))
# 	name = user_details['first_name']
	
	response_msg_text = greeting_lst[random.randint(len(greeting_lst))]
	response_msg = Message(userId)
	response_msg.makeTextMessage(response_msg_text)
	response_msg_text = response_msg.getMessage()
	print(response_msg_text)
	post_facebook_message(response_msg_text)

def sendAttachmentMessage(userId, type_msg):
	print("Send Attachment Message function")
	print("Send from id %s with type '%s'"%(userId, type_msg))
	response_msg = json.loads("""
    {
    "recipient": {
        "id": ""
        },
    "message": {
    	"attachment": {
            "type": "",
            "payload": {
                "url": ""
            }
        }        
    }}""")
	response_msg['recipient']['id'] = userId
	response_msg['message']['attachment']['type'] = type_msg
	response_msg['message']['attachment']['payload']['url'] = "http://google.com"
	
	print(response_msg)
	post_facebook_message(json.dumps(response_msg))
	
def sendTypingMessage(userId,state):
	print("Send Typing Message function")
	print("Send from id %s with typing on"%(userId))
	response_msg = json.loads("""
    {
    "recipient": {
        "id": ""
        },
    "sender_action": ""
        }       
    }""")
	response_msg['recipient']['id'] = userId
	response_msg['sender_action'] = state
	
	print(response_msg)
	post_facebook_message(json.dumps(response_msg))
	
def sendTextMessage(userId, msg):
	print("Send Text Message function")
	print("Send from id %s with message '%s'"%(userId, msg))
	response_msg = json.loads("""
    {
    "recipient": {
        "id": ""
        },
    "message": {
        "text" : ""
    }}""")
	response_msg['recipient']['id'] = userId
	response_msg['message']['text'] = msg	
	post_facebook_message(json.dumps(response_msg))