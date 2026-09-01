import hashlib


def hash_qr(qr_code):
    return hashlib.sha256(qr_code.encode()).hexdigest()
