import smtplib
from email.message import EmailMessage
import os
from dotenv import load_dotenv

load_dotenv()

def send_verification_email(email_to: str, token: str):
    mail_server = os.getenv("MAIL_SERVER")
    mail_port = os.getenv("MAIL_PORT")
    mail_user = os.getenv("MAIL_USERNAME")
    mail_pass = os.getenv("MAIL_PASSWORD")

    if not all([mail_server, mail_port, mail_user, mail_pass]):
        print("ERRO: Verifique se todas as variáveis SMTP estão no seu arquivo .env")
        print(f"Server: {mail_server}, Port: {mail_port}, User: {mail_user}")
        return

    msg = EmailMessage()
    verify_url = f"http://localhost:8000/verify?token={token}"
    msg.set_content(f"Olá! Por favor, verifique seu e-mail clicando no link: {verify_url}")
    msg["Subject"] = "Verifique sua conta"
    msg["From"] = "noreply@seusistema.com"
    msg["To"] = email_to

    try:
        server = smtplib.SMTP(mail_server, int(mail_port))
        server.starttls() 
        server.login(mail_user, mail_pass)
        server.send_message(msg)
        server.quit()
        print(f"E-mail enviado com sucesso para {email_to}")
    except Exception as e:
        print(f"Erro ao enviar e-mail: {e}")