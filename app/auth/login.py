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
        self.password_cipher = PasswordCipher()

    def _load_credentials(self):
        # function to load credentials from configuration TOML file
        username = None
        password = None

        if os.path.exists(self.config_file):
            with open(self.config_file, "r") as file:
                config = toml.load(file)
                username = config.get("credentials", {}).get("username")
                password = config.get("credentials", {}).get("password")

                # decrypt password if it is not None
                if password:
                    try:
                        password = self.password_cipher.decrypt_password(password)
                    except Exception:
                        # if decryption fails, encrypt the password
                        password = self.password_cipher.encrypt_password(password)
                        self._save_credentials(username, password)
                        password = self.password_cipher.decrypt_password(password)

        return username, password

    def _save_credentials(self, username, password):
        # function to save credentials to configuration TOML file
        config = {}

        if os.path.exists(self.config_file):
            with open(self.config_file, "r") as file:
                config = toml.load(file)

        # encrypt the password before saving
        encrypted_password = self.password_cipher.encrypt_password(password)

        # update credentials in the config dictionary
        config.setdefault("credentials", {})["username"] = username
        config.setdefault("credentials", {})["password"] = encrypted_password

        # write updated config back to the file
        with open(self.config_file, "w") as file:
            toml.dump(config, file)

    def login(self):
        saved_credentials = True

        # load credentials
        username, password = self._load_credentials()

        # check if credentials are empty and prompt user if necessary
        if not username or not password:
            print(
                "Username or password not found in TOML file. \
                Please enter your MiCloud credentials."
            )

            if not username:
                username = input("Username: ")
            if not password:
                password = getpass.getpass("Password: ")
            saved_credentials = False

        # log in to MiCloud
        mc = MiCloud(username, password)
        try:
            login_success = mc.login()
        except MiCloudAccessDenied:
            print("Access denied. Did you set the correct username and/or password?")
            sys.exit(0)

        # write credentials to the TOML file only if login was successful
        if login_success and not saved_credentials:
            self._save_credentials(username, password)

        return mc if login_success else None
