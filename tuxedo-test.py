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

FLASK_ORIGIN="http://localhost:5000"

DEFAULT_NAME = "Tuxedo"
TUXEDO_ORIGIN = "https://192.168.4.42"
API_REV = "API_REV01"
API_BASE_PATH = TUXEDO_ORIGIN + "/system_http_api/" + API_REV

MAC = ""
PRIVATE_KEY = ""
API_KEY_ENC = PRIVATE_KEY[0:64]
API_IV_ENC = PRIVATE_KEY[64:]

CODE = "1601"

def _sign_string(value, secret_key):
    response = requests.post(f"{FLASK_ORIGIN}/api/tuxedo/sign_string", data={"value": value, "secret_key": secret_key})
    return response.content.decode()

def _encrypt_data(data, private_key):
    response = requests.post(f"{FLASK_ORIGIN}/api/tuxedo/encrypt", data={"data": data, "private_key": private_key})
    return response.content.decode()

def _decrypt_data(data, private_key):
    response = requests.post(f"{FLASK_ORIGIN}/api/tuxedo/decrypt", data={"data": data, "private_key": private_key})
    return response.content.decode()

def api_call(api_route, params):
    uri_params = urllib.parse.urlencode(params)
    uri_params_encrypted = _encrypt_data(uri_params, PRIVATE_KEY)
    full_url = API_BASE_PATH + api_route
    header = "MACID:" + MAC + ",Path:" + API_REV + api_route
    print(header)
    print(API_KEY_ENC)
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
print(_decrypt_data(json.loads(get_status_response.content)["Result"], PRIVATE_KEY))

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
