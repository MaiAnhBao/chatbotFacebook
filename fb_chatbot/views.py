import json, requests, random, re, hashlib
from django.shortcuts import render
from django.views import generic
from django.http.response import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.template import Context, loader
from .config import configParams
from .message import Message
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

def verifyRequestSignature(request, response, buf):
	signature = request.headers['x-hub-signature']

	if not signature:
		print("Couldn't validate the signature")
	else:
		elements = signature.splits('=')
		method = elements[0]
		signatureHash = elements[1]

		m = hashlib.sha1()
		m.update(APP_SECRET)
		expectedHash = m.hexdigest()
#		expectedHash = hmac.new(APP_SECRET,signatureHash,sha1).digest().encode("base64").rstrip('\n')
		if signatureHash != expectedHash:
			print("Couldn't validate the request signature")
	
def post_facebook_message(received_message):
#	user_details_url = "https://graph.facebook.com/v2.6/%s"%fbid
#	user_details_params = {'fields':'first_name,last_name,profile_pic', 'access_token':PAGE_ACCESS_TOKEN}
#	user_details = requests.get(user_details_url,user_details_params).json()
	post_message_url = 'https://graph.facebook.com/v2.6/me/messages?access_token=%s'%PAGE_ACCESS_TOKEN 
	
#	response_msg = json.dumps({"recipient":{"id":fbid},"message":{"text":received_message}})
# 	print("Send message: ",response_msg)
	status = requests.post(post_message_url, headers = {"Content-Type": "application/json"},data=received_message)
#	print(status.json())

class FbBotView(generic.View):
	def get(self, request, *args, **kwargs):
		try:
			if self.request.GET['hub.mode'] == 'subscribe' and self.request.GET['hub.verify_token'] == VERIFY_TOKEN:
				return HttpResponse(self.request.GET['hub.challenge'])
			else:
				return HttpResponse("Bonjour, erreur jeton invalide")
		except Exception as e:
			return HttpResponse("Cannot get the value token")
	@method_decorator(csrf_exempt)
	def dispatch(self, request, *args, **kwargs):
		return generic.View.dispatch(self,request,*args,**kwargs)

	def post(self,request,*args,**kwargs):
		incoming_message = json.loads(self.request.body.decode('utf-8'))
		print("incoming message", incoming_message)		
		for entry in incoming_message['entry']:
			for message in entry['messaging']:
				receivedMsg = message['message']
# 				print("sender: ", message['sender']['id'])
# 				print("msg: ", message['message']['text'])
# 				print("recipient ", message['recipient']['id'])
				response_msg = Message(message['sender']['id'])
				if receivedMsg:
					if 'image' in receivedMsg:
						response_msg.makeAttachmentMessage('http://google.com','image')
					elif 'typing on' in receivedMsg:
						response_msg.makeTypingOnMessage()
					else:
						response_msg.makeTextMessage("How do you turn this on?")
				post_facebook_message(json.dumps(response_msg.getMessage()))
		return HttpResponse()
