import getpass
import os
import sys

import toml
from micloud import MiCloud
from micloud.micloudexception import MiCloudAccessDenied

from password_cipher import PasswordCipher

# define the path to the configuration file
CONFIG_FILE = "config.toml"


def _load_credentials(password_cipher):
    # function to load credentials from configuration TOML file

    username = None
    password = None

    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, "r") as file:
            config = toml.load(file)
            username = config.get("credentials", {}).get("username")
            password = config.get("credentials", {}).get("password")

            # decrypt password if it is not None
            if password:
                try:
                    password = password_cipher.decrypt_password(password)
                except Exception:
                    # if decryption fails, encrypt the password
                    password = password_cipher.encrypt_password(password)
                    _save_credentials(username, password, password_cipher)
                    password = password_cipher.decrypt_password(password)

    return username, password


def _save_credentials(username, password, password_cipher):
    # function to save credentials to configuration TOML file

    config = {}

    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, "r") as file:
            config = toml.load(file)

    # encrypt the password before saving
    encrypted_password = password_cipher.encrypt_password(password)

    # update credentials in the config dictionary
    config.setdefault("credentials", {})["username"] = username
    config.setdefault("credentials", {})["password"] = encrypted_password

    # write updated config back to the file
    with open(CONFIG_FILE, "w") as file:
        toml.dump(config, file)


def micloud_login():
    saved_credentials = True
    password_cipher = PasswordCipher()

    # load credentials
    username, password = _load_credentials(password_cipher)

    # check if credentials are empty and prompt user if necessary
    if not username or not password:
        print(
            "Username or password not found in TOML file. Please enter your MiCloud credentials."
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
        _save_credentials(username, password, password_cipher)

    return mc if login_success else None
