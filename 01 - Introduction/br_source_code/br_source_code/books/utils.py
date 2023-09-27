import hashlib

def hash_book_info(book_title, publisher_name):
    combined_info = f"{book_title}|{publisher_name}"
    combined_info_bytes = combined_info.encode('utf-8')
    sha_256_hash = hashlib.sha256(combined_info_bytes).hexdigest()
    return sha_256_hash