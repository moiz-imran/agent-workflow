def reserve(remaining, amount):
    if amount <= 0:
        raise ValueError("amount must be positive")
    if amount > remaining:
        return remaining, False
    return remaining - amount, True
