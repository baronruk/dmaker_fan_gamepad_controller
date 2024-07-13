from functools import wraps

from colorama import Fore, Style


def power_required(func):
    @wraps(func)
    def wrapper(self, *args, **kwargs):
        if not self.status().is_on:
            print(
                f"{Fore.RED}Action '{func.__name__}' requires power to be ON. "
                f"{Style.BRIGHT}Power is OFF.{Style.RESET_ALL}"
            )
            return
        return func(self, *args, **kwargs)

    return wrapper
