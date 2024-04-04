# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: Apache-2.0.

from awscrt import mqtt, http
from awsiot import mqtt_connection_builder
import sys
import threading
import time
import json
from utils.command_line_utils import CommandLineUtils
from pymongo import MongoClient
import os 
from dotenv import load_dotenv


# Load environment variables
load_dotenv()
MONGOURI = os.getenv("MONGOURI")

# Setup MongoDB client and select the database and collection
client = MongoClient(MONGOURI, 27017)
db = client['hp_print_os']
collection = db['print_data']

# This is the Cloudservice that subscribes to the Message Broker for AWS IoT to receive data through 
# an MQTT connection. On startup, the device connects to the server and subscribes to the topic and 
# listens for messages sent to that topic.
# This accomplishes the broker to Cloudservice section of the project that will be streaming data
# into the backend that calculates the KPI's for use in the front end

# CmdData acts as the arguments/input placed into a single class for use in this sample.
# I created this to easily change hard-coded data for the purpose of testing 
# while setting up this system. The final implementation will most likely change from 
# this format.


# Configuration class for MQTT connection and message parameters
class CmdData:
    def __init__(self):
        self.input_endpoint = "az1v6dihq87k4-ats.iot.us-east-2.amazonaws.com"
        self.input_ca = "root-CA.crt"
        self.input_cert = "printOS_subscriber.cert.pem"
        self.input_key = "printOS_subscriber.private.key"
        self.input_clientId = "subscriber"
        self.input_topic = "sdk/printer/#"
        self.input_count = 0
        self.input_proxy_host = None
        self.input_proxy_port = 0
        self.input_port = 8883
        self.input_is_ci = False
        self.input_message = "Test Message V2"

cmdData = CmdData()
received_count = 0
received_all_event = threading.Event()


# Callback when connection is accidentally lost.
def on_connection_interrupted(connection, error, **kwargs):
    print("Connection interrupted. error: {}".format(error))


# Callback when an interrupted connection is re-established.
def on_connection_resumed(connection, return_code, session_present, **kwargs):
    print("Connection resumed. return_code: {} session_present: {}".format(return_code, session_present))

    if return_code == mqtt.ConnectReturnCode.ACCEPTED and not session_present:
        print("Session did not persist. Resubscribing to existing topics...")
        resubscribe_future, _ = connection.resubscribe_existing_topics()

        # Cannot synchronously wait for resubscribe result because we're on the connection's event-loop thread,
        # evaluate result with a callback instead.
        resubscribe_future.add_done_callback(on_resubscribe_complete)


def on_resubscribe_complete(resubscribe_future):
    resubscribe_results = resubscribe_future.result()
    print("Resubscribe results: {}".format(resubscribe_results))

    for topic, qos in resubscribe_results['topics']:
        if qos is None:
            sys.exit("Server rejected resubscribe to topic: {}".format(topic))


def on_message_received(topic, payload, dup, qos, retain, **kwargs):
    print("Received message from topic '{}': {}".format(topic, payload))
    global received_count
    received_count += 1
    try:
        # Assuming payload is a byte string of JSON
        payload_dict = json.loads(payload.decode('utf-8'))  # Decode byte string and parse JSON
        collection.insert_one({"topic": topic, "data": payload_dict})
    except json.JSONDecodeError:
        print("Error decoding JSON payload")
    except Exception as e:
        print(f"Error inserting into MongoDB: {e}")


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


# Set up proxy options if necessary
proxy_options = None
if cmdData.input_proxy_host and cmdData.input_proxy_port:
    proxy_options = http.HttpProxyOptions(
        host_name=cmdData.input_proxy_host,
        port=cmdData.input_proxy_port
    )

# Create a MQTT connection using the configuration data
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
    on_connection_closed=on_connection_closed
)

# Connect to the MQTT server
print(f"Connecting to {cmdData.input_endpoint} with client ID '{cmdData.input_clientId}'...")
connect_future = mqtt_connection.connect()
connect_future.result()
print("Connected!")

# Subscribe to the topic and wait for messages
print(f"Subscribing to topic '{cmdData.input_topic}'...")
subscribe_future, packet_id = mqtt_connection.subscribe(
    topic=cmdData.input_topic,
    qos=mqtt.QoS.AT_LEAST_ONCE,
    callback=on_message_received
)
subscribe_result = subscribe_future.result()
print(f"Subscribed with {str(subscribe_result['qos'])}")

# Continuous loop to keep the script running and listen for messages
try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    print("Interrupted, disconnecting...")

# Disconnect from the MQTT server
print("Disconnecting...")
disconnect_future = mqtt_connection.disconnect()
disconnect_future.result()
print("Disconnected!")