import json, requests, random, re, hashlib
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

def post_facebook_message(received_message):
	post_message_url = 'https://graph.facebook.com/v2.6/me/messages?access_token=%s'%PAGE_ACCESS_TOKEN	
#	response_msg = json.dumps({"recipient":{"id":fbid},"message":{"text":received_message}})
# 	print("Send message: ",response_msg)
	try:
		r = requests.post(post_message_url, headers = {"Content-Type": "application/json"},data=received_message)
		err = r.raise_for_status()
	except requests.exceptions.Timeout:
		print("Timeout")
	except requests.exceptions.TooManyRedirects:
		print("Too many redirects")
	except requests.exceptions.HTTPError as e:
		print(e)
	except requests.exceptions.RequestException as e:
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
			return HttpResponse("Cannot get the value token")
	@method_decorator(csrf_exempt)
	def dispatch(self, request, *args, **kwargs):
		return generic.View.dispatch(self,request,*args,**kwargs)

	def post(self,request,*args,**kwargs):
		incoming_message = json.loads(self.request.body.decode('utf-8'))
		print("incoming message", incoming_message)		
		for entry in incoming_message['entry']:
			for message in entry['messaging']:
				receivedMsg = message['message']['text']
				sender_user_id = message['sender']['id']
# 				print("sender: ", message['sender']['id'])
# 				print("msg: ", message['message']['text'])
# 				print("recipient ", message['recipient']['id'])
				if receivedMsg:
					if 'hello' in receivedMsg or 'hi' in receivedMsg:
						sendGreetingMessage(sender_user_id)
					elif 'image' in receivedMsg:						
# 						response_msg.makeAttachmentMessage('http://google.com','image')
						sendAttachmentMessage(sender_user_id, 'image')
					elif 'typing on' in receivedMsg:
						sendTypingOnMessage(sender_user_id)
					else:
						sendTextMessage(sender_user_id, "How do you turn this on?")
		return HttpResponse()


def sendGreetingMessage(userId):
	greeting_lst = ['Hello', 'Hi', 'Hola']
	
	user_details_url = "https://graph.facebook.com/v2.6/%s"%userId
	user_details_params = {'fields':'first_name,last_name,profile_pic', 'access_token':PAGE_ACCESS_TOKEN}
	user_details = requests.get(user_details_url,user_details_params).json()
	name = user_details['first_name']
	
	response_msg_text = greeting_lst[random.randint(len(greeting_lst))]  + name
	response_msg = Message(userId)
	response_msg.makeTextMessage(response_msg_text)
	response_msg_text = response_msg.getMessage()
	post_facebook_message(response_msg_text)

def sendAttachmentMessage(userId, type_msg):
	response_msg = Message(userId)
	response_msg.makeAttachmentMessage("http://google.com",type_msg)
	response_msg_text = response_msg.getMessage()
	post_facebook_message(response_msg_text)
	
def sendTypingOnMessage(userId):
	response_msg = Message(userId)
	response_msg.makeTypingOnMessage()
	response_msg_text = response_msg.getMessage()
	post_facebook_message(response_msg_text)
	
def sendTextMessage(userId, message):
	response_msg = Message(userId)
	response_msg.makeTextMessage(message)
	response_msg_text = response_msg.getMessage()
	post_facebook_message(response_msg_text)