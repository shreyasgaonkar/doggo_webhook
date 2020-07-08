import random
import os
import re
import requests
from random_user_agent.user_agent import UserAgent
from random_user_agent.params import SoftwareName, OperatingSystem


URL = 'https://www.reddit.com/r/dogpictures/top.json?sort=top&t=day&limit=25'
AVATAR_URL = 'http://brunswickplantationliving.com/wp-content/uploads/2013/04/dogs.jpg'
# Set webhook url from environment variable: webhook_url or hardcode it:
try:
    WEBHOOK_URL = os.environ['webhook_url']
except KeyError:
    WEBHOOK_URL = '<enter-webhook-url>'

# Add optional proxy servers if you are sending several requests
PROXY = ['188.213.31.73:808', '163.43.108.114:8080', '173.22.66.193:48678',
         '173.82.17.188:5836']

# Set this to False if not using proxy
USE_PROXY = True
COMPLETE = False


def random_user_agent():
    """Generate random user agent"""
    software_names = [SoftwareName.CHROME.value]
    operating_systems = [OperatingSystem.WINDOWS.value, OperatingSystem.LINUX.value]
    user_agent_rotator = UserAgent(software_names=software_names,
                                   operating_systems=operating_systems, limit=100)
    user_agent = user_agent_rotator.get_random_user_agent()
    return user_agent


def call_webhook(proxy, iteration):
    """Call webhook"""
    headers = {'user-agent': random_user_agent()}
    if not proxy:
        print("Calling without proxy servers")
        proxies = None
    else:
        print(f"\nTrying Proxy: {iteration}")
        proxies = {'https': iteration}
    try:
        res = requests.get(URL, headers=headers, allow_redirects=True,
                           proxies=proxies, timeout=5)
        data = res.json()
    except (Exception, requests.exceptions.ProxyError) as caught_exception:
        print(caught_exception)
        return

    random_post = random.randrange(0, 24)
    content_url = data['data']['children'][random_post]['data']['url_overridden_by_dest']
    print(f"Snagged url: {content_url}")

    data_post = parse_webhook(WEBHOOK_URL, content_url)

    response = requests.post(WEBHOOK_URL, json=data_post)
    print(response.status_code)
    global COMPLETE
    COMPLETE = True
    return True


def parse_webhook(url, content_url):
    """Parse webhook url for Slack/Discord"""
    if re.search(r'slack', url.lower()) is None:
        print("Found Discord webhook")

        # Return JSON payload back to POST method as per IM endpoint
        # JSON as per: https://discord.com/developers/docs/resources/webhook#execute-webhook
        return {
            "username": "Doggo_Bot",
            "avatar_url": AVATAR_URL,
            "embeds": [
                {
                    "image": {
                        "url": content_url
                    }
                }
            ],
        }

    # JSON as per: https://api.slack.com/messaging/webhooks
    print("Found Slack webhook")
    return {
        "username": "Doggo_Bot",
        "icon_url": AVATAR_URL,
        "text": "Woof woof!",
        "attachments": [{
            "image_url": content_url
        }]
    }


def main_function():
    """ Main function """

    if not USE_PROXY:
        call_webhook(proxy=False, iteration=None)

    else:
        for i in PROXY:
            if COMPLETE:
                print("Success: A Doggo is on it's way!")
                break
            call_webhook(proxy=True, iteration=i)


if __name__ == "__main__":
    main_function()
