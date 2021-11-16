from config import NOTIFICATION_EMAIL_USER_LOGIN, NOTIFICATION_EMAIL_USER_PWD, INGESTION_FILE_PATH, INGESTION_PROCESSED_PATH
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from datetime import datetime
from tabulate import tabulate

import abc
import smtplib
import ssl

class BaseNotification(metaclass=abc.ABCMeta):

    def __init__(self):
        pass
    
    @abc.abstractmethod
    def send(self,args):
        pass

class EmailNotification(BaseNotification):

    def __init__(self):
        self.EMAIL_PORT = 465
        self.EMAIL_USER_LOGIN = NOTIFICATION_EMAIL_USER_LOGIN
        self.EMAIL_USER_PWD = NOTIFICATION_EMAIL_USER_PWD

        print(self.EMAIL_USER_LOGIN)
        print(self.EMAIL_USER_PWD)

    def send(self,args):
        context = ssl.create_default_context()
        today   = datetime.now().date()
        files_to_ingest = set(args['files_to_ingest'])
        files_ingested  = set(args['files_ingested'])
        status = 'Success' if len(files_ingested) == len(files_to_ingest) else 'Failed'

        if status == "Failed":
            d = [[INGESTION_FILE_PATH,INGESTION_PROCESSED_PATH,file,'failed'] for file in files_to_ingest.difference(files_ingested)]
        else:
            d = [[INGESTION_FILE_PATH,INGESTION_PROCESSED_PATH,file,'success'] for file in files_ingested]
        
        body = tabulate(d,headers=["Source Path","Dest Path","File","Status"],tablefmt="pretty")

        with smtplib.SMTP_SSL("smtp.gmail.com", self.EMAIL_PORT, context=context) as server:
            # server.starttls()
            server.login(self.EMAIL_USER_LOGIN, self.EMAIL_USER_PWD)
            msg = MIMEMultipart()

            msg['From'] = self.EMAIL_USER_LOGIN
            msg['To'] = self.EMAIL_USER_LOGIN
            msg['Subject'] = f"ETL Report - {today}"

            msg.attach(MIMEText("This is an Automated Message to report summary of last ETL Job execution. \n" + body, 'plain'))
            server.sendmail(msg['From'], msg['To'], msg.as_string())
            server.quit()