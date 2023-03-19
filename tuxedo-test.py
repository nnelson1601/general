"""Interfaces with Tuxedo control panel."""
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

from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from aiohttp.hdrs import CACHE_CONTROL, PRAGMA
import requests

_LOGGER = logging.getLogger(__name__)

DEFAULT_NAME = "Tuxedo"
DOMAIN = "https://192.168.4.42"
API_REV = "API_REV01"
API_BASE_PATH = DOMAIN + "/system_http_api/" + API_REV

MAC = ""
PRIVATE_KEY = ""
API_KEY_ENC = PRIVATE_KEY[0:64]
API_IV_ENC = PRIVATE_KEY[64:]

CODE = ""

def _sign_string(value, secret_key):
    return hmac.new(bytes(secret_key, "utf-8"), bytes(value, "utf-8"), sha1).hexdigest()

def _encrypt_data(data, key_string, iv_string):
    key = bytes.fromhex(key_string)
    iv = bytes.fromhex(iv_string)
    encryptor = AES.new(key, AES.MODE_CBC, IV=iv)
    cipher = encryptor.encrypt(pad(data, 16))
    return str(base64.b64encode(cipher), "utf-8")

def _decrypt_data(data, key_string, iv_string):
    raw = base64.b64decode(data)
    key = bytes.fromhex(key_string)
    iv = bytes.fromhex(iv_string)
    encryptor = AES.new(key, AES.MODE_CBC, IV=iv)
    decrypted = unpad(encryptor.decrypt(raw), AES.block_size)
    return str(decrypted, "utf-8")

def api_call(api_route, params):
    uri_params = urllib.parse.urlencode(params)
    uri_params_encrypted = _encrypt_data(
        bytes(uri_params, "utf-8"), API_KEY_ENC, API_IV_ENC
    )
    full_url = API_BASE_PATH + api_route
    header = "MACID:" + MAC + ",Path:" + API_REV + api_route
    authtoken = _sign_string(header, API_KEY_ENC)

    data = {
        "param": uri_params_encrypted,
        "len": len(urllib.parse.quote_plus(uri_params_encrypted)),
        "tstamp": random.random()
    }

    headers = {
        "authtoken": authtoken,
        "identity": API_IV_ENC,
        str(PRAGMA): "no-cache",
        str(CACHE_CONTROL): "no-cache"
    }

    r = requests.post(
        full_url,
        data=data,
        headers=headers,
        verify=False,
        allow_redirects=False
    )
    return r

try:
    register_route = "/Registration/Register"
    register_params = {"mac": MAC, "operation": "set"}
    register_response = api_call(register_route, register_params)
    register_response.raise_for_status()
    print(register_response)
except Exception as e:
    print("Registration failed")
    print(e)
    exit(0)

get_status_route = "/GetSecurityStatus"
get_status_params = {"operation": "get"}
get_status_response = api_call(get_status_route, get_status_params)
print(_decrypt_data(json.loads(get_status_response.content)["Result"], API_KEY_ENC, API_IV_ENC))

# arm_with_code_route = "/AdvancedSecurity/ArmWithCode"
# arm_with_code_params = { "arming": "STAY", "pID": "1", "ucode": CODE, "operation": "set" }
# arm_with_code_response = api_call(arm_with_code_route, arm_with_code_params)
# print(arm_with_code_response)

# sleep(3)

# get_status_route = "/GetSecurityStatus"
# get_status_params = {"operation": "get"}
# get_status_response = api_call(get_status_route, get_status_params)
# print(_decrypt_data(json.loads(get_status_response.content)["Result"], API_KEY_ENC, API_IV_ENC))

# disarm_with_code_route = "/AdvancedSecurity/DisarmWithCode"
# disarm_with_code_params = {"pID": "1", "ucode": CODE, "operation": "set"}
# disarm_with_code_response = api_call(disarm_with_code_route, disarm_with_code_params)
# print(disarm_with_code_response)

# sleep(3)

# get_status_route = "/GetSecurityStatus"
# get_status_params = {"operation": "get"}
# get_status_response = api_call(get_status_route, get_status_params)
# print(_decrypt_data(json.loads(get_status_response.content)["Result"], API_KEY_ENC, API_IV_ENC))

unregister_route = "/Registration/Unregister"
unregister_params = {"mac": MAC, "operation": "set"}
unregister_response = api_call(unregister_route, unregister_params)
print(unregister_response)
