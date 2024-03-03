
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

## Configuration Options

A YAML file is used to set the configuration options for the Glossary functionality, such as the path to the glossary file and file type (JSON or CSV), as well as optional settings such as language, preprocessing flag, and similarity ratio for matching strings.

1. **Glossary File Location**:
* **Option Name**: path
* **Description**: Specifies the file path of the glossary.
* **Example**: /path/to/glossary.json

2. **File Type**:
* **Option Name**: file_type
* **Description**: Indicates the type of glossary file (e.g., JSON, CSV).
* **Example**: `json`

3. **Preprocessing Flag**:
* **Option Name**: preprocess
* **Description**: Specifies whether the glossary data has been preprocessed.
* **Example**: `True` or `False`
* **Notes**: Required for JSON files; not applicable for CSV files.

4. **Language** (Optional):
* **Option Name**: language
* **Description**: Specifies the language for responses (e.g., English, Spanish).
* **Example**: `english`
* **Notes**: Optional; default is English.

5. **Similarity Threshold** (Optional):
* **Option Name**: similarity_threshold
* **Description**: Sets the minimum similarity ratio for acronym matching.
* **Example**: `0.7`
* **Notes**: Optional; default is 0.8. Used for acronym matching.

**Configuration Usage Examples** 

* **JSON Configuration**
```yaml
path: /path/to/glossary.json
file_type: json
preprocess: true
language: english
similarity_threshold: 0.7
```

* **CSV Configuration**
```yaml
path: /path/to/glossary.json
file_type: json
language: spanish
```

**Notes**
* The preprocessing flag (preprocess) should be set to True for JSON files to indicate that the glossary data has been preprocessed. This flag is not applicable for CSV files.
* Ensure that the preprocessing flag is adjusted accordingly based on the file type being used (JSON or CSV).

## Command-line Usage

**Command-line Options**
* **acronym**: The acronym(s) to look up.
* **--config CONFIG_FILE**: Path to the YAML configuration file specifying the glossary file path and format.
* **--similarity SIMILARITY**: Print similar acronyms, given a match fraction (0.0-1.0).

*Example usage*:
```
python SlackGlossaryBot/glossary/glossary.py -c config/config.yml NASA
```
This will retrieve the definition for the acronym "NASA" from the glossary.

## Running the App

To run this app on your local machine, you only need to follow these simple steps:

* Create a new Slack app using the `manifest.yml` file
* Install the app into your Slack workspace

After going through the above local development process, you can deploy the app using `Dockerfile`, which is placed at the root directory.

The `Dockerfile` is designed to establish a WebSocket connection with Slack via Socket Mode.
This means that there's no need to provide a public URL for communication with Slack.

## Environment Variables

Before running the Slack Glossary Bot, you need to set up environment variables containing your Slack Bot tokens. These tokens are necessary for authenticating the bot with Slack and enabling it to interact with your workspace.

**Setting Up Environment Variables**

The `app.py` uses `load_dotenv()` to load the environment variables. Therefore, you can set the environment variables in a `bot.env` file located in the root directory of your project. Add the following lines to your `bot.env` file:

1. **SLACK_BOT_TOKEN**: This environment variable should contain your Slack Bot User OAuth Access Token. You can obtain this token by creating a Slack app, adding a bot user, and generating a bot token.
2. **SLACK_APP_TOKEN**: This environment variable should contain your Slack App Level Token. This token is used to establish a connection between your Slack app and the Slack API.

## Docker Deployment

You can deploy SlackGlossaryBot using Docker in two ways: using a Dockerfile or using docker-compose.

### Dockerfile Deployment
**Building the Docker Image**

Ensure Docker is installed on your system.
Build the Docker image:

```
docker build -t slack-glossary-bot .
```

**Running the Docker Container**

Once the Docker image is built, you can run the container:

```
docker run -d --name slack-glossary-app slack-glossary-bot
```

Replace slack-glossary-app with the desired name for your container.

**Accessing the Application**

You can access the application by accessing the container's shell:

```
docker exec -it slack-glossary-app /bin/bash
```

Inside the container, you can run the application:

```
poetry run python SlackGlossaryBot/app.py
```

### docker-compose Deployment
**Starting the Docker Compose Services**

Ensure Docker and docker-compose are installed on your system.
Navigate to the project directory containing the docker-compose.yml file.

**Build the docker image:**

```
docker-compose build
```

**Start the services:**

```
docker-compose up -d
```

**Accessing the Application**

You can access the application by accessing the container's shell:

```
docker-compose exec bot-app /bin/bash
```

## The License

The MIT License

## Reporting Issues

If you encounter any issues with the SlackGlossaryBot application or have questions about its usage, you can report them on the GitHub repository's issue tracker. Please provide detailed information about the problem you're experiencing, including steps to reproduce it, your environment (e.g., operating system, Python version), and any relevant error messages.

I will review your reported issues and provide assistance as soon as possible. I appreciate your feedback and contributions to improving the SlackGlossaryBot application.