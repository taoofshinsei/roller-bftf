import os
from slackclient import SlackClient
from flask import Flask, request, Response
from datetime import datetime

app = Flask(__name__)

SLACK_WEBHOOK_SECRET = os.environ.get('SLACK_WEBHOOK_SECRET')
SLACK_TOKEN = os.environ.get('SLACK_TOKEN', None)
slack_client = SlackClient(SLACK_TOKEN)

#@app.route('/roll', methods=['POST'])
#def inbound():
#    if request.form.get('token') == SLACK_WEBHOOK_SECRET:
#        channel = request.form.get('channel_name')
#        username = request.form.get('user_name')
#        text = request.form.get('text')
#        inbound_message = username + " in " + channel + " says: " + text
#        print(inbound_message)
#        if channel == 'test2':
#            slack_client.api_call("chat.postMessage", channel="#test2", text="Hello from python!")
#            send_message(request.form.get('channel_id'), "Hello " + username + "! It worked!")
#    else:
#        slack_client.api_call("chat.postMessage", channel="#test2", text="Somethin' done gone wrong!")
#    return Response(), 200

@app.route('/')
def homepage():
    the_time = datetime.now().strftime("%A, %d %b %Y %l:%M %p")
    
    return """
    <h1>Hello heroku</h1>
    <p>It is currently {time}.</p>
    
    """.format(time=the_time)

if __name__ == "__main__":
    app.run(debug=True, use_reloader=True)
