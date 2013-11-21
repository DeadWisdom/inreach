import imaplib

def verify(account):
    client = imaplib.IMAP4_SSL(account.address, account.port)
    