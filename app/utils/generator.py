from hashlib import md5
import random


def md5string(o):
    return md5(o.encode()).hexdigest()


def random_token(length=10):
    return ''.join(
        (
            random.choice('ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789')
            for i in range(length)
        )
    )
