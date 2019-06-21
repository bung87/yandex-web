import smtplib
import time
import imaplib
import email
import re
import sys
import os

class InboxIsEmpty(Exception):
    pass

def simple_extract_server(address):
    id,host = address.split("@")
    return "imap." + host

def get_yandex_verification_code(address,password):
    mail = imaplib.IMAP4_SSL(simple_extract_server(address))
    mail.login(address,password)
    mail.select('inbox')
    typ, data = mail.search(None, 'ALL')
    mail_ids = data[0]
    id_list = mail_ids.split()
    if len(id_list) == 0:
        raise InboxIsEmpty()
    first_email_id = int(id_list[0])
    latest_email_id = int(id_list[-1])
    code = None
    for i in range(latest_email_id,first_email_id, -1):
        typ, data = mail.fetch( str(i), "(RFC822)" )
        raw_email = data[0][1]
        mail_content = raw_email.decode('utf-8',errors="ignore")
        email_message = email.message_from_string(mail_content)
        if email_message["from"].find("verify@yandex.com") != -1:
            matched = re.search("Please enter this verification code to get started on Twitter:\s*(?:<[^>]+>)*(\w+)", str(email_message))
            if matched:
                code = matched.group(1)
                break
    return code
                
if __name__ == "__main__":
    if len(sys.argv) > 1:
        url = get_yandex_verification_code(sys.argv[1],sys.argv[2])
    else:
        url = get_yandex_verification_code(os.environ["EMAIL"],os.environ["PASS"])
    print(url)