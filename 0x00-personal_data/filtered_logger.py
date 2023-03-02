#!/usr/bin/env python3
'''module that filters personal information and logs'''

import re
from typing import List
import logging
import mysql.connector
from os import getenv


PII_FIELDS = ('name', 'email', 'phone', 'ssn', 'password')


def filter_datum(fields: List[str], redaction: str, message: str,
                separator: str) -> str:
    '''
    function that returns the log message obfuscated
    function should use regex to replace occurences of certain field values
    use re.sub to perform substitution with single regex
    Args:
        fields: a list of strings representing all fields to obfuscate
        redaction: a string representingby what the field will be obfuscated
        message: a string representing the log line
        sepeartor: a string representing by which character is seperating all fields
                    in the log line
    Returns:
        returns the log message obfuscated
    '''
    for field in fields:
        message = re.sub(field + "=.*?" + separator,
                            field + "=" + redaction + separator, 
                            message)
    return message


class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class
        """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self):

        '''constructor method'''
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        '''function that filters values by filter_datum'''
        return filter_datum(self.fields, self.REDACTION,
                            super(RedactingFormatter, self).format(record),
                            self.SEPARATOR)

def get_logger() -> logging.Logger:
    '''logger function that returns logging.Logger  object'''

    log  = logging.getLogger('user_data')
    log.setLevel(logging.INFO)
    log.propagate = False

    sh = logging.StreamHandler()
    formatter = RedactingFormatter()
    sh.setFormatter(formatter)
    log.addHandler(sh)

    return log

def get_db()  -> mysql.connector.connection.MYSQLConnection:
    '''function that manages database connection via environment variables
    it prevents adding  databse credentials in the code base'''
    
    connection_db = mysql.connector.connection.MYSQLConnection(
        user = getenv('PERSONAL_DATA_DB_USERNAME', 'root'),
        password = getenv('PERSONAL_DATA_DB_PASSWORD', ''),
        host = getenv('PERSONAL_DATA_DB_HOST', 'localhost'),
        database = getenv('PERSONAL_DATA_DB_NAME',)
    )

    return connection_db

def main():
    '''function that retrieve all rows in the user tabl;e
    and displays each row as a filtered format'''

    database = get_db()
    db_cursor = database.cursor()
    db_cursor.execute("SELECT * FROM users;")
    fields = [i[0] for i in db_cursor.description()]

    log = get_logger()

    for row in db_cursor:
        string_row = '' . join(f'{f}={str(r)}; for r, f in zip(row, fields')
        log.info(string_row.strip())

        db_cursor.close()
        database.close()

if __name__ == '__main__':
    main()
