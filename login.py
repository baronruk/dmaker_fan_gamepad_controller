import getpass
import os
import sys

import toml
from micloud import MiCloud
from micloud.micloudexception import MiCloudAccessDenied

# define the path to the configuration file
CONFIG_FILE = "config.toml"


def _load_credentials():
    # function to load credentials from configuration TOML file

    username = None
    password = None

    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, "r") as file:
            config = toml.load(file)
            username = config.get("credentials", {}).get("username")
            password = config.get("credentials", {}).get("password")

    return username, password


def micloud_login():
    saved_credentials = True
    # load credentials
    username, password = _load_credentials()

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

    # log in to MiCloud and retrieve the device list
    mc = MiCloud(username, password)
    try:
        login_success = mc.login()
    except MiCloudAccessDenied:
        print("Access denied. Did you set the correct username and/or password?")
        sys.exit(0)

    # write credentials to the TOML file only if login was successful
    if login_success and not saved_credentials:
        with open(CONFIG_FILE, "w") as file:
            toml.dump(
                {"credentials": {"username": username, "password": password}}, file
            )

    return mc or None
