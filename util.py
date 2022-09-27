import uuid


def getuuid() -> int:
    return uuid.uuid1().int
