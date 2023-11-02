#This will be used to create more "things" to publish data to AWS IOT
#
import boto3
import json
import pathlib
import os

if not os.path.basename(os.getcwd()) == "Printer_creator":
    print("Current Working Directory is not in the Printer_Creator folder.")
    exit(1)
    
# Initialize the AWS IoT client
iot = boto3.client(
    'iot',
    region_name='us-east-2',
    aws_access_key_id='AKIAYXUEF7I5AISUPULC',
    aws_secret_access_key='t/Reko9M09w61Llh+2/8tW32DAc48kiUPHxJ4j9W',
    aws_session_token=None
)

thing_name = "automatic_printer_2"  #Replace with naming function that pulls it from DynamoDB later

# Create a new Thing
iot.create_thing(thingName=thing_name)

# Create keys and certificate for the Thing
keys_and_cert = iot.create_keys_and_certificate(setAsActive=True)

# Attach the certificate to the Thing
iot.attach_thing_principal(
    thingName=thing_name,
    principal=keys_and_cert['certificateArn']
)

# Create or use an existing IoT policy
# Define your policy document as a JSON string
policy_name = f"{thing_name}_Policy"
policy_document = {
    "Version": "2012-10-17",
    "Statement": [
      {
        "Effect": "Allow",
        "Action": [
          "iot:Publish",
          "iot:PublishRetain"
        ],
        "Resource": f"arn:aws:iot:us-east-2:600498895418:topic/printers/{thing_name}/data"
        
      },
      {
        "Effect": "Allow",
        "Action": "iot:Connect",
        "Resource": [
          "arn:aws:iot:us-east-2:600498895418:client/sdk-java",
          f"arn:aws:iot:us-east-2:600498895418:client/{thing_name}",
          "arn:aws:iot:us-east-2:600498895418:client/sdk-nodejs-*"
        ]
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

#grab the certificate ID in order to download the cert to local machine
certificate_id = keys_and_cert['certificateArn'].split('/')[-1]

# Download the certificate 
response = iot.describe_certificate(certificateId=certificate_id)
certificate_pem = response['certificateDescription']['certificatePem']

# Get the public and private keys
private_key = keys_and_cert['keyPair']['PrivateKey']
public_key = keys_and_cert['keyPair']['PublicKey']

# Download the policy
response = iot.get_policy(policyName=policy_name)
policy_document = response['policyDocument']

raw_code = f"import sys\nimport os\npwd = os.path.dirname(os.path.abspath(__file__))\npubRunner_dir = os.path.join(pwd, '..', 'lib')\nsys.path.append(pubRunner_dir)\nimport pubRunner\npubRunner.executePublishing('az1v6dihq87k4-ats.iot.us-east-2.amazonaws.com',\n'../{thing_name}/certificate.pem','../{thing_name}/private_key.key','{thing_name}','printers/{thing_name}/data')"


# Create the new folder and files to store data
path = pathlib.Path("../" + thing_name)
path.mkdir()

# Define the local file paths to save the certificate, keys, and policy
certificate_file_path = f"../{thing_name}/certificate.pem"
private_key_path = f"../{thing_name}/private_key.key"
public_key_path = f"../{thing_name}/public_key.key"
policy_file_path = f"../{thing_name}/policy.json"
code_file_path = f"../{thing_name}/main.py"

#write to new files
with open(certificate_file_path, "w") as cert_file:
    cert_file.write(certificate_pem)

with open(private_key_path, "w") as private_file:
    private_file.write(private_key)

with open(public_key_path, "w") as public_file:
    public_file.write(public_key)

with open(policy_file_path, "w") as policy_file:
    policy_file.write(policy_document)

with open(code_file_path, "w") as code_file:
    code_file.write(raw_code)



# Print out the certificate ARN and other information
print(f"Thing Name: {thing_name}")
print(f"Certificate ARN: {keys_and_cert['certificateArn']}")
print(f"Certificate ID: {keys_and_cert['certificateId']}")
