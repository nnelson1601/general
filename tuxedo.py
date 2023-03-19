"""Interfaces with Tuxedo control panel."""
import requests
from aiohttp.hdrs import CACHE_CONTROL, PRAGMA
from Crypto.Util.Padding import pad, unpad
from Crypto.Cipher import AES
import asyncio
import base64
from datetime import timedelta
from hashlib import sha1
import hmac
import json
import logging
import random
import re
from time import sleep
import urllib
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
urllib3.util.ssl_.DEFAULT_CIPHERS = 'ALL:@SECLEVEL=1'

from flask import Response, request, Blueprint

tuxedo = Blueprint("tuxedo", __name__)

@tuxedo.route("/api/tuxedo/sign_string", methods=["POST"])
def sign_string():
  value = request.form["value"]
  secret_key = request.form["secret_key"]

  return Response(
      response=hmac.new(bytes(secret_key, "utf-8"), bytes(value, "utf-8"), sha1).hexdigest(),
      status=200
  ) 


@tuxedo.route("/api/tuxedo/encrypt", methods=["POST"])
def encrypt():
  data = bytes(request.form["data"], "utf-8")
  private_key = request.form["private_key"]

  key_string = private_key[0:64]
  iv_string = private_key[64:]

  key = bytes.fromhex(key_string)
  iv = bytes.fromhex(iv_string)
  encryptor = AES.new(key, AES.MODE_CBC, IV=iv)
  cipher = encryptor.encrypt(pad(data, 16))

  encrypted_data = str(base64.b64encode(cipher), "utf-8")

  return Response(
      response=encrypted_data,
      status=200
  )


@tuxedo.route("/api/tuxedo/decrypt", methods=["POST"])
def decrypt():
  data = request.form["data"]
  private_key = request.form["private_key"]

  key_string = private_key[0:64]
  iv_string = private_key[64:]

  raw = base64.b64decode(data)
  key = bytes.fromhex(key_string)
  iv = bytes.fromhex(iv_string)
  encryptor = AES.new(key, AES.MODE_CBC, IV=iv)
  decrypted_data = str(unpad(encryptor.decrypt(raw), AES.block_size), "utf-8")

  return Response(
      response=decrypted_data,
      status=200
  )

