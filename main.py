import os
import logging
from dotenv import load_dotenv
from source.Alice import Alice
from source.helpers.logging.Formatter import CustomFormatter


load_dotenv()
token = os.getenv('Token')


def main():
    """Function to launch the bot"""

    bot = Alice(command_prefix="!")
    bot.run(token)


if __name__ == "__main__":
    if not os.path.isdir('alice_logs'):
        os.makedirs('alice_logs')

    fmt = '%(asctime)s [%(name)s]: %(levelname)s: %(message)s'

    stdout_handler = logging.StreamHandler()
    stdout_handler.setLevel(logging.DEBUG)
    stdout_handler.setFormatter(CustomFormatter(fmt))

    file_handler = logging.FileHandler("alice_logs/logs.log", 'a')
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(logging.Formatter(fmt))

    logging.basicConfig(
        level=logging.DEBUG,
        handlers=[
            stdout_handler,
            file_handler
        ]
    )
    main()
