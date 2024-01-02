"""
Menghapus karakter tidak valid sebagai nama file atau folder.

Args:
  name (str): String yang akan difilter.

Returns:
  str: String hasil filter
"""
def filter_invalid_chars(name: str) -> str:
    invalid_chars = ['/', '\\', ':', '*', '?', '"', '<', '>', '|', '+', '=', '&', '%', '@', '#', '$', '^', '[', ']', '{', '}', '`', '~']
    falid = ''.join(char if char not in invalid_chars else '' for char in name)
    
    return falid.replace(" ", "_")