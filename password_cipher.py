import base64
import os

from cryptography.fernet import Fernet

# define the path to the key file
KEY_FILE = ".key"


class PasswordCipher:
    def __init__(self, key_file=KEY_FILE):
        self.key_file = key_file
        self.key = self._load_key()

    def _generate_key(self):
        """
        Generates a key and saves it to a file.
        """
        key = Fernet.generate_key()
        with open(self.key_file, "wb") as key_file:
            key_file.write(key)

    def _load_key(self):
        """
        Loads the key from the key file.
        """
        if not os.path.exists(self.key_file):
            self._generate_key()
        return open(self.key_file, "rb").read()

    def encrypt_password(self, password):
        """
        Encrypts the password using the key.
        """
        f = Fernet(self.key)
        encrypted_password = f.encrypt(password.encode())
        return base64.urlsafe_b64encode(encrypted_password).decode()

    def decrypt_password(self, encrypted_password):
        """
        Decrypts the password using the key.
        """
        f = Fernet(self.key)
        decrypted_password = f.decrypt(
            base64.urlsafe_b64decode(encrypted_password.encode())
        )
        return decrypted_password.decode()
