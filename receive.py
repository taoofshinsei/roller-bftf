import os
from flask import Flask, request, Response

app = Flask(__name__)

SLACK_WEBHOOK_SECRET = os.environ.get('SLACK_WEBHOOK_SECRET')

def channel_info(channel_id):
    channel_info = slack_client.api_call("channels.info", channel=channel_id)
    if channel_info:
        return channel_info['channel']
    return None

@app.route('/slack', methods=['POST'])
def inbound():
    if request.form.get('token') == SLACK_WEBHOOK_SECRET:
        channel = request.form.get('channel_name')
        username = request.form.get('user_name')
        text = request.form.get('text')
        inbound_message = username + " in " + channel + " says: " + text
        print(inbound_message)
        detailed_info = channel_info(request.form.get('id'))
        if detailed_info:
            print('Latest text from ' + request.form.get('name') + ":")
            print(detailed_info['latest']['text'])
        if request.form.get('name') == 'test2':
            send_message(request.form.get('id'), "Hello " + channel['name'] + "! It worked!")
    return Response(), 200

@app.route('/', methods=['GET'])
def test():
    return Response('It works!')

if __name__ == "__main__":
    app.run(debug=True)
