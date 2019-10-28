from base64 import b64encode, b64decode

from Crypto.Cipher import AES, PKCS1_OAEP
from Crypto.Hash import SHA256
from Crypto.PublicKey import RSA


class SymmetricCipher(object):
    """
    Class creates logic, that let use
    symmetric ciphers, based on AES.
    """

    def __init__(self, key):
        self.key = b64decode(key)
        self.cipher, self.nonce = None, None

    def _init_cipher(self, nonce=None):
        self.cipher = AES.new(self.key, AES.MODE_EAX, nonce)
        self.nonce = self.cipher.nonce

    def encrypt(self, binary_message):
        """
        Crypt your binary message.
        """

        self._init_cipher()
        ciphertext = self.cipher.encrypt(binary_message)
        return self.nonce + ciphertext

    def decrypt(self, binary_message):
        """
        Return your cripted message as a decrypted binary data.
        """

        nonce, ciphertext = binary_message[:16], binary_message[16:]
        self._init_cipher(nonce)

        return self.cipher.decrypt(ciphertext)


class AsymmetricCipher(object):
    """
    Class used for trasnport session key:
    session key = get_random_bytes(32)
    """

    RSA_LENGTH = 2048

    def __init__(self, public_key=None):
        self._public_key = None
        self.cipher = None

        if public_key:
            self._public_key = RSA.import_key(public_key)
            self.cipher = PKCS1_OAEP.new(self._public_key)
        else:
            key = RSA.generate(self.RSA_LENGTH)

            self._public_key = key.publickey().export_key(format="PEM")
            self.cipher = PKCS1_OAEP.new(key=key)

    @property
    def public_key(self):
        return self._public_key

    def encrypt(self, binary_message):
        """
        Crypt binary data with public key.
        """

        msg = self.cipher.encrypt(binary_message)
        return b64encode(msg)

    def decrypt(self, binary_message):
        """
        Decrypt binary data with public key.
        """

        value = b64decode(binary_message)
        return self.cipher.decrypt(value)


def get_text_digest(text, salt=""):
    """
    Return text digest combined with salt value.
    Uses SHA-256 algorithm.
    """

    h = SHA256.new()
    h.update(f"{text}{salt}".encode())
    return h.hexdigest()
