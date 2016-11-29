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
        
    def makeTypingOnMessage(self):    
        self.messageData['sender_action'] = "typing_on"
        
    def makeTypingOffMessage(self):
        self.messageData['sender_action'] = "typing_off"
        del self.messageData['message']
        
    def makeReadReceiptMessage(self):
        self.messageData['sender_action'] = "mark_seen"
        del self.messageData['message']
        
    def makeAttachmentMessage(self,url,sendType):        
        self.messageData['message']['attachment']['type'] = sendType
        self.messageData['message']['attachment']['payload']['url'] = url            
        
    def makeTextMessage(self,messageText):
        self.messageData['message']['text'] = messageText
        del self.messageData['message']['attachment']
        
    def getMessage(self):
        return self.messageData

        
