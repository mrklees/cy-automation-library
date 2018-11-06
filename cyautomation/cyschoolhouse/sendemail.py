import smtplib
from configparser import ConfigParser
from pathlib import Path

def send_email(to_addrs, subject, body):
    creds_path = str(Path(__file__).parent / 'credentials.ini')
    
    config = ConfigParser()
    config.read(creds_path)
    
    username = config['Single Sign On']['user']
    password = config['Single Sign On']['pass']
    
    if '@cityyear.org' not in username:
        username += '@cityyear.org'
   
    mailserver = smtplib.SMTP('smtp.office365.com',587)
    mailserver.ehlo()
    mailserver.starttls()
    mailserver.login(username, password)
    msg = f'''From: {username}\nSubject: {subject}\n\n{body}'''
    mailserver.sendmail(from_addr=username, to_addrs=to_addrs, msg=msg)
    mailserver.quit()
