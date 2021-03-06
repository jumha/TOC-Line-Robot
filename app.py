import os
import sys
import bullCow

from flask import Flask, jsonify, request, abort, send_file
from dotenv import load_dotenv
from linebot import LineBotApi, WebhookParser
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage, TemplateSendMessage, ButtonsTemplate, MessageTemplateAction

from fsm import TocMachine
from utils import send_text_message, send_button_message

load_dotenv()

#machine = TocMachine()

app = Flask(__name__, static_url_path="")

game = {
    'choice': 8,
    'num': 1234
}
user_id = []
machine = []
draw_machine = TocMachine('draw')

# get channel_secret and channel_access_token from your environment variable
channel_secret = os.getenv("LINE_CHANNEL_SECRET", None)
channel_access_token = os.getenv("LINE_CHANNEL_ACCESS_TOKEN", None)
if channel_secret is None:
    print("Specify LINE_CHANNEL_SECRET as environment variable.")
    sys.exit(1)
if channel_access_token is None:
    print("Specify LINE_CHANNEL_ACCESS_TOKEN as environment variable.")
    sys.exit(1)

line_bot_api = LineBotApi(channel_access_token)
parser = WebhookParser(channel_secret)


@app.route("/callback", methods=["POST"])
def callback():
    signature = request.headers["X-Line-Signature"]
    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # parse webhook body
    try:
        events = parser.parse(body, signature)
    except InvalidSignatureError:
        abort(400)

    # if event is MessageEvent and message is TextMessage, then echo text
    for event in events:
        if not isinstance(event, MessageEvent):
            continue
        if not isinstance(event.message, TextMessage):
            continue

        line_bot_api.reply_message(
            event.reply_token, TextSendMessage(text=event.message.text)
        )

    return "OK"


@app.route("/webhook", methods=["POST"])

def webhook_handler():
    signature = request.headers["X-Line-Signature"]
    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info(f"Request body: {body}")

    # parse webhook body
    try:
        events = parser.parse(body, signature)
    except InvalidSignatureError:
        abort(400)


    # if event is MessageEvent and message is TextMessage, then echo text
    for event in events:
        userId = event.source.user_id
        print(userId)
        if not userId in user_id:
            user_id.append(userId)
            machine.append(TocMachine(userId))
        idx = user_id.index(userId)

        if not isinstance(event, MessageEvent):
            continue
        if not isinstance(event.message, TextMessage):
            continue
        if not isinstance(event.message.text, str):
            continue
        print(f"\nFSM STATE: {machine[idx].state}")
        print(f"REQUEST BODY: \n{body}")
        text = event.message.text
        if machine[idx].is_initial():
            machine[idx].num = bullCow.generateNum()
            machine[idx].choice = 8            
            
            if machine[idx].start(event):
                reply_token = event.reply_token
                send_text_message(reply_token, "????????????????????????8?????????\n????????????????????????????????????")
        elif machine[idx].is_gaming():   
            if text.lower() == "????????????":
                reply_token = event.reply_token
                send_text_message(reply_token, f"????????? {str(machine[idx].num)} \n??????????????????????????? \n ?????????????????????????????????????????????")
                machine[idx].quit()
                continue
            if not text.lower().isdigit():
                reply_token = event.reply_token
                send_text_message(reply_token, "????????????0-9?????????????????????:")
                continue
            guess = int(text)
            if not bullCow.noDuplicates(guess):
                print("Number should not have repeated digits. Try again.")
                reply_token = event.reply_token
                send_text_message(reply_token, "???????????????????????????????????????:")
                machine[idx].wrong()
                continue
            if guess < 1000 or guess > 9999:
                print("?????????????????????????????????????????????:")
                reply_token = event.reply_token
                send_text_message(reply_token, "??????????????????????????????????????????:")
                machine[idx].wrong()
                continue
            bull_cow = bullCow.numOfBullsCows(machine[idx].num,guess)
            if bull_cow[0] == 4:
                print("You guessed right!")
                reply_token = event.reply_token
                temp = TemplateSendMessage(
                            alt_text='Buttons template',
                            template=ButtonsTemplate(
                                title='????????????',
                                text=f"{bull_cow[0]} bulls, {bull_cow[1]} cows\n????????????????????????",
                                actions=[
                                    MessageTemplateAction(
                                        label='????????????',
                                        text='????????????'
                                    ),
                                    MessageTemplateAction(
                                        label='????????????',
                                        text='????????????'
                                    ),
                                ]
                            )
                        )
                
                send_button_message(reply_token, temp)
                machine[idx].correct()
                continue
            print(f"{bull_cow[0]}A{bull_cow[1]}B")
            
            machine[idx].choice -=1
            if machine[idx].choice <= 0:              
                reply_token = event.reply_token
                temp = TemplateSendMessage(
                            alt_text='Buttons template',
                            template=ButtonsTemplate(
                                title='????????????',
                                text=f"{bull_cow[0]}A{bull_cow[1]}B\n????????? {str(machine[idx].num)} \n???????????????????????????",
                                actions=[
                                    MessageTemplateAction(
                                        label='????????????',
                                        text="????????????"
                                    ),
                                    MessageTemplateAction(
                                        label='????????????',
                                        text="????????????"
                                    ),
                                ]
                            )
                        )
                send_button_message(reply_token, temp)
                machine[idx].loss()
                continue
            reply_token = event.reply_token
            send_text_message(reply_token, f"{bull_cow[0]}A{bull_cow[1]}B\n?????????{machine[idx].choice}?????????")
            machine[idx].wrong
        elif machine[idx].is_finish():
            if text.lower() == "????????????":
                machine[idx].num = bullCow.generateNum()
                machine[idx].choice = 8
                reply_token = event.reply_token
                send_text_message(reply_token, "????????????????????????8?????????\n????????????????????????????????????")
                machine[idx].restart()
            elif text.lower() == "????????????":
                reply_token = event.reply_token
                send_text_message(reply_token, "????????????\n?????????????????????????????????????????????")
                machine[idx].quit()

    return "OK"


@app.route("/show-fsm", methods=["GET"])
def show_fsm():
    draw_machine.get_graph().draw("fsm.svg", prog="dot")
    return send_file("fsm.svg", mimetype="image/svg")


if __name__ == "__main__":
    PORT = os.environ['PORT']
    app.run(host="0.0.0.0", port=PORT, debug=True)
