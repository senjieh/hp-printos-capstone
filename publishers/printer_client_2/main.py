# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: Apache-2.0.

from awscrt import mqtt, http
from awsiot import mqtt_connection_builder
import sys
import threading
import time
import json
from utils.command_line_utils import CommandLineUtils
from data_creator2 import get_job_results
import tkinter as tk
from tkinter import messagebox
import random
import string

# This client uses the Message Broker for AWS IoT to send data through an MQTT connection. 
# On startup, the device connects to the server and begins publishing messages to that topic.
# This accomplishes the client to broker section of the project that will end up sending
# printer information and data that can be sifted through to display KPI's

# CmdData acts as the arguments/input placed into a single class for use in this sample.
# I created this to easily change hard-coded data for the purpose of testing 
# while setting up this system. The final implementation will most likely change from 
# this format.
class CmdData:
    def __init__(self):
        self.input_endpoint = "az1v6dihq87k4-ats.iot.us-east-2.amazonaws.com"
        self.input_ca = "../rootCA/rootCA1.pem"
        self.input_cert = "printOS_client2.cert.pem"
        self.input_key = "printOS_client2.private.key"
        self.input_clientId = "publisher_2"
        self.input_topic = "sdk/printer/test"
        self.input_count = 0
        self.input_proxy_host = None
        self.input_proxy_port = 0
        self.input_port = 8883  # Assuming the default MQTT over TLS port
        self.input_is_ci = False  # Assuming you do not need CI functionality
        self.input_message = get_job_results(10)

cmdData = CmdData()
received_count = 0
received_all_event = threading.Event()


# Callback when connection is accidentally lost.
def on_connection_interrupted(connection, error, **kwargs):
    print("Connection interrupted. error: {}".format(error))


# Callback when an interrupted connection is re-established.
def on_connection_resumed(connection, return_code, session_present, **kwargs):
    print("Connection resumed. return_code: {} session_present: {}".format(return_code, session_present))


# Callback when the connection successfully connects
def on_connection_success(connection, callback_data):
    assert isinstance(callback_data, mqtt.OnConnectionSuccessData)
    print("Connection Successful with return code: {} session present: {}".format(callback_data.return_code, callback_data.session_present))


# Callback when a connection attempt fails
def on_connection_failure(connection, callback_data):
    assert isinstance(callback_data, mqtt.OnConnectionFailuredata)
    print("Connection failed with error code: {}".format(callback_data.error))


# Callback when a connection has been disconnected or shutdown successfully
def on_connection_closed(connection, callback_data):
    print("Connection closed")


# Function to generate a predefined printer data
def send_standard_data():
    printer_data = {
        "printer_id": 1,
        "timestamp": int(time.time()),
        "print_job_pages": 5,
        "print_job_pages_dropped": 3,
        "print_job_pages_printed": 2
    }
    send_message(printer_data)

# Function to generate a variant of the printer data
def send_variant_data():
    printer_data = {
        "printer_id": 1,
        "timestamp": int(time.time()),  # Current timestamp
        "print_job_pages": 10,
        "print_job_pages_dropped": 2,
        "print_job_pages_printed": 8
    }
    send_message(printer_data)

# Function to generate random printer data
def send_random_data():
    pages = random.randint(1, 100)
    pages_dropped = random.randint(0, pages)
    pages_printed = pages - pages_dropped
    printer_data = {
        "printer_id": 1,
        "timestamp": int(time.time()),
        "print_job_pages": pages,
        "print_job_pages_dropped": pages_dropped,
        "print_job_pages_printed": pages_printed
    }
    send_message(printer_data)

# Function to publish the message
def send_message(printer_data):
    message_json = json.dumps(printer_data)
    mqtt_connection.publish(
        topic=cmdData.input_topic,
        payload=message_json,
        qos=mqtt.QoS.AT_LEAST_ONCE)
    print(f"Published: {printer_data}")


if __name__ == '__main__':
    # GUI Setup
    root = tk.Tk()
    root.title("Printer Data Publisher")

    # Buttons
    standard_button = tk.Button(root, text="Send Standard Data", command=send_standard_data)
    variant_button = tk.Button(root, text="Send Variant Data", command=send_variant_data)
    random_button = tk.Button(root, text="Send Random Data", command=send_random_data)

    standard_button.pack(pady=10)
    variant_button.pack(pady=10)
    random_button.pack(pady=10)

    proxy_options = None
    if cmdData.input_proxy_host is not None and cmdData.input_proxy_port != 0:
        proxy_options = http.HttpProxyOptions(
            host_name=cmdData.input_proxy_host,
            port=cmdData.input_proxy_port)

    # Create a MQTT connection from the command line data
    mqtt_connection = mqtt_connection_builder.mtls_from_path(
        endpoint=cmdData.input_endpoint,
        port=cmdData.input_port,
        cert_filepath=cmdData.input_cert,
        pri_key_filepath=cmdData.input_key,
        ca_filepath=cmdData.input_ca,
        on_connection_interrupted=on_connection_interrupted,
        on_connection_resumed=on_connection_resumed,
        client_id=cmdData.input_clientId,
        clean_session=False,
        keep_alive_secs=30,
        http_proxy_options=proxy_options,
        on_connection_success=on_connection_success,
        on_connection_failure=on_connection_failure,
        on_connection_closed=on_connection_closed)


    if not cmdData.input_is_ci:
        print(f"Connecting to {cmdData.input_endpoint} with client ID '{cmdData.input_clientId}'...")
    else:
        print("Connecting to endpoint with client ID")
    connect_future = mqtt_connection.connect()
    connect_future.result()
    print("Connected!")

    root.mainloop()

    # Disconnect on close
    def on_closing():
        print("Disconnecting...")
        disconnect_future = mqtt_connection.disconnect()
        disconnect_future.result()
        print("Disconnected!")
        root.destroy()

    root.protocol("WM_DELETE_WINDOW", on_closing)
