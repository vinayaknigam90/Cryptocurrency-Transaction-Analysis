#!/usr/bin/env python
from hashlib import *
from base58 import *

def SHA256D(bstr):
    return sha256(sha256(bstr).digest()).digest()

def ConvertPKHToAddress(prefix, addr):
    data = prefix + addr
    return b58encode(data + SHA256D(data)[:4])

def PubkeyToAddress(pubkey_hex):
    pubkey = bytearray.fromhex(pubkey_hex)
    round1 = sha256(pubkey).digest()
    h = new('ripemd160')
    h.update(round1)
    pubkey_hash = h.digest()
    return ConvertPKHToAddress(b'\x00', pubkey_hash)

