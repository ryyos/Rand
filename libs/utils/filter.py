def filter_invalid_chars(name):
    invalid_chars = ['/', '\\', ':', '*', '?', '"', '<', '>', '|', '+', '=', '&', '%', '@', '#', '$', '^', '[', ']', '{', '}', '`', '~']
    falid = ''.join(char if char not in invalid_chars else '' for char in name)
    
    return falid