def expired(now, deadline):
    return now >= deadline


def label(key):
    return "cache:" + key
