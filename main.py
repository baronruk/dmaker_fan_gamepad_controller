import sys
import time

import pygame

from device_manager import parse_device_list, select_device
from fan_controller import FanController
from login import micloud_login

# initialize pygame
pygame.init()
pygame.joystick.init()


def _initialize_joystick():
    """
    Initializes the first connected joystick if available.
    """
    if pygame.joystick.get_count() > 0:
        # get the first joystick
        joystick = pygame.joystick.Joystick(0)
        joystick.init()

        print(f" => Gamepad initialized: {joystick.get_name()}")

        return joystick
    else:
        print(" => No gamepad connected.")

        return None


# login to MiCloud and retrieve the list of online devices
session = micloud_login()
device_list = session.get_devices()

# parse the device list and select device
parsed_device_list = parse_device_list(device_list)
selected_device = select_device(parsed_device_list)

# retrieve the IP address and token for the selected device
IP_ADDRESS = selected_device["localip"]
TOKEN = selected_device["token"]

# initialize FanController
fan = FanController(ip=IP_ADDRESS, token=TOKEN)
# initialize gamepad
joystick = _initialize_joystick()

running = True
while running:
    if not pygame.joystick.get_count() and joystick is not None:
        # gamepad was disconnected
        print(" => Gamepad disconnected.")
        joystick = None

    if pygame.joystick.get_count() and joystick is None:
        # gamepad was reconnected
        joystick = _initialize_joystick()

    else:
        for event in pygame.event.get():
            if event.type == pygame.JOYBUTTONDOWN:
                button = event.button

                print(f" => Gamepad button: {button}")

                if button == 0:  # A
                    fan.toggle_buzzer()
                elif button == 1:  # B
                    fan.toggle_child_lock()
                elif button == 2:  # X
                    fan.toggle_mode()
                elif button == 3:  # Y
                    fan.toggle_led_indicators()
                elif button == 4:  # LB
                    fan.rotate_left()
                elif button == 5:  # RB
                    fan.rotate_right()
                elif button == 6:  # BACK
                    fan.print_status()
                elif button == 7:  # START
                    fan.toggle_power()
                elif button == 8:  # Xbox
                    print("Exiting...")
                    running = False
                elif button == 10:  # right analog
                    fan.toggle_oscillation()
                elif button == 11:  # D-PAD left
                    fan.decrease_angle()
                elif button == 12:  # D-PAD right
                    fan.increase_angle()
                elif button == 13:  # D-PAD up
                    fan.increase_speed()
                elif button == 14:  # D-PAD down
                    fan.decrease_speed()

            elif event.type == pygame.JOYAXISMOTION:
                axis = event.axis
                value = event.value

                print(f" => Gamepad axis {axis} moved to {value:.2f}")

                if axis == 3:
                    if value <= -1:
                        fan.rotate_left()
                    elif value >= 1:
                        fan.rotate_right()
    # pause briefly to avoid high CPU usage
    time.sleep(0.1)

# quit Pygame and exit
pygame.quit()
sys.exit(0)
