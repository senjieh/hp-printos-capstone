# hp-printos-capstone
HP PrintOs Capstone 2023 Official Repository

Overview

This project consists of several services defined in a docker-compose.yml file, including an API, a front-end, a printer client, a cloud service subscriber, and a MongoDB database.
Services
API

    Directory: /api
    Exposed Port: 4001

Front-end

    Directory: /printos_front_end
    Exposed Port: 3000

Print Data Client

    Directory: /printer_client
    Exposed Port: 4000

Cloud Service Intake Process

    Directory: /cloudservice_subscriber
    Exposed Port: 3999

MongoDB

    Image: mongo:latest
    Container Name: mongodb
    Exposed Port: 27017
    Data Volume: mongodb_data

How to Run

    Ensure you have Docker and Docker Compose installed on your machine.
    Navigate to the project directory containing the docker-compose.yml file.
    Run the following command to start all services:

    bash

docker-compose up -d

To stop the services, use:

bash

    docker-compose down

Accessing the Services

After running the services:

    Access the API at: http://localhost:4001
    Access the Front-end at: http://localhost:3000
    Access the Print Data Client at: http://localhost:4000
    Access the Cloud Service Intake Process at: http://localhost:3999
    Access the MongoDB instance at: mongodb://localhost:27017

Data Persistence

The MongoDB service uses a named volume (mongodb_data) to persist its data. This ensures that even if the MongoDB container is removed, the data remains intact. If you wish to clear the MongoDB data, you can remove the named volume.
