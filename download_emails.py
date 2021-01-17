import imaplib
import email
import os
from email.generator import Generator
from credentials import login, password


def connect(login, password):
    imap = imaplib.IMAP4_SSL('imap.gmail.com')
    imap.login(login, password)
    return imap


def disconnect(imap):
    imap.logout()


if __name__ == '__main__':
    imap = connect(login, password)
    imap.select(mailbox='"[Gmail]/Sent Mail"', readonly=True)
    resp, items = imap.search(None, 'All')
    sent_item_list = items[0].split()
    counter = 1
    save_path = os.path.join(os.getcwd(), "emails", "sent_emails")
    try:
        os.makedirs(save_path)
    except FileExistsError:
        pass

    for item in sent_item_list:
        resp, data = imap.fetch(item, "(RFC822)")
        raw_email = data[0][1]
        email_message = email.message_from_bytes(raw_email)
        ext = '.elm'
        filename = 'msg-part-{}{}'.format(counter, ext)
        counter += 1
        with open(os.path.join(save_path, filename), "w") as out:
            gen = Generator(out)
            gen.flatten(email_message)

    disconnect(imap)
    print('Finished copying {} emails to {} folder.'.format(len(sent_item_list), save_path))
