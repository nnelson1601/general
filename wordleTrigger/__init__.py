import datetime
import logging

import azure.functions as func

import requests

APP_SERVICE_URL = "https://app-wordle.azurewebsites.net"
WARMUP_ROUTE = APP_SERVICE_URL + "/api/workflow/warmup"
SOLVE_ROUTE = APP_SERVICE_URL + "/api/workflow/solve"

def main(mytimer: func.TimerRequest) -> None:
    utc_timestamp = datetime.datetime.utcnow().replace(
        tzinfo=datetime.timezone.utc).isoformat()

    # if mytimer.past_due:
    #     logging.info('The timer is past due!')
    
    logging.info('Python timer trigger function ran at %s', utc_timestamp)

    logging.info('Warming up app service at %s', utc_timestamp)
    requests.get(APP_SERVICE_URL + '/api/workflow/warmup')

    logging.info('Warming it up again to be sure at %s', utc_timestamp)
    requests.get(APP_SERVICE_URL + '/api/workflow/warmup')

    logging.info('Solving wordle at %s', utc_timestamp)
    requests.get(APP_SERVICE_URL + '/api/workflow/solve')

    return True

if __name__ == '__main__' : main(None)
