"""This module has components that are used for testing tuya's device control and Pulsar massage queue."""
import logging
import os
import time
import re
import pandas as pd
import openpyxl
import datetime
from threading import Thread
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
DEVICE_ID_BRICK = "bfa931ed1d78c0fad7mkll"
DEVICE_ID_Аeratedconcrete = "bfa6826e5e45e21a82u08p"

# response = openapi.get("/v1.0/iot-03/devices/{}/status".format(DEVICE_ID_BRICK))


def data_energy(response):
    response = str(response)
    exchange = response[21:70]
    pattern = r"'value': (\d+)"
    match = re.search(pattern, exchange)
    value = int(match.group(1))
    return value


def change_data(data):
    data = data[:-2]+"."+data[len(data)-2:]

    return data


brick_old_data = int(data_energy(openapi.get(
    "/v1.0/iot-03/devices/{}/status".format(DEVICE_ID_BRICK))))
aercon_old_data = int(data_energy(openapi.get(
    "/v1.0/iot-03/devices/{}/status".format(DEVICE_ID_Аeratedconcrete))))
df = pd.DataFrame([], columns=['Time', 'Аerated concrete', 'Brick'])

while True:
    time.sleep(300)
    brick_new_data = int(data_energy(openapi.get(
        "/v1.0/iot-03/devices/{}/status".format(DEVICE_ID_BRICK))))
    aercon_new_data = int(data_energy(openapi.get(
        "/v1.0/iot-03/devices/{}/status".format(DEVICE_ID_Аeratedconcrete))))
    df.loc[len(df)] = [datetime.datetime.now(), float(change_data(str(brick_new_data))) - float(change_data(
        str(brick_old_data))), float(change_data(str(aercon_new_data))) - float(change_data(str(aercon_old_data)))]
    brick_old_data = int(data_energy(openapi.get(
        "/v1.0/iot-03/devices/{}/status".format(DEVICE_ID_BRICK))))
    aercon_old_data = int(data_energy(openapi.get(
        "/v1.0/iot-03/devices/{}/status".format(DEVICE_ID_Аeratedconcrete))))
    df.to_excel('./energy.xlsx', index=False)
