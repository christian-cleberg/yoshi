# Import Python modules
import sqlite3
import sys
import os

# Specify the name of the vault database
vault_decrypted = 'vault.sqlite'
vault_encrypted = 'vault.sqlite.aes'


# Create the accounts table inside the vault database
def create_table() -> None:
    db_connection = sqlite3.connect(vault_decrypted)
    cursor = db_connection.cursor()
    cursor.execute(
        ''' CREATE TABLE accounts (uuid text, application text, username text, password text, url text) ''')
    db_connection.commit()
    db_connection.close()


# Check if the account table exists within the database
def table_check() -> bool:
    check = False
    db_connection = sqlite3.connect(vault_decrypted)
    cursor = db_connection.cursor()
    cursor.execute(
        ''' SELECT count(name) FROM sqlite_master WHERE type='table' AND name='accounts' ''')
    if cursor.fetchone()[0] != 1:
        user_choice = input(
            'Password vault does not exist. Would you like to create it now? (y/n): ')
        if user_choice == 'y' or user_choice == 'Y':
            create_table()
            check = True
        else:
            sys.exit('Program aborted upon user request.')
    else:
        check = True
    db_connection.commit()
    db_connection.close()
    return check


# Add a new account to the database
def create_account(uuid: str, application: str, username: str, password: str,
                   url: str) -> None:
    db_connection = sqlite3.connect(vault_decrypted)
    cursor = db_connection.cursor()
    cursor.execute(
        ''' INSERT INTO accounts VALUES (:uuid,:application,:username,:password,:url) ''',
        {'uuid': uuid, 'application': application, 'username': username,
         'password': password, 'url': url})
    db_connection.commit()
    db_connection.close()


# Delete an account with a specified UUID
def delete_account(uuid: str) -> None:
    db_connection = sqlite3.connect(vault_decrypted)
    cursor = db_connection.cursor()
    cursor.execute(
        ''' DELETE FROM accounts WHERE uuid = :uuid ''', {'uuid': uuid})
    db_connection.commit()
    db_connection.close()


# Find a specific account by UUID
def find_account(uuid: str) -> list:
    db_connection = sqlite3.connect(vault_decrypted)
    cursor = db_connection.cursor()
    cursor.execute(
        ''' SELECT * FROM accounts WHERE uuid = :uuid ''', {'uuid': uuid})
    account = cursor.fetchall()
    db_connection.close()
    return account


# Return all accounts found within the database table
# The `accounts` variable is a list of tuples
def find_accounts() -> list:
    db_connection = sqlite3.connect(vault_decrypted)
    cursor = db_connection.cursor()
    cursor.execute(''' SELECT * FROM accounts ''')
    accounts = cursor.fetchall()
    db_connection.close()
    return accounts


def update_account(field_name: str, new_value: str, uuid: str) -> None:
    queries = {
        'application': 'UPDATE accounts SET application = :new_value WHERE uuid = :uuid',
        'username': 'UPDATE accounts SET username = :new_value WHERE uuid = :uuid',
        'password': 'UPDATE accounts SET password = :new_value WHERE uuid = :uuid',
        'url': 'UPDATE accounts SET url = :new_value WHERE uuid = :uuid'
    }
    db_connection = sqlite3.connect(vault_decrypted)
    cursor = db_connection.cursor()
    cursor.execute(queries[field_name],
                   {'new_value': new_value, 'uuid': uuid})
    db_connection.commit()
    db_connection.close()


def purge_table() -> None:
    db_connection = sqlite3.connect(vault_decrypted)
    cursor = db_connection.cursor()
    cursor.execute(''' DROP TABLE accounts ''')
    db_connection.commit()
    db_connection.close()


def purge_database() -> None:
    os.remove(vault_decrypted)
