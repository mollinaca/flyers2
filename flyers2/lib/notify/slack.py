from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError

"""
https://github.com/slackapi/python-slack-sdk
"""


def post_message(slack_bot_token: str, slack_channel: str, message: str):
    client = WebClient(token=slack_bot_token)

    try:
        response = client.chat_postMessage(channel=slack_channel, text=message)
        print(response)
        # assert response["message"]["text"] == message
        return response
    except SlackApiError as e:
        # You will get a SlackApiError if "ok" is False
        assert e.response["ok"] is False
        assert e.response["error"]  # str like 'invalid_auth', 'channel_not_found'
        # print(f"Got an error: {e.response['error']}")
        return e.response


def file_upload(slack_bot_token: str, slack_channel: str, filepath: str, comment: str):
    client = WebClient(token=slack_bot_token)

    try:
        response = client.files_upload(
            channels=slack_channel, file=filepath, initial_comment=comment
        )
        assert response["file"]  # the uploaded file
        return response
    except SlackApiError as e:
        # You will get a SlackApiError if "ok" is False
        assert e.response["ok"] is False
        assert e.response["error"]  # str like 'invalid_auth', 'channel_not_found'
        # print(f"Got an error: {e.response['error']}")
        return e.response
