import os

""" HERE IT'S DEFINED ALL ENVIRONMENT VARIABLES """

# The default values are not related to default docker container environment variables values
POSTGRES_DB_HOST = os.getenv('POSTGRES_DB_HOST','')
POSTGRES_DB_USER = os.getenv('POSTGRES_DB_USER','')
POSTGRES_DB_PWD = os.getenv('POSTGRES_DB_PWD','')

POSTGRES_TABLE_NAME = 'trips'
INGESTION_FILE_PATH = "/data/landing"
INGESTION_PROCESSED_PATH = "/data/processed"

# Only works with GMAIL Protocol
NOTIFICATION_EMAIL_USER_LOGIN = os.getenv('NOTIFICATION_EMAIL_USER_LOGIN','')
NOTIFICATION_EMAIL_USER_PWD = os.getenv('NOTIFICATION_EMAIL_USER_PWD','')


