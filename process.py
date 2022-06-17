from Account import Account
import database
from string import ascii_letters, punctuation, digits
import random
import uuid
from prettytable import PrettyTable


# Generate a list of characters
def generate_characters(n: int) -> list:
    characters = list()
    password_format = ascii_letters + punctuation + digits
    for x in range(n):
        characters.append(random.choice(password_format))
    return characters


# Randomly shuffle the characters
def shuffle_characters(characters: list) -> str:
    random.shuffle(characters)
    character_string = ''.join(characters)
    return character_string


# Generate a combination of passphrases
def generate_passphrase(n: int, sep: str) -> str:
    phrases = []
    lucky_number = random.choice(range(0, n))
    for x in range(0, n):
        line = random.choice(open('wordlist.txt').readlines())
        line = line.replace('\n', '')
        if x == lucky_number:
            phrases.append(line.strip().capitalize() + str(x))
        else:
            phrases.append(line.strip().capitalize())
    passphrase = sep.join(phrases)
    return passphrase


# List all saved accounts
def list_accounts() -> None:
    accounts = database.find_accounts()
    t = PrettyTable(['UUID', 'Application', 'Username', 'Password', 'URL'])
    for account in accounts:
        t.add_row([account[0], account[1], account[2], account[3], account[4]])
    print(t)


# Delete a single account by UUID
def delete_account(uuid: str) -> None:
    account_record = database.find_account(uuid)
    account: Account = Account(account_record[0][0],
                               account_record[0][1],
                               account_record[0][2],
                               account_record[0][3],
                               account_record[0][4])
    if account.delete_account():
        print('Account successfully deleted.')


# Purge the `accounts` table and `vault.sqlite` file
def purge_accounts() -> None:
    check = input(
        'Are you absolutely sure you want to delete your password vault? This action is irreversible. (y/n): ')
    if check:
        database.purge_table()
        database.purge_database()
        print('The password vault has been purged. You may now exit or create a new one.')


# Request user input and create an account
def create_account() -> None:
    application_string = input('Please enter a name for this account: ')
    username_string = input('Please enter your username for this account: ')
    url_string = input('(Optional) Please enter a URL for this account: ')
    password_type = input(
        '''Do you want a random character password (p), an XKCD-style passphrase 
(x), or a custom password (c)? (p|x|c): ''')
    if password_type == "x" or password_type == "xkcd":
        password_length = int(
            input('Please enter number of words to include (min. 2): '))
        password_separator = input(
            'Please enter your desired separator symbol (_, -, ~, etc.: ')
        if password_length < 3:
            print('Error: Your passphrase length must be at least 3 words.')
        else:
            password_string = generate_passphrase(
                password_length, password_separator)
    elif password_type == "p":
        password_length = int(
            input('Please enter your desired password length (min. 8): '))
        if password_length < 8:
            print('Error: Your password length must be at least 8 characters.')
        else:
            password_characters = generate_characters(password_length)
            password_string = shuffle_characters(password_characters)
    else:
        password_string = input('Please enter your desired password: ')
    account = Account(str(uuid.uuid4()), application_string,
                      username_string, password_string, url_string)
    account.save_account()
    print('Account saved to the vault. Use `--list` to see all saved accounts.')


# Allow users to edit any account info except the UUID
def edit_account(uuid: str, edit_parameter: int) -> None:
    if edit_parameter == 1:
        field_name = 'application'
        new_value = input('Please enter your desired Application name: ')
    elif edit_parameter == 2:
        field_name = 'username'
        new_value = input('Please enter your desired username: ')
    elif edit_parameter == 3:
        field_name = 'password'
        type_check = input(
            'Do you want a new random password or to enter a custom password? (random/custom): ')
        if type_check == 'random':
            password_length = int(
                input('Please enter your desired password length: '))
            if password_length < 8:
                print('Error: Your password length must be at least 8 characters.')
            else:
                password_characters = generate_characters(password_length)
                new_value = shuffle_characters(password_characters)
        else:
            new_value = input('Please enter your desired password: ')
    elif edit_parameter == 4:
        field_name = 'url'
        new_value = input('Please enter your desired URL: ')
    database.update_account(field_name, new_value, uuid)
    print('Account successfully updated.')
