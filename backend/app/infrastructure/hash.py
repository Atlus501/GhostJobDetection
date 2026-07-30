import hashlib

def id_hash(text: str):
  return hashlib.sha256(text.encode()).hexdigest()