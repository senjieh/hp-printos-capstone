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

## Outdated

~~HP PrintOs Capstone 2023 Official Repository~~

~~Overview~~

~~This project consists of several services defined in a docker-compose.yml file, including an API, a front-end, a printer client, a cloud service subscriber, and a MongoDB database.~~
~~Services~~
~~API~~

   ~~Directory: /api~~
    ~~Exposed Port: 4001~~

~~Front-end~~

   ~~Directory: /printos_front_end~~
    ~~Exposed Port: 3000~~

~~Print Data Client~~

   ~~Directory: /printer_client~~
    ~~Exposed Port: 4000~~

~~Cloud Service Intake Process~~

   ~~Directory: /cloudservice_subscriber~~
    ~~Exposed Port: 3999~~

~~MongoDB~~

   ~~Image: mongo:latest~~
    ~~Container Name: mongodb~~
    ~~Exposed Port: 27017~~
    ~~Data Volume: mongodb_data~~

~~How to Run~~

   ~~Ensure you have Docker and Docker Compose installed on your machine.~~
    ~~Navigate to the project directory containing the docker-compose.yml file.~~
    ~~Run the following command to start all services:~~

 ~~bash~~

~~docker-compose up -d~~

~~To stop the services, use:~~

~~bash~~

   ~~docker-compose down~~

~~Accessing the Services~~

~~After running the services:~~

   ~~Access the API at: http://localhost:4001
    Access the Front-end at: http://localhost:3000
    Access the Print Data Client at: http://localhost:4000
    Access the Cloud Service Intake Process at: http://localhost:3999
    Access the MongoDB instance at: mongodb://localhost:27017~~

~~Data Persistence~~

~~The MongoDB service uses a named volume (mongodb_data) to persist its data. This ensures that even if the MongoDB container is removed, the data remains intact. If you wish to clear the MongoDB data, you can remove the named volume.~~
