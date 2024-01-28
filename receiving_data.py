"""This module has components that are used for testing tuya's device control and Pulsar massage queue."""
import logging
import os 
import re
from tuya_connector import (
    TuyaOpenAPI,
    TuyaOpenPulsar,
    TuyaCloudPulsarTopic,
    TUYA_LOGGER,
)

ACCESS_ID = "9qju98emj4m7fwapss7s"
ACCESS_KEY = "545add9613ca42008b97c24913d3dfb8"
API_ENDPOINT = "https://openapi.tuyaeu.com"
MQ_ENDPOINT = "wss://mqe.tuyaeu.com:8285/"

# Enable debug log
TUYA_LOGGER.setLevel(logging.DEBUG)

# Init openapi and connect
openapi = TuyaOpenAPI(API_ENDPOINT, ACCESS_ID, ACCESS_KEY)
openapi.connect()

# Call any API from Tuya
DEVICE_ID ="bfa931ed1d78c0fad7mkll"

response = openapi.get("/v1.0/iot-03/devices/{}/status".format(DEVICE_ID))

if os.path.exists("energy.txt"):
    os.remove("D:\IoT\energy.txt")

with open("energy.txt","w+") as my_file:
    response = str(response)
    exchange = response[21:70]
    pattern = r"'value': (\d+)"
    match = re.search(pattern, exchange)
    value = int(match.group(1))
    my_file.write(str(value))
