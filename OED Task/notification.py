import requests
import os
import datetime

USER_KEY = "uk3gn12updfquxpyxxa7z4459q265n"  # Your user key
API_TOKEN = "adfhpbk828kvfdnjgvq1xojabbgt5s"  # Replace with your actual API token
#MESSAGE = f"SSH login detected on {os.uname().nodename} at {datetime.datetime.now()}"

'''if 'PAM_TYPE' in os.environ and os.environ['PAM_TYPE'] == 'open_session':'''
    # Get the client's IP address
#client_ip = os.environ.get('PAM_RHOST', 'unknown IP')
MESSAGE ="Program run and added"
# Send notification
response = requests.post(
    "https://api.pushover.net/1/messages.json",
    data={
        "token": API_TOKEN,
        "user": USER_KEY,
        "message": MESSAGE,
    },
)

# Optional: Print response for debugging
print(response.text)
