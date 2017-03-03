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

@app.route('/roll', methods=['POST'])
def inbound():
    if request.form.get('token') == SLACK_WEBHOOK_SECRET:
        channel = request.form.get('channel_name')
        username = request.form.get('user_name')
        text = request.form.get('text')
        diceResults = die_roller.rollDice(text)
        if channel == 'test2' and diceResults:
            sumOfResults = 0;
            stringOfResults = ""
#            for i in diceResults:
#                sumOfResults += i
#                stringOfResults += " %d".format(i)
#            stringOfResults += ": %d".format(sumOfResults)
#            slack_client.api_call("chat.postMessage",
#                channel="#test2",
#                text=stringOfResults
#                username=rollerBotName)
    return Response(), 200

@app.route('/')
def homepage():
    diceResults = die_roller.rollDice("2d20")
    the_time = datetime.now().strftime("%A, %d %b %Y %l:%M %p")
    
    return """
    <h1>Hello heroku</h1>
    <p>It is currently {time}.</p>
    
    """.format(time=diceResults)

if __name__ == '__main__':
    app.run(debug=True, use_reloader=True)
