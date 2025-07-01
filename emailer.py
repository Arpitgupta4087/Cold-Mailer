import smtplib
import pandas as pd
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


def send_bulk_emails(sender_email, sender_password, subject, body, file_path):
    try:

        if file_path.name.endswith(".csv"):
            df = pd.read_csv(file_path)
        else:
            df = pd.read_excel(file_path)

        if "email" not in df.columns:
            return " No 'Email' column found in the file."

        recipients = df["Email"].dropna().unique()


        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(sender_email, sender_password)

        for recipient in recipients:
            msg = MIMEMultipart()
            msg["From"] = sender_email
            msg["To"] = recipient
            msg["Subject"] = subject

            msg.attach(MIMEText(body, "plain"))

            server.send_message(msg)

        server.quit()
        return f"Emails sent successfully to {len(recipients)} recipients."

    except Exception as e:
        return f"Error: {str(e)}"
