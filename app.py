import os
from slackclient import SlackClient
from flask import Flask, request, Response
from datetime import datetime
import die_roller

app = Flask(__name__)

SLACK_WEBHOOK_SECRET = os.environ.get('SLACK_WEBHOOK_SECRET')
SLACK_TOKEN = os.environ.get('SLACK_TOKEN', None)
slack_client = SlackClient(SLACK_TOKEN)
rollerBotName = "RollerBot"
username = ""
text = ""
stringOfResults = ""

@app.route('/roll', methods=['POST'])
def inbound():
    if request.form.get('token') == SLACK_WEBHOOK_SECRET:
        channel = request.form.get('channel_name')
        username = request.form.get('user_name')
        text = request.form.get('text')
        diceResults = die_roller.rollDice(text)
        if diceResults:
            if channel == 'test2':
                sumOfResults = 0;
                stringOfResults = "@" + username + " rolling " + text + ": `"
                for i in diceResults[:-1]:
                    sumOfResults += i
                    stringOfResults += "{result} ".format(result=i)
                sumOfResults += diceResults[-1]
                if diceResults[-1] >= 0:
                    stringOfResults += "+{result}`".format(result=diceResults[-1])
                else:
                    stringOfResults += "{result}`".format(result=diceResults[-1])
#                slack_client.api_call("chat.postMessage",
#                    channel="#" + channel,
#                    text=stringOfResults,
#                    username=rollerBotName)
                stringOfResults += "\nFinal result of rolling " + text + ": `{result}`".format(result=sumOfResults)
                slack_client.api_call("chat.postMessage",
                    channel="#" + channel,
                    text=stringOfResults,
                    username=rollerBotName)
        else:
            slack_client.api_call("chat.postMessage",
                channel="#" + channel,
                text="Could not parse " + text + ".",
                username=rollerBotName)
    return Response(), 200

@app.route('/')
def homepage():
    return """
    <h1>{uname}</h1>
    <p>{results}.</p>
    
    """.format(uname = username, results=stringOfResults)

if __name__ == '__main__':
    app.run(debug=True, use_reloader=True)
