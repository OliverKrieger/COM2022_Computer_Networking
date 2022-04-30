import rsa
import config 

#####################################
#              Classes              #
#####################################
class EncryptionManager:
    def __init__(self):
        self.PublicKey, self.PrivateKey = rsa.newkeys(config.EncryptionBitSize) # 512 is bits, which is 64 bytes, but rsa encryption holds 11 bytes, meaning this becomes 11 
        self.ConnectionFromClientKey = None # will be null on the requesting client - set only for the server to respond to client
        self.ConnectionFromServerKey = None # will be null on the responding server - set only for the client to respond to server

    def set_cck(self, k:bytes): # standing for set_client_connection_key from key bytes
        self.ConnectionFromClientKey = rsa.PublicKey.load_pkcs1(k)

    def set_sck(self, k:bytes): # standing for set_server_connection_key from key bytes
        self.ConnectionFromServerKey = rsa.PublicKey.load_pkcs1(k)

    def export_public_key(self) -> bytes:
        return self.PublicKey.save_pkcs1()

    def encrypt_message(self, m:bytes, key:rsa.PublicKey) -> bytes:
        print("Encrypting Message with public key ", key)
        print("original message size ", len(m))
        enm:bytes = rsa.encrypt(m, key)
        print("Encrypted Message size ", len(enm))
        return enm

    def decrypt_message(self, m:bytes, key:rsa.PrivateKey) -> bytes:
        print("Decrypting Message with private key ", key)
        print("my public key is ", self.PublicKey)
        print("Encrypted message size ", len(m))
        print("Encrypted message ", m)
        dem = rsa.decrypt(m, key)
        print("Decrypted message size ", len(dem))
        print("Decrypted message ", dem)
        return dem