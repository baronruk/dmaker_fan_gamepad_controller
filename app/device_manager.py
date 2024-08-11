import json

from .auth.login import Authenticator


def parse_device_list(devices):
    """
    Function to parse and reformat the device list, including only online devices
    """
    parsed_devices = []

    for device in devices:
        if device.get("isOnline"):
            name = device.get("name")
            localip = device.get("localip")
            token = device.get("token")
            parsed_devices.append({"name": name, "localip": localip, "token": token})

    return parsed_devices


def select_device(device_list):
    """
    Display the menu with device names and index numbers then prompt the user to select a device
    """
    selected_device = None

    while not selected_device:
        try:
            print("\nCurrectly online devices:\n")
            for index, device in enumerate(device_list):
                print(f"{index + 1}. {device['name']}")

            selected_index = (
                int(input("\nSelect a device by entering the index number: ")) - 1
            )

            # get the selected device
            selected_device = device_list[selected_index]
        except ValueError:
            print("\nInvalid index number. Please select a valid index number.")
        except IndexError:
            print("\nIndex out of range. Please select a valid index number.")

    return selected_device


def _find_device_by_token(device_list, token):
    for device in device_list:
        if device.get("token") == token:
            return device
    return None


def list_devices():
    session = Authenticator().login()
    device_list = session.get_devices()

    # parse the device list
    parsed_device_list = parse_device_list(device_list)
    selected_device = select_device(parsed_device_list)

    # find the selected device in the original device list
    full_device_info = _find_device_by_token(device_list, selected_device.get("token"))

    # print the full information of the selected device
    print("\nSelected Device Full Information:")
    print(f"\n{json.dumps(full_device_info, indent=4, sort_keys=True)}")
