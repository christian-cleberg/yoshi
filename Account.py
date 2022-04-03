import database


class Account:
    def __init__(self, uuid: str, application: str, username: str,
                 password: str, url: str) -> None:
        self.uuid = uuid
        self.application = application
        self.username = username
        self.password = password
        self.url = url

    def display_account(self) -> None:
        print('ID:', self.uuid)
        print('Application:', self.application)
        print('Username:', self.username)
        print('Password:', self.password)
        print('URL:', self.url)

    def save_account(self) -> None:
        database.create_account(
            self.uuid, self.application, self.username, self.password, self.url)

    def delete_account(self) -> bool:
        database.delete_account(self.uuid)
        return True
