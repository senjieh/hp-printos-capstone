# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: Apache-2.0.

from awscrt import mqtt, http
from awsiot import mqtt_connection_builder
import sys
import threading
import time
import random
import string
import json

# This client uses the Message Broker for AWS IoT to send data through an MQTT connection. 
# On startup, the device connects to the server and begins publishing messages to that topic.
# This accomplishes the client to broker section of the project that will end up sending
# printer information and data that can be sifted through to display KPI's

# PrinterPublisher is the class that represents the publisher, creates and sends data to IOT
#
class PrinterPublisher:
    def __init__(self, endpoint, basicCert, privateKey, clientID, iotTopic):
        self.input_endpoint = endpoint
        self.input_ca = "../rootCA/rootCA1.pem"
        self.input_cert = basicCert
        self.input_key = privateKey
        self.input_clientId = clientID
        self.input_topic = iotTopic
        self.input_count = 0
        # Assuming you do not need the proxy settings
        self.input_proxy_host = None
        self.input_proxy_port = 0
        # Add other necessary fields with default or hardcoded values as needed
        self.input_port = 8883  # Assuming the default MQTT over TLS port
        self.input_is_ci = False  # Assuming you do not need CI functionality
        self.input_message = "Test Message"


        received_count = 0
        received_all_event = threading.Event()

    def generate_random_id(self, length=8):
        """
        Generate a random ID consisting of both letters and numbers.
        """
        return ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(length))

    def generate_printer_data(self):
        """
        Generate random printer data.
        """
        job_name = random.choice(["Document", "Presentation", "Invoice", "Report", "Letter"])
        pages = random.randint(1, 100)  # Assuming a document can have up to 100 pages
        pages_dropped = random.randint(0, pages)  # Randomly determine how many pages failed to print
        pages_printed = pages - pages_dropped

        return {
            "id": random.randint(1, 1000000),
            "printer_id": 1,
            "print_job": self.generate_random_id(),
            "print_job_pages": pages,
            "print_job_pages_dropped": pages_dropped,
            "print_job_pages_printed": pages_printed,
            "timestamp": int(time.time())
        }

    # Callback when connection is accidentally lost.
    def on_connection_interrupted(self, connection, error, **kwargs):
        print("Connection interrupted. error: {}".format(error))


    # Callback when an interrupted connection is re-established.
    def on_connection_resumed(self, connection, return_code, session_present, **kwargs):
        print("Connection resumed. return_code: {} session_present: {}".format(return_code, session_present))


    # Callback when the connection successfully connects
    def on_connection_success(self, connection, callback_data):
        assert isinstance(callback_data, mqtt.OnConnectionSuccessData)
        print("Connection Successful with return code: {} session present: {}".format(callback_data.return_code, callback_data.session_present))


    # Callback when a connection attempt fails
    def on_connection_failure(self, connection, callback_data):
        assert isinstance(callback_data, mqtt.OnConnectionFailuredata)
        print("Connection failed with error code: {}".format(callback_data.error))


    # Callback when a connection has been disconnected or shutdown successfully
    def on_connection_closed(self, connection, callback_data):
        print("Connection closed")


def executePublishing(endpoint, basicCertPATH, privateKeyPATH, clientID, iotTopic):

    printerP = PrinterPublisher(endpoint, basicCertPATH, privateKeyPATH, clientID, iotTopic)

    # Create the proxy options if the data is present in cmdData
    proxy_options = None
    if printerP.input_proxy_host is not None and printerP.input_proxy_port != 0:
        proxy_options = http.HttpProxyOptions(
            host_name=printerP.input_proxy_host,
            port=printerP.input_proxy_port)

    # Create a MQTT connection from the command line data
    mqtt_connection = mqtt_connection_builder.mtls_from_path(
        endpoint=printerP.input_endpoint,
        port=printerP.input_port,
        cert_filepath=printerP.input_cert,
        pri_key_filepath=printerP.input_key,
        ca_filepath=printerP.input_ca,
        on_connection_interrupted=printerP.on_connection_interrupted,
        on_connection_resumed=printerP.on_connection_resumed,
        client_id=printerP.input_clientId,
        clean_session=False,
        keep_alive_secs=30,
        http_proxy_options=proxy_options,
        on_connection_success=printerP.on_connection_success,
        on_connection_failure=printerP.on_connection_failure,
        on_connection_closed=printerP.on_connection_closed)

    if not printerP.input_is_ci:
        print(f"Connecting to {printerP.input_endpoint} with client ID '{printerP.input_clientId}'...")
    else:
        print("Connecting to endpoint with client ID")
    connect_future = mqtt_connection.connect()

    # Future.result() waits until a result is available
    connect_future.result()
    print("Connected!")

    message_count = printerP.input_count
    message_topic = printerP.input_topic

    if message_count == 0:
        print("Sending messages until program killed")
    else:
        print("Sending {} message(s)".format(message_count))

    publish_count = 1
    while (publish_count <= message_count) or (message_count == 0):
        printer_data = printerP.generate_printer_data()
        print("Publishing message to topic '{}': {}".format(message_topic, printer_data))
        message_json = json.dumps(printer_data)
        mqtt_connection.publish(
            topic=message_topic,
            payload=message_json,
            qos=mqtt.QoS.AT_LEAST_ONCE)
        time.sleep(random.randint(5, 30))  # Randomize sleep time between 5 to 30 seconds
        publish_count += 1

    # Disconnect
    print("Disconnecting...")
    disconnect_future = mqtt_connection.disconnect()
    disconnect_future.result()
    print("Disconnected!")