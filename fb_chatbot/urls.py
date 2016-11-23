# fbchatbot/fb_chatbot/urls.py
from django.conf.urls import include, url, handler404
from .views import FbBotView
from . import views
urlpatterns = [
		url(r'^test/?$', FbBotView.as_view()),
		url(r'^$', views.index),
		]

handler404 = views.error404
