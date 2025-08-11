def my_function(x: int | None):  # Allow None
    if x is None:
        return int(x)
    return x
