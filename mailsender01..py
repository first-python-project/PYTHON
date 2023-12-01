import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import os
import zipfile

def send_email_with_attachment():
    sender_email = "boanproject1234@naver.com"
    receiver_email = "pricep@naver.com"
    subject = "압축 된 파일입니다"
    body = "압축된 파일"

    zip_file_name = "compress.zip"
    upload_folder = "uploads"

    zip_file_path = os.path.join(upload_folder, zip_file_name)
    with zipfile.ZipFile(zip_file_path, 'w') as zipf:
        for file in os.listdir(upload_folder):
            file_path = os.path.join(upload_folder, file)
            zipf.write(file_path, os.path.basename(file_path))

    smtp_server = "smtp.naver.com"
    smtp_port = 587
    smtp_username = "boanproject1234@naver.com"
    smtp_password = "!Qhdkscjfwj@"

    message = MIMEMultipart()
    message['From'] = sender_email
    message['To'] = receiver_email
    message['Subject'] = subject
    message.attach(MIMEText(body, 'plain'))

    with open(zip_file_path, 'rb') as attachment:
        base = MIMEBase('application', 'zip')
        base.set_payload(attachment.read())
        encoders.encode_base64(base)
        base.add_header('Content-Disposition', 'attachment', filename=zip_file_name)
        message.attach(base)

    with smtplib.SMTP(smtp_server, smtp_port) as server:
        server.starttls()
        server.login(smtp_username, smtp_password)
        server.sendmail(sender_email, receiver_email, message.as_string())

    
    os.remove(zip_file_path)

send_email_with_attachment()