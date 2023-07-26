import requests
import os
import subprocess
from slack_sdk import WebClient


def send_message(token, channel, message):
    url = "https://slack.com/api/chat.postMessage"
    headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json'
    }
    data = {
        'channel': channel,
        'text': message
    }
    response = requests.post(url, headers=headers, json=data)
    print(response, response.text)
    return response


def upload_file(token, channel, file_path="report.html", title="Pytest Results"):
    client = WebClient(token=token)
    response = client.files_upload(
        channels=channel,
        file=file_path,
        title=title
    )
    return response


def truncate_file(file_path="report.html", min_size=1000000):
    # Get the current size of the file
    file_size = os.path.getsize(file_path)

    if file_size < min_size:
        # Calculate the amount of padding needed
        padding_size = min_size - file_size

        # Truncate the file by appending padding_size bytes of null bytes
        with open(file_path, "ab") as file:
            file.write(b"\x00" * padding_size)


slack_token = os.environ['SLACK_TOKEN']
slack_channel = "#pytest-report"

# Send Pytest Report to Slack
summary = subprocess.check_output(['python', 'generate_report.py']).decode('utf-8')
send_message(slack_token, slack_channel, summary)

# Make Sure HTML Report Doesn't Return as Snippet
truncate_file()

# Send HTML Report to Slack
upload_file(slack_token, slack_channel)
