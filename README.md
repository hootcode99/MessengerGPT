# MessengerGPT
A Facebook Messenger interface for GPT-3.5

## What is this?
This is definitely one of my less serious projects.

My girlfriend found talking to GPT interesting, but was turned-off by needing to have a Microsoft account and be asked to login constantly. It was too much hassle for her and the mobile interface left more to be desired.

Personally, I had also happened to want to experiment with and learn more about the OpenAI Python module. I also just wanted to see if I could build a bot for Facebook Messenger. I had built bots for Twitter and Discord before, but not Facebook.
I know that businesses leverage automated chatbots on FB and thought experimenting with making one might be valuable later.

## What's inside?
### FBchat
I'm using fbchat to handle the Facebook login & GET/POST requests. Unfortunately the Python fbchat module this was built on is no longer supported. I was able to make it work, but it took some tweaking of the source for the module. But after that, it worked without issue. The module allows you to simply use a facebook account rather than getting an API key from Facebook. I made an account for the bot and used that to run the script with.

### OpenAI
This script leverages GPT-3.5 through the OpenAI Python API. One can simply make a developer account with OpenAI [here](https://platform.openai.com/) to recieve an API key. You receieve a generous amount of submission tokens for free. Since this was a toy project for my girlfriend, I figured she'd never use them up and that was the case. OpenAI API bots I've built in the past for things like Discord have run to the limit though. They will deplete quickly in a multi-user scenario, but you can pay for more. 

## A Fun Addition (for me)
My girlfriend enjoyed talking to the bot. Talking to it on Facebook made it more convenient for her and made it feel more conversational. It's always fun to see the uninitiated talk to GPT like it's a person :)

However, I wanted to have a little fun myself. So I added a 'manual response mode' that, when activated, would forward her queries to my terminal and let me read and respond. It worked...well. I tried it a few times, had a few laughs, and then of course, debriefed her (don't want to be unethical). 
