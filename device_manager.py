import pprint

from login import micloud_login


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
    print("\nCurrectly online devices:\n")
    for index, device in enumerate(device_list):
        print(f"{index}. {device['name']}")

    selected_index = int(input("\nSelect a device by entering the index number: "))
    # get the selected device
    selected_device = device_list[selected_index]

    return selected_device


def _find_device_by_token(device_list, token):
    for device in device_list:
        if device.get("token") == token:
            return device
    return None


if __name__ == "__main__":
    session = micloud_login()
    device_list = session.get_devices()

    # parse the device list
    parsed_device_list = parse_device_list(device_list)
    selected_device = select_device(parsed_device_list)

    # find the selected device in the original device list
    full_device_info = _find_device_by_token(device_list, selected_device.get("token"))

    # print the full information of the selected device
    print("\nSelected Device Full Information:")
    pp = pprint.PrettyPrinter(indent=4)
    pp.pprint(full_device_info)
