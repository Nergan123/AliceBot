import os
import logging
from dotenv import load_dotenv
from source.Alice import Alice


load_dotenv()
token = os.getenv('Token')


def main():
    """Function to launch the bot"""

    bot = Alice(command_prefix="!")
    bot.run(token)


if __name__ == "__main__":
    if not os.path.isdir('alice_logs'):
        os.makedirs('alice_logs')

    logging.basicConfig(
        level=logging.DEBUG,
        format='%(asctime)s [%(name)s]: %(levelname)s: %(message)s',
        handlers=[
            logging.FileHandler("alice_logs/logs.log", 'a'),
            logging.StreamHandler()
        ]
    )
    main()
