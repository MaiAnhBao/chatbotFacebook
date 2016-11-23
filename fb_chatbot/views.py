import json, requests, random, re
from django.shortcuts import render
from django.views import generic
from django.http.response import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
# Create your views here.

PAGE_ACCESS_TOKEN = ""
VERIFY_TOKEN = ""

def post_facebook_message(fbid, received_message):
	post_message_url = 'https://graph.facebook.com/v2.6/me/message?access_token=%s'%PAGE_ACCESS_TOKEN 
	response_msg = "OK"
	status = requests.post(post_message_url, headers = {'Content-Type': 'application/json'},data=response_msg)
	print(status.json())

class FbBotView(generic.View):
	def get(self, request, *args, **kwargs):
		if self.request.GET['hub.verify_token'] == VERIFY_TOKEN:
			return HttpResponse(self.request.GET['hub.challenge'])
		else:
			return HttpResponse("Bonjour, erreur jeton invalide")
	@method_decorator(csrf_exempt)
	def dispatch(self, request, *args, **kwargs):
		return generic.View.dispatch(self,request,*args,**kwargs)

	def post(self,request,*args,**kwargs):
		incoming_message = json.loads(self.request.body.decode('utf-8'))
		for entry in incoming_message['entry']:
			for message in entry['messaging']:
				if 'message' in message:
					print(message)
					post_facebook_message(message['sender']['id'],message['message']['text'])
		return HttpResponse()
