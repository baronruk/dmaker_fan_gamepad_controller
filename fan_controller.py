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
        print(f"Power: {self.status().power.upper()}")

    def toggle_buzzer(self):
        if self.status().buzzer:
            self.set_buzzer(False)
        else:
            self.set_buzzer(True)
        print(f"Buzzer: {_convert_bool(self.status().buzzer)}")

    def toggle_child_lock(self):
        if self.status().child_lock:
            self.set_child_lock(False)
        else:
            self.set_child_lock(True)
        print(f"Child lock: {_convert_bool(self.status().child_lock)}")

    @power_required
    def toggle_led_indicators(self):
        if self.status().led:
            self.set_led(False)
        else:
            self.set_led(True)
        print(f"LED indicators: {_convert_bool(self.status().led)}")

    @power_required
    def toggle_oscillation(self):
        if self.status().oscillate:
            self.set_oscillate(False)
        else:
            self.set_oscillate(True)
        print(f"Oscillation: {_convert_bool(self.status().oscillate)}")

    @power_required
    def decrease_speed(self):
        current_speed = self.status().speed

        if current_speed > 1:
            self.set_speed(current_speed - 1)
            print(f"Speed decreased. Current speed: {self.status().speed}")
        else:
            print(f"Minimum speed reached. Current speed: {current_speed}")

    @power_required
    def increase_speed(self):
        current_speed = self.status().speed

        if current_speed < 100:
            self.set_speed(current_speed + 1)
            print(f"Speed increased. Current speed: {self.status().speed}")
        else:
            print(f"Maximum speed reached. Current speed: {current_speed}")

    @power_required
    def rotate_left(self):
        if self.status().oscillate:
            print("Cannot rotate while oscillation is ON")
        else:
            self.set_rotate(MoveDirection.Left)
            print("Rotated to the left.")

    @power_required
    def rotate_right(self):
        if self.status().oscillate:
            print("Cannot rotate while oscillation is ON")
        else:
            self.set_rotate(MoveDirection.Right)
            print("Rotated to the right.")

    def print_status(self):
        status = self.status()
        print(
            "\nDevice status\n"
            f"Power: {status.power.upper()}\n"
            f"Operation mode: {status.mode.value.upper()}\n"
            f"Speed: {status.speed}\n"
            f"Oscillation: {_convert_bool(status.oscillate)}\n"
            f"Angle: {status.angle}\n"
            f"LED: {_convert_bool(status.led)}\n"
            f"Buzzer: {_convert_bool(status.buzzer)}\n"
            f"Child lock: {_convert_bool(status.child_lock)}\n"
            f"Power-off time (minutes): {status.delay_off_countdown or 'UNSET'}\n",
        )

    @power_required
    def increase_angle(self):
        if not self.status().oscillate:
            print("Cannot adjust the angle while oscillation is OFF")
            return

        supported_angles = SUPPORTED_ANGLES[self.model]
        current_angle_index = supported_angles.index(self.status().angle)

        if current_angle_index + 1 >= len(supported_angles):
            print(
                f"Maximum angle reached. Current angle: {supported_angles[current_angle_index]}"
            )
            return

        new_angle = supported_angles[current_angle_index + 1]
        self.set_angle(new_angle)
        print(f"Angle increased. Current angle: {new_angle}")

    @power_required
    def decrease_angle(self):
        if not self.status().oscillate:
            print("Cannot adjust the angle while oscillation is OFF")
            return

        supported_angles = SUPPORTED_ANGLES[self.model]
        current_angle_index = supported_angles.index(self.status().angle)

        if current_angle_index - 1 < 0:
            print(
                f"Minimum angle reached. Current angle: {supported_angles[current_angle_index]}"
            )
            return

        new_angle = supported_angles[current_angle_index - 1]
        self.set_angle(new_angle)
        print(f"Angle increased. Current angle {new_angle}")

    @power_required
    def toggle_mode(self):
        current_mode = self.status().mode
        current_mode_index = self.operation_modes.index(current_mode.value)

        next_mode_index = (current_mode_index + 1) % len(self.operation_modes)
        next_mode_str = self.operation_modes[next_mode_index]
        next_mode = OperationModeMiot[next_mode_str.capitalize()]

        self.set_mode(next_mode)
        print(
            f"Previous mode: {current_mode.name.upper()}"
            " --> "
            f"Switched to: {self.status().mode.value.upper()}"
        )
