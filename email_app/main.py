from emails import EmailFetcher, EmailDownloader, EmailSender
import credentials as cr

class EmailClientApp:
    def __init__(self):
        self.username = cr.EMAIL
        self.running = True
        self.options = {
            "1": self.fetch_emails_imap,
            "2": self.fetch_emails_pop3,
            "3": self.download_unread_attachment,
            "4": self.send_simple_email,
            "5": self.send_email_with_attachment,
            "6": self.send_email_with_multi_attachments,
            "7": self.send_email_with_reply_to,
            "0": self.exit_program
        }

    def print_menu(self):
        print("\n\033[95m Choose an option: \033[0m")
        print("1. Fetch 10 Emails Using IMAP")
        print("2. Fetch 10 Emails Using POP3")
        print("3. Download unread email with attachment (IMAP only)")
        print("4. Send simple email")
        print("5. Send email with attachment")
        print("6. Send email with multiple attachments")
        print("7. Send email with Reply-To")
        print("0. Exit")

    def fetch_emails_imap(self):
        client = EmailFetcher(self.username, "IMAP")
        client.login()
        emails = client.fetch_emails(limit=10)
        print("\n\033[92m Latest 10 Emails (IMAP): \033[0m")
        for subject in emails:
            print(subject)
        client.close()

    def fetch_emails_pop3(self):
        client = EmailFetcher(self.username, "POP3")
        client.login()
        emails = client.fetch_emails(limit=10)
        print("\n\033[92m Latest 10 Emails (POP3): \033[0m")
        for subject in emails:
            print(subject)
        client.close()

    def download_unread_attachment(self):
        client = EmailDownloader(self.username, "IMAP")
        client.login()
        target_subject = input("\n\033[95m Enter the subject to search for in UNREAD emails: \033[0m")
        attachment_path, email_path = client.download_email_attach(target_subject)
        if attachment_path and email_path:
            print("\033[32m Email and attachment saved successfully at: \033[0m", email_path, attachment_path)
        else:
            print("\033[31m No matching unread email with attachment found. \033[0m")
        client.close()

    def send_simple_email(self):
        client = EmailSender(self.username)
        client.login()
        to_email = input("Enter recipient email: ")
        subject = input("Enter subject: ")
        body = input("Enter body: ")
        client.send_email_txt(subject, body, to_email)
        client.close()

    def send_email_with_attachment(self):
        client = EmailSender(self.username)
        client.login()
        to_email = input("Enter recipient email: ")
        subject = input("Enter subject: ")
        body = input("Enter body: ")
        attach_path = input("Enter path to attachment: ")
        client.send_email_attach(subject, body, to_email, attach_path)
        client.close()

    def send_email_with_reply_to(self):
        client = EmailSender(self.username)
        client.login()
        to_email = input("Enter recipient email: ")
        subject = input("Enter subject: ")
        body = input("Enter body: ")
        reply_to = input("Enter Reply-To email: ")
        client.send_email_with_reply_to(subject, body, to_email, reply_to)
        client.close()

    def send_email_with_multi_attachments(self):
        client = EmailSender(self.username)
        client.login()
        to_email = input("Enter recipient email: ")
        subject = input("Enter subject: ")
        body = input("Enter body: ")
        attach_paths = input("Enter paths to attachments separated by commas: ").split(',')
        attach_paths = [path.strip() for path in attach_paths]
        client.send_email_multi_attach(subject, body, to_email, attach_paths)
        client.close()

    def exit_program(self):
        print("\033[94m Goodbye! \033[0m")
        self.running = False

    def run(self):
        while self.running:
            self.print_menu()
            choice = input("\n\033[95m Enter your choice: \033[0m").strip()
            action = self.options.get(choice)
            if action:
                action()
            else:
                print("\033[91m Invalid choice. Please select a valid option. \033[0m")

if __name__ == "__main__":
    app = EmailClientApp()
    app.run()
