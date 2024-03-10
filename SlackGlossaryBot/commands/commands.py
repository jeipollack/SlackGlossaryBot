from subprocess import check_output


def register_glossary_commands(app):
    """Register Glossary Commands.

    Registers slash commands and actions related to glossary definitions.

    Parameters
    ----------
    app: App
        The Slack Bolt app.

    """
    # Cache dictionaries for storing fetched acronym definitions in English and Spanish
    english_messages = {}
    spanish_messages = {}

    def fetch_definition(text, config_path):
        """Fetch Definition.

        Fetches the definition of an acronym from the glossary.

        Parameters
        ----------
        text : str
            The acronym or term to fetch the definition for.
        config_path : str
            The path to the configuration file.

        Returns
        -------
        bytes
            The definition of the acronym in bytes.

        """
        return check_output(
            [
                "python3",
                "/opt/SlackGlossaryBot/SlackGlossaryBot/glossary/glossary.py",
                "-c",
                config_path,
                text,
            ]
        )

    def get_response_message(
        acronym,
        definition_message,
        button_text,
        action_id,
    ):
        """Get Response Message.

        Returns a response message with a button trigger.

        Parameters
        ----------
        acronym : str
            The acronym or term(s).
        definition_message : str
            The definition message.
        button_text : str
            The text displayed on the button.
        action_id : str
            The action ID triggered by the button.

        Returns
        -------
        dict
            The message with a button trigger.

        """
        message = {
            "text": definition_message,
            "blocks": [
                {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": definition_message,
                    },
                    "accessory": {
                        "type": "button",
                        "text": {
                            "type": "plain_text",
                            "text": button_text,
                        },
                        "action_id": action_id,
                        "value": acronym,  # Pass the acronym as the value
                    },
                }
            ],
        }
        return message

    @app.command("/glossary")
    def define_acronym(ack, respond, command):
        """Define Acronym.

        Defines an acronym and provides a button to trigger Spanish translation.

        Parameters
        ----------
        ack : Ack
            The acknowledge function.
        respond : Respond
            The respond function.
        command : dict
            The slash command.

        """
        ack()
        acronym = command["text"]
        # Check if the English translation is already cached
        if acronym in english_messages:
            definition_message = english_messages[acronym]
        else:
            definition = fetch_definition(
                acronym, "/opt/SlackGlossaryBot/config/config_csv.yml"
            )
            definition_message = (
                f"{acronym} => " + definition.decode("utf-8").strip().split("\n")[0]
            )
            english_messages[acronym] = definition_message

        # Build message with button to trigger get_spanish_translation
        message = get_response_message(
            acronym,
            definition_message,
            "Translate to Spanish :es:",
            "get_spanish_translation",
        )

        respond(message)

    @app.action("get_spanish_translation")
    def get_spanish_translation(ack, respond, action):
        """Get Spanish Translation.

        Fetches the Spanish translation of an acronym.

        Parameters
        ----------
        ack : Ack
            The acknowledge function.
        respond : Respond
            The respond function.
        action : dict
            The action triggered.

        """
        ack()
        acronym = action["value"]

        # Check if the Spanish translation is already cached
        if acronym in spanish_messages:
            definition_message = spanish_messages[acronym]
        else:
            definition = fetch_definition(
                acronym, "/opt/SlackGlossaryBot/config/config_es.yml"
            )  # Fetch Spanish definition based on the acronym
            definition_message = (
                f"{acronym} => " + definition.decode("utf-8").strip().split("\n")[0]
            )
            spanish_messages[acronym] = definition_message

        # Build message with button to translate to English
        message = get_response_message(
            acronym,
            definition_message,
            "Translate to English :us:",
            "get_english_translation",
        )
        respond(message)

    @app.action("get_english_translation")
    def get_english_translation(ack, respond, action):
        """Get English Translation.

        Fetches the English translation of an acronym.

        Parameters
        ----------
        ack : Ack
            The acknowledge function.
        respond : Respond
            The respond function.
        action : dict
            The action triggered.

        """
        ack()
        acronym = action["value"]
        if acronym in english_messages:
            definition_message = english_messages.get(acronym)
        else:
            definition = fetch_definition(
                acronym, "/opt/SlackGlossaryBot/config/config_csv.yml"
            )
            definition_message = (
                f"{acronym} => " + definition.decode("utf-8").strip().split("\n")[0]
            )
            english_messages[acronym] = definition_message

        # Build message with button to trigger /glosario command
        message = get_response_message(
            acronym,
            definition_message,
            "Traducción en Español :es:",
            "get_spanish_translation",
        )
        respond(message)

    @app.command("/glosario")
    def define_es_acronym(ack, respond, command):
        """Define Spanish Acronym.

        Defines a Spanish acronym and provides a button to trigger English translation.

        Parameters
        ----------
        ack : Ack
            The acknowledge function.
        respond : Respond
            The respond function.
        command : dict
            The slash command.

        """
        ack()
        #
        acronym = command["text"]
        # Check if the English translation is already cached
        if acronym in spanish_messages:
            definition_message = spanish_messages[acronym]
        else:
            definition = fetch_definition(
                acronym, "/opt/SlackGlossaryBot/config/config_es.yml"
            )
            definition_message = (
                f"{acronym} => " + definition.decode("utf-8").strip().split("\n")[0]
            )
            spanish_messages[acronym] = definition_message

        # Build message with button to trigger get_spanish_translation
        message = get_response_message(
            acronym,
            definition_message,
            "Traducción en Inglés :us:",
            "get_english_translation",
        )
        respond(message)
