import re
from flask import Flask, request
from slack_sdk import WebClient
from slack_bolt import App, Say
from slack_bolt.adapter.flask import SlackRequestHandler
from slack_bolt.workflows.step import WorkflowStep
from decouple import config
from gitlab import GitLab

app = Flask(__name__)

client = WebClient(token=config('SLACK_BOT_TOKEN'))

bolt_app = App(token=config('SLACK_BOT_TOKEN'),
          signing_secret=config('SLACK_SIGNING_SECRET'))

# Actions, commands, shortcuts, options requests,
# and view submissions must always be acknowledged using the ack() function

# GL = GitLab()

def edit(ack, step, configure):
    ack()

    blocks = [

def save(ack, view, update):
    pass

def execute(step, complete, fail):
    pass

ws = WorkflowStep(
    callback_id="add_task",
    edit=edit,
    save=save,
    execute=execute,
)

bolt_app.step(ws)


@bolt_app.command("/help")
def help_command(say, ack):
    ack()
    text = {
        "blocks": [
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": "This is the help command!"
                }
            }
        ]
    }
    say(text=text)


handler = SlackRequestHandler(bolt_app)


# Flask handler to respond to slack challenge
@app.route("/rileybot/events", methods=["POST"])
def slack_events():
    """ Declaring the route where slack will post a request """
    return handler.handle(request)



# Bolt library decorator/handler
@bolt_app.message("hello rileybot")
def greetings(payload: dict, say: Say):
    """
    This checks messages for 'hello rileybot' in it
    """
    user = payload.get("user")
    say(f"Hi <@{user}>")



@bolt_app.message(re.compile("(hi|hello|hey) rileybot"))
def reply_in_thread(payload: dict):
    """ This will reply in thread instead of creating a new thread """
    response = client.chat_postMessage(channel=payload.get('channel'),
                                     thread_ts=payload.get('ts'),
                                     text=f"Hi<@{payload['user']}>")


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=True)
