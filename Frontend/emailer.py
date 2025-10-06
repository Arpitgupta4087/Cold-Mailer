import smtplib
import pandas as pd
from email.message import EmailMessage

def send_bulk_emails(sender_email, sender_password, subject, body, excel_file, attachment_file=None):
    try:

        if excel_file.name.endswith(".csv"):
            df = pd.read_csv(excel_file)
        else:
            df = pd.read_excel(excel_file)

        if "Email" not in df.columns:
            return "❌ Missing 'Email' column in uploaded file."

        for email in df["Email"].dropna():
            msg = EmailMessage()
            msg["Subject"] = subject
            msg["From"] = sender_email
            msg["To"] = email
            msg.set_content(body)


            if attachment_file:
                filename = attachment_file.name
                file_data = attachment_file.read()
                msg.add_attachment(file_data, maintype="application", subtype="pdf", filename=filename)


            with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
                smtp.login(sender_email, sender_password)
                smtp.send_message(msg)

        return f"✅ Emails sent to {len(df)} recipients."

    except Exception as e:
        return f"❌ Error: {str(e)}"
