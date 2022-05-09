import datetime
import logging

import requests

import azure.functions as func

url = 'https://prod-04.centralus.logic.azure.com:443/workflows/ba702c58db334b86bbd490eed1a9c898/triggers/manual/paths/invoke?api-version=2016-10-01&sp=%2Ftriggers%2Fmanual%2Frun&sv=1.0&sig=1vH0g_Yi-YLkxtM9W2pykxDE29uMZHGAGnQYCSMSa7M'

def main(mytimer: func.TimerRequest) -> None:
    utc_timestamp = datetime.datetime.utcnow().replace(
        tzinfo=datetime.timezone.utc).isoformat()

    if mytimer.past_due:
        logging.info('The timer is past due!')

    logging.info('Python timer trigger function ran at %s', utc_timestamp)

    x = requests.post(url)


