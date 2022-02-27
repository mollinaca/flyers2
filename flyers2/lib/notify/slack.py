import json
import requests
import time
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError

"""
https://github.com/slackapi/python-slack-sdk
"""


def post_message(slack_bot_token: str, slack_channel: str, message: str):
    client = WebClient(token=slack_bot_token)

    try:
        response = client.chat_postMessage(channel=slack_channel, text=message)
        # assert response["message"]["text"] == message
        return response
    except SlackApiError as e:
        # You will get a SlackApiError if "ok" is False
        assert e.response["ok"] is False
        assert e.response["error"]  # str like 'invalid_auth', 'channel_not_found'
        return e.response


def file_upload(slack_bot_token: str, slack_channel: str, filepath: str, comment: str):
    client = WebClient(token=slack_bot_token)
    response = client.files_upload(
        channels=slack_channel, file=filepath, initial_comment=comment
    )

    if response["ok"]:
        return response
    else:
        time.sleep(61)

    response = client.files_upload(
        channels=slack_channel, file=filepath, initial_comment=comment
    )
    return response


#    try:
#        assert response["file"]  # the uploaded file
#        return response
#    except SlackApiError as e:
#        # print(f"Got an error: {e.response['error']}")
#        # You will get a SlackApiError if "ok" is False
#        assert e.response["ok"] is False
#        assert e.response["error"]  # str like 'invalid_auth', 'channel_not_found'
#        return e.response


def auth_test(token: str):
    url = "https://slack.com/api/auth.test"
    params = {"token": token}
    r = requests.post(url, data=params)
    return r


def file_upload2(slack_bot_token: str, slack_channel: str, file: str, comment: str):
    url = "https://slack.com/api/files.upload"
    data = {
        "token": slack_bot_token,
        "channels": slack_channel,
        "initial_comment": comment,
    }
    fileData = open(file, "rb").read()
    files = {"file": fileData}
    r = requests.post(url, data=data, files=files)

    if r.status_code == requests.codes.ok:
        return json.loads(r.text)
    elif r.status_code == 408:
        ret = json.loads({"ok": False, "body": r.text})
        return ret

    time.sleep(61)
    if r.status_code == requests.codes.ok:
        return json.loads(r.text)
    else:
        ret = json.loads({"ok": False, "body": r.text})
        return ret
