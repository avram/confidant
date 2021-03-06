from cryptography.fernet import Fernet

from confidant import app
from confidant import log


class CipherManager:
    '''
    Class for encrypting and decrypting strings.

    cipher = CipherManager(key)
    encrypted_text = cipher.encrypt('hello world')
    decrypted_text = cipher.decrypt(encrypted_text)
    '''
    def __init__(self, key, version=2):
        self.key = key
        self.version = version

    def encrypt(self, raw):
        # Disabled encryption is dangerous, so we don't use falsiness here.
        if app.config['USE_ENCRYPTION'] is False:
            log.warning('Not using encryption in CipherManager.encrypt'
                        ' If you are not running in a development or test'
                        ' environment, this should not be happening!')
            return raw
        if self.version == 2:
            f = Fernet(self.key)
            return f.encrypt(raw.encode('utf-8'))
        else:
            raise CipherManagerError('Bad cipher version')

    def decrypt(self, enc):
        # Disabled encryption is dangerous, so we don't use falsiness here.
        if app.config['USE_ENCRYPTION'] is False:
            log.warning('Not using encryption in CipherManager.decrypt'
                        ' If you are not running in a development or test'
                        ' environment, this should not be happening!')
            return enc
        if self.version == 2:
            f = Fernet(self.key)
            return f.decrypt(enc.encode('utf-8'))
        else:
            raise CipherManagerError('Bad cipher version')


class CipherManagerError(Exception):
    pass
