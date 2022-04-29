import rsa
from Crypto.Cipher import AES
from typing import *
from ast import literal_eval as make_tuple

from utils import Socket_Manager, ReqManager
from header import Header
from requests import *
import config
from message import Msg

#####################################
#              Classes              #
#####################################
class EncryptionManager:
    def __init__(self):
        pbk, prk = rsa.newkeys(128)
        self.key = b'Sixteen byte key'
        self.connectionKey = None
        self.cipher = AES.new(self.key, AES.MODE_EAX)
        self.localNonce = self.cipher.nonce
        self.connectionNonce = None
        self.publicKey = pbk
        print("original key", self.publicKey)
        self.privateKey = prk
        self.connectionPublicKey = None
        self.connectionClientReceivedPublicKey = None

    def set_connection_key(self, n):
        print("set connection key")
        self.connectionKey = AES.new(self.key, AES.MODE_EAX, nonce=n)

    def exchange_keys(self, socket:Socket_Manager):
        rm = ReqManager(socket)
        head = Header()
        head.set_mt(Types.exchangeKey.value)
        try:
            # SHOULD encode the key, but does it actually!
            #key = rsa.PublicKey.save_pkcs1(self.publicKey)
            key = str(self.localNonce).encode()
            res:Msg = rm.newReq(create_req(head, key), config.ConnectionAddress)
            print("client received key, ", res.message)
            self.connectionClientReceivedPublicKey = rsa.PublicKey.load_pkcs1(res.message)
        except Exception as e:
            print(e)
            return

    def set_connectionPublicKey(self, key:int):
        self.connectionPublicKey = key

    def encrypt_message(self, m:bytes, key) -> Tuple:
        print("encrypting message ", m, " len ", len(m))
        print("key ", key)
        return self.cipher.encrypt_and_digest(m)
        #return rsa.encrypt(m, key)

    def decrypt_message(self, m:bytes):
        return rsa.decrypt(m, self.privateKey)