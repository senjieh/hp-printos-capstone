# Use the official Python 3 image as a base image
FROM python:3

# Set the working directory
WORKDIR /app

COPY requirements.txt .

RUN pip install -r requirements.txt

# # Copy the necessary files to the container at /app
ADD ./root-CA.crt /app/root-CA.crt
ADD ./printOS_subscriber.cert.pem /app/printOS_subscriber.cert.pem
ADD ./printOS_subscriber.private.key /app/printOS_subscriber.private.key

# Install the necessary system packages and set up environment
RUN apt-get update && \
    apt-get install -y git && \
    pip install --upgrade pip && \
    # Check to see if root CA file exists, download if not
    if [ ! -f "/app/root-CA.crt" ]; then \
        curl -o /app/root-CA.crt https://www.amazontrust.com/repository/AmazonRootCA1.pem; \
    fi && \
    # Clone the AWS SDK
    git clone https://github.com/aws/aws-iot-device-sdk-python-v2 --recursive && \
    # Install the AWS SDK
    pip install ./aws-iot-device-sdk-python-v2

COPY . .

EXPOSE 3999

# The command that will be executed when the container starts
CMD ["python", "-u", "main.py"]
