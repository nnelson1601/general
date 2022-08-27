
import json
import os
from dotenv import load_dotenv

import datetime

from flask import Response, request

from azure.storage.blob import BlobClient

load_dotenv()
STCREIGHTON_STRING = os.getenv('STCREIGHTON_STRING')

from __main__ import app

@app.route("/api/creighton/observation", methods = ['POST', 'GET'])
def record_observation():
    print("TESTING")
    data = request.get_json()

    blob_client = BlobClient.from_connection_string(
        STCREIGHTON_STRING, container_name="observations", blob_name="creighton.json")

    download_stream = blob_client.download_blob()
    print(json.loads(download_stream.readall()))

    print(blob_client)

    return
    utc_timestamp = datetime.datetime.utcnow().replace(
            tzinfo=datetime.timezone.utc).isoformat()


    return Response(
        response="Wordle game complete",
        status=200
    )
