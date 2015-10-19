import m2secret
import hashlib

PASSW = 'SOMMELIER_APP'


def encrypt_userid(userid):
    """
    Encrypt userid to construct the URL for each user.
    """
    secret = m2secret.Secret()
    secret.encrypt(userid, PASSW)
    serialized = secret.serialize()
    return serialized


def decrypt_userid(encrypted_userid):
    """
    Helps to extract the userid from the URLs.
    """
    secret = m2secret.Secret()
    secret.deserialize(encrypted_userid)
    userid = secret.decrypt(PASSW)   
    return userid


def convert_to_md5(text):
    """
    convert to md5

    Input:
        text - unicode/str

    Output:
        unicode
    """
    m = hashlib.md5()
    m.update(text)
    return unicode(m.hexdigest())
