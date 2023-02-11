from fbchat import Client, Message
from fbchat.models import *
import openai
import os
import time

# Facebook Login
username = 'fixeditcomputertech@gmail.com'
password = 'botpass123'
# conversation thread id
targetThread = 100002469114451 #100016831968558
# Load the GPT-3 model
openai.api_key = 'api key'
model_engine = "text-davinci-002"

class GPTBot(Client):
    # generate GPT response
    def generate_text(self, prompt):
        completions = openai.Completion.create(
            engine=model_engine,
            prompt=prompt,
            max_tokens=1024,
            n=1,
            stop=None,
            temperature=0.5,
        )
        message = completions.choices[0].text
        return message

    def onMessage(self, mid=None, author_id=None, message=None, message_object=None, thread_id=None,
                        thread_type=ThreadType.USER, ts=None, metadata=None, msg=None):
        self.markAsDelivered(thread_id, message_object.uid)
        self.markAsRead(thread_id)
        query = message_object.text.strip()

        if author_id != self.uid and len(query.split()) > 3:
            self.reactToMessage(message_object.uid, MessageReaction.YES)
            time.sleep(.3)
            print(f'QUERY-> {query}\n')
            GPT_response = self.generate_text(query).replace("?","")
            print(f'RESPONSE:{GPT_response}\n--------------------------------------------')
            self.send(Message(text=GPT_response), thread_id=targetThread, thread_type=thread_type)

        elif author_id != self.uid:
            self.reactToMessage(message_object.uid, MessageReaction.NO)
            print(f'INVALID QUERY-> {query}\n')
            time.sleep(.3)
            base_response = "Sorry, I don't know how to answer that.\nPlease ask me a question."
            print(f'RESPONSE:\n{base_response}\n--------------------------------------------')
            self.send(Message(text=base_response), thread_id=targetThread, thread_type=thread_type)

print(f'BOT STARTED \n'
      f'Targeting Thread: {targetThread}\n--------------------------------------')
# create chat client
client = GPTBot(username, password, logging_level=40)
client.listen()
