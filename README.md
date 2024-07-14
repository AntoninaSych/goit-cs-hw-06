# GOIT CS HW 06

## Description

This project is a simple web application that interacts with a server using sockets and stores information in a MongoDB database. It includes an HTTP server, a Socket server, and utilizes Docker for containerization.

## Setup

1. Clone the repository:
    ```bash
    git clone https://github.com/yourusername/goit-cs-hw-06.git
    cd goit-cs-hw-06
    ```

2. Build and run the Docker containers:
    ```bash
    docker-compose up --build
    ```

3. Access the web application:
    - HTTP server: [http://localhost:3000](http://localhost:3000)
    - MongoDB: `mongodb://localhost:27017/`

## Usage

- Navigate to the home page and go to the message page to send a message.
- The message will be sent to the Socket server and stored in the MongoDB database.
- Check the console for confirmation of saved messages.
