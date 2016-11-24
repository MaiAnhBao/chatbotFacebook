import json, requests, random, re
from django.shortcuts import render
from django.views import generic
from django.http.response import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.template import Context, loader
# Create your views here.

PAGE_ACCESS_TOKEN = "EAAMYeSx5DKEBAMhFtXDqSYiGYxxu3ifz6y2gsOgyURgJo23ZCOLZBagXjZBq9ZACWYwoQhJ4KXIZCLZA2mdD5ZClwVBchR2aveN8Nbhk7TYQCtYOuoBe3IgzeWmP8melmOEvzDPPqj8QNy4ZAmzZAhPcLW7z64zOr09Na2VbH3bmsvgZDZD"
VERIFY_TOKEN = "2318934571"

def index(request):
	return HttpResponse("Bonjour, le monde")

def error404(request):
	template = loader.get_template('404.html')
	context = Context({"message":"All: %s" % request,})
	return HttpResponse(content=template.render(context), content_type='text/html;charset=utf8', status=404)

def post_facebook_message(fbid, received_message):
	post_message_url = 'https://graph.facebook.com/v2.5/me/message?access_token=%s'%PAGE_ACCESS_TOKEN 
	response_msg = json.dumps({"recipient":{"id":fbid},"message":{"text":received_message}})
	status = requests.post(post_message_url, headers = {"Content-Type": "application/json"},data=response_msg)
	print(status.json())

class FbBotView(generic.View):
	def get(self, request, *args, **kwargs):
		try:
			if self.request.GET['hub.verify_token'] == VERIFY_TOKEN:
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
		for entry in incoming_message['entry']:
			for message in entry['messaging']:
				if 'message' in message:
					print(message)
					try:
						receivedMsg = message['message']
					except ValueError as e:
						print("Decode error")
					post_facebook_message(message['sender']['id'],message['message']['text'])
		return HttpResponse()
