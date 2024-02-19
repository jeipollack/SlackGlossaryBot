
This README provides comprehensive instructions for installing, using, and deploying SlackGlossary using Docker. Users can follow these instructions to get started with the application.


# SlackGlossaryBot

SlackGlossaryBot is a Python application that retrieves definitions for acronyms from a glossary stored in JSON or CSV format. It provides a simple command-line interface to look up acronym definitions.

## Installation

1. Clone the repository:

  ```bash
   git clone https://github.com/jeipollack/SlackGlossaryBot.git
```

2. Navigate to the project directory:

  ```bash
  cd SlackGlossaryBot
  ```

3. Install the dependencies using poetry

  ```bash
   poetry install
  ```


## Usage


**Command-line Options**
* **acronym**: The acronym(s) to look up.
* **--config CONFIG_FILE**: Path to the YAML configuration file specifying the glossary file path and format.
* **--similarity SIMILARITY**: Print similar acronyms, given a match fraction (0.0-1.0).


Example usage:
```
python app.py -c config.yaml -s 0.8 ABC
```

This will retrieve the definition for the acronym "NASA" from the glossary.

## Docker Deployment

You can deploy SlackGlossaryBot using Docker in two ways: using a Dockerfile or using docker-compose.

### Dockerfile Deployment
Building the Docker Image

Ensure Docker is installed on your system.
Build the Docker image:

```
docker build -t slack-glossary-bot .
```

Running the Docker Container

Once the Docker image is built, you can run the container:

```
docker run -d --name slack-glossary-app slack-glossary-bot
```

Replace slack-glossary-app with the desired name for your container.

Accessing the Application

You can access the application by accessing the container's shell:

```
docker exec -it slack-glossary-app /bin/bash
```

### docker-compose Deployment
Starting the Docker Compose Services

Ensure Docker and docker-compose are installed on your system.
Navigate to the project directory containing the docker-compose.yml file.
Start the services:

```
docker-compose up -d
```

Accessing the Application

You can access the application by accessing the container's shell:

```
docker-compose exec bot-app /bin/bash
```

Inside the container, you can run the application:

```
poetry run python SlackGlossaryBot/app.py [options]
```
