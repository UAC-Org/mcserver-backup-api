"""
Token management API.
"""

import random
import string
from os import makedirs, path, remove, stat, utime
from time import time


def touch(filepath: str) -> None:
    """
    Touch a file.
    """
    if not path.isfile(filepath):
        open(filepath, "w").close()
    else:
        ts = stat(filepath).st_atime
        utime(filepath, (ts, time()))


def generate_token(length: int = 32) -> str:
    """
    Generate a random token.
    """
    return "".join(
        random.choice(string.ascii_letters + string.digits) for _ in range(length)
    )


def update_token(token: str) -> None:
    """
    Update a token in filesystem.

    Structure of the token files:
        token/
            token1...
            token2...
            ...
    """
    token_dir = path.join(path.dirname(__file__), "token")
    if not path.isdir(token_dir):
        makedirs(token_dir)
    touch(path.join(token_dir, token))


def get_token(token: str) -> bool:
    """
    Check if a token is valid.
    """
    token_dir = path.join(path.dirname(__file__), "token")
    if path.isfile(path.join(token_dir, token)):
        # check token if used recently (5 minutes)
        if path.getmtime(path.join(token_dir, token)) < time() - 300:
            return True
    return False


def remove_token(token: str) -> None:
    """
    Remove a token from filesystem.
    """
    token_dir = path.join(path.dirname(__file__), "token")
    if path.isfile(path.join(token_dir, token)):
        remove(path.join(token_dir, token))
    else:
        raise FileNotFoundError(f"Token {token} not found.")
