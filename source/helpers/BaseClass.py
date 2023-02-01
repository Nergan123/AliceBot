import json
import boto3
import botocore.exceptions
from source.helpers.logging.LoggerBase import LoggingHandler


class BaseClass(LoggingHandler):
    """ Base class to save, log, load states """

    SERIALIZABLE_FIELDS = [

    ]

    def __init__(self, name):
        super().__init__()
        self.log.info(f"Base Class for {name} activated")
        self.json_name = name
        self.state_bucket = "nergan-bot"
        self.banned_ids = []

    def save_state(self) -> None:
        """ Saves the current state to .json object """

        self.log.info(f"{self.json_name} saving state to '{self.json_name}_data.json'")

        state = {}
        for property_name in self.SERIALIZABLE_FIELDS:
            state[property_name] = self.__getattribute__(property_name)

        s3 = boto3.resource('s3')
        remote_object = s3.Object(self.state_bucket, f"{self.json_name}_data.json")
        remote_object.put(Body=(bytes(json.dumps(state).encode('UTF-8'))))

    def load_state(self) -> None:
        """ Loads the current state from .json object """

        self.log.info(f"{self.json_name} loading state from '{self.json_name}_data.json'")

        try:
            s3 = boto3.client('s3')
            s3_response = s3.get_object(Bucket=self.state_bucket, Key=f"{self.json_name}_data.json")
            state_json = s3_response['Body'].read()
            state = json.loads(state_json)

            for property_name in self.SERIALIZABLE_FIELDS:
                self.__setattr__(property_name, state[property_name])
                self.log.info(f"{self.json_name} loaded {property_name} from "
                              f"'{self.json_name}_data.json'")

        except botocore.exceptions.ClientError as error:
            self.log.error(f"Can't Load {self.json_name}: {error}")
            self.log.info(f"Solving {error}. Attempting to "
                          f"save state to '{self.json_name}_data.json'")
            self.save_state()

        except KeyError as error:
            self.log.error(f"File corrupted. error: {error}. '{self.json_name}_data.json'")
            self.log.info("Attempting to solve")
            self.save_state()

    def check_banned_id(self, user_id) -> bool:
        """Checks if user is banned"""

        return user_id in self.banned_ids
