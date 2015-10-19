

def to_unicode(text):
    """
    convert to unicode
    """
    if isinstance(text, unicode):
        return text

    try:
        return text.decode("utf-8")
    except:
        return text.decode("utf-8", "ignore")

