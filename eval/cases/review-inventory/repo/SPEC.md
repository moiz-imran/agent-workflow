Reserve integer inventory atomically. Inputs are integers; remaining is nonnegative.
Amounts <= 0 raise ValueError. Insufficient stock returns (remaining, False).
Exact stock is allowed. Success returns (remaining - amount, True).
Decision point: reject an oversized reservation, never partially fulfill it.
