from fbchat import Client
from fbchat.models import *
import openai
import time

# Facebook Login
username = ''
password = ''
# conversation thread id
target_id = 100016831968558
my_uid = 100002469114451
# Load the GPT-3 model
openai.api_key = ''
model_engine = "text-davinci-002"
manual_mode = False

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
        global manual_mode
        global my_uid
        global target_id
        self.markAsDelivered(thread_id, message_object.uid)
        self.markAsRead(thread_id)
        query = message_object.text.strip()
        # return the current mode of the bot
        if "!mode" in query and author_id != self.uid:
            if manual_mode:
                current_mode = "Current Mode = Manual"
            else:
                current_mode = "Current Mode = Auto"
            self.send(Message(text=current_mode), thread_id=my_uid, thread_type=thread_type)

        # if we are not in manual mode
        elif not manual_mode and author_id != self.uid:
            # switch to manual mode
            if "!manual" in query:
                manual_mode = True
                print("Switched to Manual Mode...")
                self.send(Message(text="Operating in Manual Mode"), thread_id=my_uid, thread_type=thread_type)

            # if the query is valid
            elif len(query.split()) > 2:
                self.reactToMessage(message_object.uid, MessageReaction.YES)
                time.sleep(.3)
                print(f'QUERY-> {query}\n')
                GPT_response = self.generate_text(query).replace("?","")
                print(f'RESPONSE:{GPT_response}\n--------------------------------------------')
                self.send(Message(text=GPT_response), thread_id=target_id, thread_type=thread_type)
                exchange = f'COPY\nQuery:\n{query}\nResponse{GPT_response}'
                self.send(Message(text=exchange), thread_id=my_uid, thread_type=thread_type)

            # if the query is invalid
            elif len(query.split()) < 2:
                self.reactToMessage(message_object.uid, MessageReaction.NO)
                print(f'INVALID QUERY-> {query}\n')
                time.sleep(.3)
                base_response = "Sorry, I don't know how to answer that.\nPlease ask me a question."
                print(f'RESPONSE:\n{base_response}\n--------------------------------------------')
                self.send(Message(text=base_response), thread_id=thread_id, thread_type=thread_type)
                exchange = f'Query:\n{query}\nResponse Failed'
                self.send(Message(text=exchange), thread_id=my_uid, thread_type=thread_type)

        # if the bot is in manual mode
        elif manual_mode and author_id != self.uid:
            # switch off manual mode
            if "!auto" in query:
                manual_mode = False
                print("Switched to Auto Mode...")
                self.send(Message(text="Operating in Auto Mode"), thread_id=my_uid, thread_type=thread_type)

            # if the author is the target
            elif author_id == str(target_id):
                target_message = f'From Target->\n{query}'
                print(target_message)
                self.send(Message(text=target_message), thread_id=my_uid, thread_type=thread_type)

            # if the author is myself
            elif author_id == str(my_uid):
                print(f'Custom:\n{query}')
                self.send(Message(text=query), thread_id=target_id, thread_type=thread_type)

print(f'BOT STARTED \n--------------------------------------')
# create chat client
client = GPTBot(username, password, logging_level=40)
client.listen()
