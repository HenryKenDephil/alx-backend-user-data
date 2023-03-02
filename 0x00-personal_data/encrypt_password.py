#!/usr/bin/env python3
'''password encryption'''

import bcrypt

def hash_password(password: str) -> bytes:
    '''expects a single string argument named password
    returns a salted, hashed password
    which is a byte string'''

    encoded_psw = bytes(password, 'utf-8')
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(encoded_psw, salt)
    return hashed


def is_valid(hashed_password: bytes, password: str)  -> bool:
    '''implement an is_valid function that expects 2 argumemnts
    and returns a boolean
    
    Args:
        hashed_password: bytes type
        password: str type
        use bbcrypt tom validate that the provided password
        matches the hashed password'''
    
    encoded_psw = bytes(password, 'utf-8')
    if bcrypt.checkpw(encoded_psw, hashed_password) is True:
        return True
    return False
