#This will be used to create more "things" to publish data to AWS IOT
#
import boto3

# Initialize the AWS IoT client
iot = boto3.client('iot')

# Define the name of the new Thing
thing_name = "printer123"  # Replace with a dynamic name if needed

# Create a new Thing
response = iot.create_thing(
    thingName=thing_name
)

# Create keys and certificate for the Thing
keys_and_cert = iot.create_keys_and_certificate(setAsActive=True)

# Attach the certificate to the Thing
iot.attach_thing_principal(
    thingName=thing_name,
    principal=keys_and_cert['certificateArn']
)

# Create or use an existing IoT policy
# Define your policy document as a JSON string
policy_name = "printer_policy"
policy_document = {
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": "iot:Publish",
            "Resource": f"arn:aws:iot:<your-region>:<your-account-id>:topic/printers/{thing_name}/data"
        },
        {
            "Effect": "Allow",
            "Action": "iot:Subscribe",
            "Resource": f"arn:aws:iot:<your-region>:<your-account-id>:topicfilter/printers/{thing_name}/data"
        }
    ]
}

# Create the policy
iot.create_policy(
    policyName=policy_name,
    policyDocument=json.dumps(policy_document)
)

# Attach the policy to the certificate
iot.attach_policy(
    policyName=policy_name,
    target=keys_and_cert['certificateArn']
)

# Print out the certificate ARN and other information
print(f"Thing Name: {thing_name}")
print(f"Certificate ARN: {keys_and_cert['certificateArn']}")
print(f"Certificate ID: {keys_and_cert['certificateId']}")
