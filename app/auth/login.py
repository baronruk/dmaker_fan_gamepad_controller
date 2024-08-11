import getpass
import os
import sys

import toml
from micloud import MiCloud
from micloud.micloudexception import MiCloudAccessDenied

from ..helpers import get_absolute_path
from .password_cipher import PasswordCipher

# define the path to the configuration file
CONFIG_FILE = get_absolute_path("../../config.toml")


class Authenticator:
    def __init__(self, config_file=None):
        self.config_file = config_file or CONFIG_FILE
        self.password = None
        self.password_cipher = PasswordCipher()
        self.saved_credentials = True
        self.username = None

    def _load_credentials(self):
        # function to load credentials from configuration TOML file

        if os.path.exists(self.config_file):
            with open(self.config_file, "r") as file:
                config = toml.load(file)
                self.username = config.get("credentials", {}).get("username")
                self.password = config.get("credentials", {}).get("password")

                # decrypt password if it is not None
                if self.password:
                    try:
                        self.password = self.password_cipher.decrypt_password(
                            self.password
                        )
                    except Exception as exception:
                        print(f"Failed to decrypt the password: {exception}")
                        sys.exit(1)

    def _save_credentials(self):

        # function to save credentials to configuration TOML file
        config = {}

        if os.path.exists(self.config_file):
            with open(self.config_file, "r") as file:
                config = toml.load(file)

        # encrypt the password before saving
        encrypted_password = self.password_cipher.encrypt_password(self.password)

        # update credentials in the config dictionary
        config.setdefault("credentials", {})["username"] = self.username
        config.setdefault("credentials", {})["password"] = encrypted_password

        # write updated config back to the file
        with open(self.config_file, "w") as file:
            toml.dump(config, file)

    def prompt_for_credentials(self):
        # prompt the user for credentials
        if not self.username:
            self.username = input("Username: ")
        if not self.password:
            self.password = getpass.getpass("Password: ")
        self.saved_credentials = False

    def login(self):
        # load credentials
        self._load_credentials()

        # check if credentials are empty and prompt user if necessary
        if not self.username or not self.password:
            print(
                "Username and/or password? not found in TOML file. "
                "Please enter your MiCloud credentials."
            )
            self.prompt_for_credentials()

        # log in to MiCloud
        mc = MiCloud(self.username, self.password)
        try:
            login_success = mc.login()
        except MiCloudAccessDenied:
            print("Access denied. Did you set the correct username and/or password?")
            sys.exit(0)

        # write credentials to the TOML file only if login was successful
        if login_success and not self.saved_credentials:
            self._save_credentials()

        return mc if login_success else None
