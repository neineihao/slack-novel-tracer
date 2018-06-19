from slackclient import SlackClient
import configparser
from SQL_process import find_update
from apscheduler.schedulers.background import BlockingScheduler


# instantiate Slack client
scheduler = BlockingScheduler()
config = configparser.ConfigParser()
config.read('config.ini')
general_id = 'CB9S0JTB5'
sc = SlackClient(config['slack_ini']['Bot User OAuth'])

def send_massege(channel, message="Hello from Python! :tada:"):
    sc.api_call(
        "chat.postMessage",
        channel=channel,
        text=message
    )

def main():
    texts = find_update()
    if texts:
        for text in texts:
            send_massege(general_id, message=text)
    else:
        send_massege(general_id, message="It works")



if __name__ == '__main__':
    scheduler.add_job(main, 'interval', minutes=15)
    scheduler.start()
