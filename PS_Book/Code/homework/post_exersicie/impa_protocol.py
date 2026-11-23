import imaplib

IMAP4_SERVER = "pi-server.local"
PORT = 3143
PORT_SSL = 3990
USER_NAME = "admin"
PASS = 'admin'

def read_imap_email():
    mailbox = imaplib.IMAP4(IMAP4_SERVER, PORT)
    mailbox.login(USER_NAME, PASS)
    print("Logowanie do poczty")
    mailbox.select('inbox')
    result, data = mailbox.search(None, "ALL")
    print(f"mail {result} data: {data}")

    mailbox.logout()

if __name__=="__main__":
    read_imap_email()
