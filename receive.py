import os
from slackclient import SlackClient
from flask import Flask, request, Response

app = Flask(__name__)

SLACK_WEBHOOK_SECRET = os.environ.get('SLACK_WEBHOOK_SECRET')
SLACK_TOKEN = os.environ.get('SLACK_TOKEN', None)
slack_client = SlackClient(SLACK_TOKEN)

@app.route('/slack', methods=['POST'])
def inbound():
    if request.form.get('token') == SLACK_WEBHOOK_SECRET:
        channel = request.form.get('channel_name')
        username = request.form.get('user_name')
        text = request.form.get('text')
        inbound_message = username + " in " + channel + " says: " + text
        print(inbound_message)
        if channel == 'test2':
            sc.api_call("chat.postMessage", channel="#test2", text="Hello from python!")
#            send_message(request.form.get('channel_id'), "Hello " + username + "! It worked!")
    return Response(), 200

@app.route('/', methods=['GET'])
def test():
    return Response('It works!')

if __name__ == "__main__":
    slack_client.api_call("chat.postMessage", channel="#test2", text="Hello from Python!")
    #app.run(debug=True)
