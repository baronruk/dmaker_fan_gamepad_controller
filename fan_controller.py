from colorama import Fore, Style
from miio import FanMiot
from miio.fan_common import MoveDirection
from miio.integrations.fan.dmaker.fan_miot import SUPPORTED_ANGLES, OperationModeMiot

from decorators import power_required


def _convert_bool(boolean):
    return "ON" if boolean else "OFF"


class FanController(FanMiot):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.operation_modes = [mode.name.lower() for mode in OperationModeMiot]
        self.print_status()

    def toggle_power(self):
        if self.status().is_on:
            self.off()
        else:
            self.on()
        print(
            f"{Fore.GREEN}Power: {Style.BRIGHT}{self.status().power.upper()}"
            f"{Style.RESET_ALL}"
        )

    def toggle_buzzer(self):
        if self.status().buzzer:
            self.set_buzzer(False)
        else:
            self.set_buzzer(True)
        print(
            f"{Fore.GREEN}Buzzer: {Style.BRIGHT}{_convert_bool(self.status().buzzer)}"
            f"{Style.RESET_ALL}"
        )

    def toggle_child_lock(self):
        if self.status().child_lock:
            self.set_child_lock(False)
        else:
            self.set_child_lock(True)
        print(
            f"{Fore.GREEN}Child lock: {Style.BRIGHT}{_convert_bool(self.status().child_lock)}"
            f"{Style.RESET_ALL}"
        )

    @power_required
    def toggle_led_indicators(self):
        if self.status().led:
            self.set_led(False)
        else:
            self.set_led(True)
        print(
            f"{Fore.GREEN}LED indicators: {Style.BRIGHT}{_convert_bool(self.status().led)}"
            f"{Style.RESET_ALL}"
        )

    @power_required
    def toggle_oscillation(self):
        if self.status().oscillate:
            self.set_oscillate(False)
        else:
            self.set_oscillate(True)
        print(
            f"{Fore.GREEN}Oscillation: {Style.BRIGHT}{_convert_bool(self.status().oscillate)}"
            f"{Style.RESET_ALL}"
        )

    @power_required
    def decrease_speed(self):
        current_speed = self.status().speed

        if current_speed > 1:
            self.set_speed(current_speed - 1)
            print(
                f"{Fore.GREEN}Speed decreased. {Style.BRIGHT}Current speed: {self.status().speed}"
                f"{Style.RESET_ALL}"
            )
        else:
            print(
                f"{Fore.YELLOW}Minimum speed reached."
                f"{Fore.GREEN}{Style.BRIGHT}Current speed: {current_speed}"
                f"{Style.RESET_ALL}"
            )

    @power_required
    def increase_speed(self):
        current_speed = self.status().speed

        if current_speed < 100:
            self.set_speed(current_speed + 1)
            print(
                f"{Fore.GREEN}Speed increased. {Style.BRIGHT}Current speed: {self.status().speed}"
                f"{Style.RESET_ALL}"
            )
        else:
            print(
                f"{Fore.YELLOW}Maximum speed reached."
                f"{Fore.GREEN}{Style.BRIGHT} Current speed: {current_speed}"
                f"{Style.RESET_ALL}"
            )

    @power_required
    def rotate_left(self):
        if self.status().oscillate:
            print(
                f"{Fore.RED}Cannot rotate while oscillation is {Style.BRIGHT}ON{Style.RESET_ALL}"
            )
        else:
            self.set_rotate(MoveDirection.Left)
            print(f"{Fore.GREEN}Rotated to the left.")

    @power_required
    def rotate_right(self):
        if self.status().oscillate:
            print(
                f"{Fore.RED}Cannot rotate while oscillation is {Style.BRIGHT}ON{Style.RESET_ALL}"
            )
        else:
            self.set_rotate(MoveDirection.Right)
            print(f"{Fore.GREEN}Rotated to the right.")

    def print_status(self):
        status = self.status()
        print(
            f"\n{Fore.BLUE}{Style.BRIGHT}Device status\n"
            f"{Style.RESET_ALL}"
            f"{Fore.GREEN}Power: {Style.BRIGHT}{status.power.upper()}\n"
            f"{Style.RESET_ALL}"
            f"{Fore.GREEN}Operation mode: {Style.BRIGHT}{status.mode.value.upper()}\n"
            f"{Style.RESET_ALL}"
            f"{Fore.GREEN}Speed: {Style.BRIGHT}{status.speed}\n"
            f"{Style.RESET_ALL}"
            f"{Fore.GREEN}Oscillation: {Style.BRIGHT}{_convert_bool(status.oscillate)}\n"
            f"{Style.RESET_ALL}"
            f"{Fore.GREEN}Angle: {Style.BRIGHT}{status.angle}\n"
            f"{Style.RESET_ALL}"
            f"{Fore.GREEN}LED: {Style.BRIGHT}{_convert_bool(status.led)}\n"
            f"{Style.RESET_ALL}"
            f"{Fore.GREEN}Buzzer: {Style.BRIGHT}{_convert_bool(status.buzzer)}\n"
            f"{Style.RESET_ALL}"
            f"{Fore.GREEN}Child lock: {Style.BRIGHT}{_convert_bool(status.child_lock)}\n"
            f"{Style.RESET_ALL}"
            f"{Fore.GREEN}Power-off time (minutes): "
            f"{Style.BRIGHT}{status.delay_off_countdown or 'UNSET'}\n"
            f"{Style.RESET_ALL}",
        )

    @power_required
    def increase_angle(self):
        if not self.status().oscillate:
            print(
                f"{Fore.RED}Cannot adjust the angle while oscillation is {Style.BRIGHT}OFF"
                f"{Style.RESET_ALL}"
            )
            return

        supported_angles = SUPPORTED_ANGLES[self.model]
        current_angle_index = supported_angles.index(self.status().angle)

        if current_angle_index + 1 >= len(supported_angles):
            print(
                f"{Fore.YELLOW}Maximum angle reached. "
                f"{Fore.GREEN}{Style.BRIGHT}Current angle: "
                f"{supported_angles[current_angle_index]}"
                f"{Style.RESET_ALL}"
            )
            return

        new_angle = supported_angles[current_angle_index + 1]
        self.set_angle(new_angle)
        print(
            f"{Fore.GREEN}Angle increased. {Style.BRIGHT}Current angle: {new_angle}"
            f"{Style.RESET_ALL}"
        )

    @power_required
    def decrease_angle(self):
        if not self.status().oscillate:
            print("Cannot adjust the angle while oscillation is OFF")
            return

        supported_angles = SUPPORTED_ANGLES[self.model]
        current_angle_index = supported_angles.index(self.status().angle)

        if current_angle_index - 1 < 0:
            print(
                f"{Fore.YELLOW}Minimum angle reached. "
                f"{Fore.GREEN}{Style.BRIGHT}Current angle: "
                f"{supported_angles[current_angle_index]}"
                f"{Style.RESET_ALL}"
            )
            return

        new_angle = supported_angles[current_angle_index - 1]
        self.set_angle(new_angle)
        print(
            f"{Fore.GREEN}Angle decreased. {Style.BRIGHT}Current angle: {new_angle}"
            f"{Style.RESET_ALL}"
        )

    @power_required
    def toggle_mode(self):
        current_mode = self.status().mode
        current_mode_index = self.operation_modes.index(current_mode.value)

        next_mode_index = (current_mode_index + 1) % len(self.operation_modes)
        next_mode_str = self.operation_modes[next_mode_index]
        next_mode = OperationModeMiot[next_mode_str.capitalize()]

        self.set_mode(next_mode)
        print(
            f"{Fore.RED}Previous mode: {Style.BRIGHT}{current_mode.name.upper()}"
            f"{Fore.RESET}{Style.RESET_ALL}"
            f" --> {Fore.GREEN}Switched to: {Style.BRIGHT}{self.status().mode.value.upper()}"
            f"{Style.RESET_ALL}"
        )
