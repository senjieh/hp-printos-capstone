# hp-printos-capstone

## Current Prototype - 11/16/23

Overview

The frontend was developed using Vue3, the backend is comprised of an API, MongoDB database, cloud service subscriber and publisher.

Relevant Directories to run current prototype

- Vue_frontend: contains all frontend code, all in Vue3
- aws_spring_ec2: this is the API, was developed with Java Spring Boot
- cloudservice_subscriber: pushes AWS IoT publisher data into our MongoDB database
- publishers: publishers that create device data
- testing: test suite
- .github/workflows: for github actions (CI/CD)

Irrelevant Directories

- Vue_frontend_rounting_practice: this was made to learn how to do page routing for frontend
- api: this is an old api for an initial wireframe prototype
- aws_iot_core_sdk: provided by AWS when we were initially setting up AWS IoT core
- printos_front_end: original wireframe prototype
- mongodb: was our mongodb setup for original wireframe prototype

To run

1. install npm into your device
   a. Windows and Mac: https://nodejs.org/en/download/
   b. make sure to select npm package manager during installation options
2. verify npm and node are installed

```
node -v
npm -v
```

3. cd into Vue_frontend
4. run the following

```
npm install
npm run serve
```

5. click on localhost to view frontend
