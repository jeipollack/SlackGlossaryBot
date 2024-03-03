import os
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler
from dotenv import load_dotenv
from commands.commands import register_glossary_commands


load_dotenv("bot.env")


def start_socket_mode_handler(app):
    socket_handler = SocketModeHandler(app, os.environ["SLACK_APP_TOKEN"]).start()
    return socket_handler


def main():
    # Initializes your app with your bot token
    app = App(token=os.environ.get("SLACK_BOT_TOKEN"))

    # Register glossary commands
    register_glossary_commands(app)

    # Start your app
    socket_handler = start_socket_mode_handler(app)
    socket_handler.start()


if __name__ == "__main__":
    main()
