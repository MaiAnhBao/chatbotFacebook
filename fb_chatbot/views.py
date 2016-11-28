import json, requests, random, re, hashlib
from django.shortcuts import render
from django.views import generic
from django.http.response import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.template import Context, loader
from .config import configParams
# Create your views here.

cfg = configParams()

PAGE_ACCESS_TOKEN = "EAAMYeSx5DKEBAMhFtXDqSYiGYxxu3ifz6y2gsOgyURgJo23ZCOLZBagXjZBq9ZACWYwoQhJ4KXIZCLZA2mdD5ZClwVBchR2aveN8Nbhk7TYQCtYOuoBe3IgzeWmP8melmOEvzDPPqj8QNy4ZAmzZAhPcLW7z64zOr09Na2VbH3bmsvgZDZD"
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
	
def post_facebook_message(fbid, received_message):
#	user_details_url = "https://graph.facebook.com/v2.6/%s"%fbid
#	user_details_params = {'fields':'first_name,last_name,profile_pic', 'access_token':PAGE_ACCESS_TOKEN}
#	user_details = requests.get(user_details_url,user_details_params).json()
	post_message_url = 'https://graph.facebook.com/v2.6/me/messages?access_token=%s'%PAGE_ACCESS_TOKEN 
	response_msg = json.dumps({"recipient":{"id":fbid},"message":{"text":received_message}})
	status = requests.post(post_message_url, headers = {"Content-Type": "application/json"},data=response_msg)
	print(status.json())

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
				if 'message' in message:
					print("============= Process ========")
					print(message)
					try:
						receivedMsg = message['message']
					except ValueError as e:
						print("Decode error")
					print("sender: ", message['sender']['id'])
					print("msg: ", message['message']['text'])
					post_facebook_message(message['sender']['id'],message['message']['text'])
		return HttpResponse()
