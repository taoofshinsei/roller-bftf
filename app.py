import os
from slackclient import SlackClient
from flask import Flask, request, Response
from die_roller import Roll

app = Flask(__name__)

SLACK_WEBHOOK_SECRET = os.environ.get('SLACK_WEBHOOK_SECRET')
SLACK_TOKEN = os.environ.get('SLACK_TOKEN', None)
slack_client = SlackClient(SLACK_TOKEN)
rollerBotName = "RollerBot"
msg = ""
username = ""

@app.route('/roll', methods=['POST'])
def inbound():
    if request.form.get('token') == SLACK_WEBHOOK_SECRET:
        channel = request.form.get('channel_name', '')
        username = request.form.get('user_name', '')
        text = request.form.get('text', '')
        if text == "help":
            msg = """/roll generates a random dice roll result with arbitrary modifiers.\n`/roll <name> <dice>... <modifiers>...`\n>*name:* String name of the roll i.e. `attack`, `damage`, `perception`\n>*dice:* A list of space or comma seperated dice to roll i.e. `2d10,5d4`\n>*modifiers:* A list of modifiers i.e. `+3-4`, `+3 -4`, `+3,-4`"""
        else:
            try:
                roller = Roll(text)
                mod = "`{}{}`".format("+" if roller.mod > 0 else "", roller.mod)
                dice = ["*{}d{}:* `{}`".format(c, d, " ".join(list(map(str,v)))) for c,d,v in roller.results]
                msg =  "@{} rolls {} {}\n".format(username, " and ".join(dice), mod if roller.mod else '')
                msg += ">{}".format(roller)
            except ValueError as exp:
                msg = str(exp)
            
        slack_client.api_call("chat.postMessage", channel="#" + channel,
                              text=msg, username=rollerBotName)
        return Response(), 200
    return Response(), 401

@app.route('/')
def homepage():
    return """
    <h1>{uname}</h1>
    <p>{results}.</p>
    
    """.format(uname = username, results=msg)

if __name__ == '__main__':
    app.run(debug=True, use_reloader=True)
