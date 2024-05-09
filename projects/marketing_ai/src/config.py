import os
from dotenv import load_dotenv

"""
This module provides the Config class to manage configuration variables
from environment files. It also supports fetching test cases 
ifthe configuration is loaded from a test environment file.
"""


# a class for defining the config variables
class Config:
    def __init__(self, path=".env", gpt_model="gpt-3.5-turbo"):
        self.path = path
        self.GPT_MODEL = gpt_model
        self.API_KEY = os.getenv("OPENAI_API_KEY")
        self.DALL_E_API_KEY = os.getenv("DALL_E_API_KEY")
        self.current_key = 0

    def next_key(self):
        self.API_KEY = self.keys[self.current_key]
        self.DALL_E_API_KEY = self.keys[self.current_key]
        if self.current_key + 1 >= len(self.keys):
            self.current_key = 0
        else:
            self.current_key += 1

    def set_keys(self, keys: list[str]):
        self.keys = keys


global __config
__config: Config = None


def get_config() -> Config:
    global __config
    if __config is None:
        __config = Config()
    return __config
