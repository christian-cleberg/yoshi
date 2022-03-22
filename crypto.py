from cryptography.fernet import Fernet

vault_file = 'vault.sqlite'


def generate_key() -> bytes:
    new_key = Fernet.generate_key()
    return new_key


def load_key(key_file: str) -> bytes:
    return open(key_file, 'rb').read()


def encrypt(key, filename=vault_file) -> None:
    f = Fernet(key)
    with open(filename, 'rb') as file:
        file_data = file.read()
    encrypted_data = f.encrypt(file_data)
    with open(filename, 'wb') as file:
        file.write(encrypted_data)


def decrypt(key, filename=vault_file) -> None:
    f = Fernet(key)
    with open(filename, 'rb') as file:
        encrypted_data = file.read()
    decrypted_data = f.decrypt(encrypted_data)
    with open(filename, 'wb') as file:
        file.write(decrypted_data)
