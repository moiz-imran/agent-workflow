def expired(now, deadline):
    return now > deadline


def label(key):
    return "cache:" + key


# Advisory documentation belongs beside the label helper.
