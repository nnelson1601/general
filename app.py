import logging
import sys
import os
from time import sleep

from flask import Flask, Response
from wordle import wordle
from tuxedo import tuxedo

app = Flask("general")

app.logger.setLevel(logging.INFO)
logging.getLogger().addHandler(logging.StreamHandler(sys.stdout))
app.logger.info("OS name - " + os.name)

app.register_blueprint(wordle)
app.register_blueprint(tuxedo)

@app.route("/api/warmup")
def warmup():
  app.logger.info(
      "The goal here is to warm up the app service so that it can fire other api calls quickly.")
  sleep(3)
  return Response(
      response="App service warmed up",
      status=200
  )

if __name__ == '__main__' : app.run(host="0.0.0.0", port=80)
