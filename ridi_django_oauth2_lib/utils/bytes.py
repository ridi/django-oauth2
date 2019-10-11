def bytes_to_int(by):
    result = 0
    for b in by:
        result = result * 256 + int(b)
    return result
