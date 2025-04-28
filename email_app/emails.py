import get_token 
from poplib import POP3_SSL
import email
from email.header import decode_header
from imaplib import IMAP4_SSL
import credentials as cr
import base64 
import os     
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from email.mime.text import MIMEText
import mimetypes

tokenito = get_token.OAuthToken()
get_tokenito = tokenito.get_oauth_credentials()
TOKEN = get_tokenito.token

class EmailLogin:
    def __init__(self, username, protocol):
        self.username = str(username).strip()
        self.protocol = protocol.upper()
        self.mail = None

    def auth_string(self):
        return f'user={self.username}\1auth=Bearer {TOKEN}\1\1'.encode('utf-8')
    
    def auth_string_base64(self):
        auth_string = self.auth_string()
        return base64.b64encode(auth_string).decode('utf-8')

    def login(self):
        if self.protocol == "IMAP":
            self.mail = IMAP4_SSL("imap.gmail.com")
            self.mail.authenticate("XOAUTH2", lambda _: self.auth_string())
        elif self.protocol == "POP3":
            self.mail = POP3_SSL("pop.gmail.com")
            self.mail._shortcmd(f"AUTH XOAUTH2 {self.auth_string_base64()}")
        else:
            raise ValueError("Protocol must be 'IMAP' or 'POP3'")

    def close(self):
        if self.mail:
            if self.protocol == "IMAP":
                self.mail.logout()
            elif self.protocol == "POP3":
                self.mail.quit()

class EmailFetcher(EmailLogin):
    def __init__(self, username, protocol):
        super().__init__(username, protocol)

    def _fetch_email_message(self, message_id, criteria="(RFC822)"):
        try:
            result, msg_data = self.mail.fetch(message_id, criteria)
            if result != "OK":
                return False, None, None
            email_msg = email.message_from_bytes(msg_data[0][1])
            return True, email_msg, msg_data
        except Exception as e:
            print(f"Error fetching message {message_id}: {str(e)}")
            return False, None, None
        
    def fetch_emails_IMAP(self, limit=10):
        self.mail.select("inbox")
        result, data = self.mail.search(None, "ALL")
        email_ids = data[0].split()
        recent_email_ids = email_ids[-limit:]
        emails = []
        for email_id in recent_email_ids:
            success, msg, _ = self._fetch_email_message(email_id)
            if success:
                subject, encoding = decode_header(msg["Subject"])[0]
                if isinstance(subject, bytes):
                    subject = subject.decode(encoding if encoding else "utf-8")
                emails.append(subject)
        return emails
    
    def fetch_emails_POP3(self, limit=10):
        num_messages = len(self.mail.list()[1])
        emails = []
        for i in range(num_messages):
            msg = self.mail.retr(i + 1)
            msg_data = b"\n".join(msg[1])
            msg = email.message_from_bytes(msg_data)
            raw_subject = msg.get("Subject")
            if raw_subject:
                subject, encoding = decode_header(raw_subject)[0]
                if isinstance(subject, bytes):
                    subject = subject.decode(encoding if encoding else "utf-8")
                emails.append(subject)
            if len(emails) >= limit:
                break
        return emails

    def fetch_emails(self, limit=10):
        if self.protocol == "IMAP":
            return self.fetch_emails_IMAP(limit)
        elif self.protocol == "POP3":
            return self.fetch_emails_POP3(limit)
        else:
            raise ValueError("Protocol must be 'IMAP' or 'POP3'")

class EmailDownloader(EmailFetcher):
    def __init__(self, username, protocol):
        super().__init__(username, protocol)

    def create_download_folder(self):
        if not os.path.exists(cr.DOWNLOAD_FOLDER):
            os.makedirs(cr.DOWNLOAD_FOLDER)

    def fetch_unread_messages(self, mark_as_seen=False):
        emails = []
        self.mail.select("inbox")
        result, messages = self.mail.search(None, 'UnSeen')
        
        if result != "OK":
            print("Failed to retrieve emails.")
            return emails

        for message_id in messages[0].split():
            success, msg, _ = self._fetch_email_message(message_id)
            if success and msg and not isinstance(msg, str):
                emails.append((message_id, msg))  # save both ID and message
                if mark_as_seen:
                    self.mail.store(message_id, '+FLAGS', '\\Seen')
        return emails
    
    def save_attachment(self, msg):
        self.create_download_folder()
        att_path = "No attachment found."
        for part in msg.walk():
            if part.get_content_maintype() == 'multipart':
                continue
            if part.get('Content-Disposition') is None:
                continue

            filename = part.get_filename()
            if filename:
                att_path = os.path.join(cr.DOWNLOAD_FOLDER, filename)
                if not os.path.isfile(att_path):
                    with open(att_path, 'wb') as f:
                        f.write(part.get_payload(decode=True))
                    print(f"Saved attachment: {filename}")
        return att_path
    
    def save_email_to_txt(self, msg):
        self.create_download_folder()

        subject, encoding = decode_header(msg.get("Subject"))[0]
        if isinstance(subject, bytes):
            subject = subject.decode(encoding or "utf-8", errors="replace")

        body = ""

        parts = msg.walk() if msg.is_multipart() else [msg]
        for part in parts:
            if part.get_content_type() == "text/plain" and "attachment" not in str(part.get("Content-Disposition")):
                payload = part.get_payload(decode=True)
                charset = part.get_content_charset() or encoding or "utf-8"
                body = payload.decode(charset, errors="replace")
                break 

        filename = f"{subject}.txt"
        filepath = os.path.join(cr.DOWNLOAD_FOLDER, filename)
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(body)

        print(f"Saved email to: {filepath}")
        return filepath
    
    def download_email_attach(self, target_subject):
        unread_emails = self.fetch_unread_messages(mark_as_seen=False)

        for message_id, msg in unread_emails:
            subject, encoding = decode_header(msg.get("Subject"))[0]
            if isinstance(subject, bytes):
                subject = subject.decode(encoding if encoding else "utf-8")

            if subject.strip() == target_subject.strip():
                print(f"\033[33m Found matching unread email: {subject} \033[0m")

                attachment_path = self.save_attachment(msg)
                email_path = self.save_email_to_txt(msg)
                self.mail.store(message_id, '+FLAGS', '\\Seen')
                return attachment_path, email_path
        print("No unread email matching the subject was found.")
        return None

class EmailSender(EmailLogin):
    def __init__(self, username):
        super().__init__(username, protocol="SMTP") 

    def login(self):
        self.mail = smtplib.SMTP_SSL("smtp.gmail.com")
        self.mail.ehlo()
        self.mail.docmd('AUTH', 'XOAUTH2 ' + self.auth_string_base64())
        return True

    def send_email_txt(self, subject, body, to_email):
        msg = MIMEMultipart()
        msg['From'] = self.username
        msg['To'] = to_email
        msg['Subject'] = subject

        msg.attach(MIMEText(body, 'plain'))

        try:
            self.mail.sendmail(self.username, to_email, msg.as_string())
            print(f"Email sent to {to_email}")
            return True
        except Exception as e:
            print(f"Failed to send email: {str(e)}")
            return False

    def manage_attach(self, msg, attach_path):
        if attach_path:
            ctype, encoding = mimetypes.guess_type(attach_path)
            if ctype is None or encoding is not None:
                ctype = 'application/octet-stream'
            maintype, subtype = ctype.split('/', 1)

            with open(attach_path, 'rb') as f:
                part = MIMEBase(maintype, subtype)
                part.set_payload(f.read())
                encoders.encode_base64(part)
                part.add_header('Content-Disposition', 'attachment', filename=os.path.basename(attach_path))
                msg.attach(part)
        return msg
            

    def send_email_attach(self, subject, body, to_email, attach_path):
        msg = MIMEMultipart()
        msg['From'] = self.username
        msg['To'] = to_email
        msg['Subject'] = subject

        msg.attach(MIMEText(body, 'plain'))
        self.manage_attach(msg, attach_path)
        try:
            self.mail.sendmail(self.username, to_email, msg.as_string())
            print(f"Email with attachment sent to {to_email}")
            return True
        except Exception as e:
            print(f"Failed to send email: {str(e)}")
            return False
        
    def send_email_with_reply_to(self, subject, body, to_email, reply_to):
        msg = MIMEMultipart()
        msg['From'] = self.username
        msg['To'] = to_email
        msg['Subject'] = subject
        msg.add_header('Reply-To', reply_to)

        msg.attach(MIMEText(body, 'plain'))

        try:
            self.mail.sendmail(self.username, to_email, msg.as_string())
            print(f"Email sent to {to_email} with Reply-To header")
            return True
        except Exception as e:
            print(f"Failed to send email: {str(e)}")
            return False
        
    def send_email_multi_attach(self, subject, body, to_email, attachments=None):
        msg = MIMEMultipart()
        msg['From'] = self.username
        msg['To'] = to_email
        msg['Subject'] = subject

        msg.attach(MIMEText(body, 'plain'))

        if attachments:
            for attach_path in attachments:
                if os.path.isfile(attach_path):
                    self.manage_attach(msg, attach_path)
                else:
                    print(f"Warning: Attachment {attach_path} does not exist and was skipped.")

        try:
            self.mail.sendmail(self.username, to_email, msg.as_string())
            print(f"Email with {len(attachments) if attachments else 0} attachments sent to {to_email}")
            return True
        except Exception as e:
            print(f"Failed to send email with multiple attachments: {str(e)}")
            return False
