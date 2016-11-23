# fbchatbot/fb_chatbot/urls.py
from django.conf.urls import include, url
from .views import FbBotView
urlpatterns = [
		url(r'^test/?$', FbBotView.as_view())
		]
