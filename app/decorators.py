from functools import wraps


def power_required(func):
    @wraps(func)
    def wrapper(self, *args, **kwargs):
        if not self.status().is_on:
            print(f"Action '{func.__name__}' requires power to be ON. Power is OFF.")
            return
        return func(self, *args, **kwargs)

    return wrapper
