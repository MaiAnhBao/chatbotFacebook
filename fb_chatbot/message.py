'''
Created on 29 nov. 2016

@author: hnnguyen
'''
import json

class Message:
    
    messageData = json.loads("""
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
        },
        "text" : ""
    }}""")
        
    def __init__(self,recipientId):        
        self.messageData['recipient']['id'] = recipientId
        
    def sendTypingOn(self):    
        self.messageData['sender_action'] = "typing_on"
        
    def sendTypingOff(self):
        self.messageData['sender_action'] = "typing_off"
        del self.messageData['message']
        
    def sendReadReceipt(self):
        self.messageData['sender_action'] = "mark_seen"
        del self.messageData['message']
        
    def getImageMessage(self,url):
        self.messageData['message']['attachment']['type'] = "image"
        self.messageData['message']['attachment']['payload']['url'] = url
        
    def getAudioMessage(self,url):
        self.messageData['message']['attachment']['type'] = "audio"
        self.messageData['message']['attachment']['payload']['url'] = url
        
    def getVideoMessage(self,url):
        self.messageData['message']['attachment']['type'] = "video"
        self.messageData['message']['attachment']['payload']['url'] = url    
        
    def getTextMessage(self,messageText):
        self.messageData['message']['text'] = messageText
        del self.messageData['message']['attachment']

msg = Message("111")
msg.sendTypingOff()
print(msg.messageData)
