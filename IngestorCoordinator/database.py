from config import *
from notification import EmailNotification

import os
import shutil
import logging


TABLE_DDL_SQL = f"""
    CREATE TABLE IF NOT EXISTS public.{POSTGRES_TABLE_NAME}(
        region             VARCHAR(25),
        origin_coord       VARCHAR(100),
        destination_coord  VARCHAR(100),
        datetime           TIMESTAMP WITHOUT TIME ZONE,
        datasource         VARCHAR(25)
    )
"""

DROP_TABLE_SQL = f"DROP TABLE IF EXISTS public.{POSTGRES_TABLE_NAME}"

def create_all_tables(conn):
    cur = conn.cursor()
    cur.execute(TABLE_DDL_SQL)
    cur.execute(f"SELECT create_hypertable('{POSTGRES_TABLE_NAME}','datetime')")
    cur.execute(f"ALTER TABLE public.{POSTGRES_TABLE_NAME} SET(timescaledb.compress,timescaledb.compress_segmentby = 'region')")

    conn.commit()
    print("Created Table from DDL: \n \n"  + TABLE_DDL_SQL)

def delete_all_tables(conn):
    cur = conn.cursor()
    cur.execute(DROP_TABLE_SQL)
    conn.commit()
    print("Dropped Table from DDL: \n \n"  + DROP_TABLE_SQL)

def load_into_table(conn, path):
    cur = conn.cursor()
    files = os.listdir(path)
    files_to_move = []

    print("Loading CSV Files has started")
    try:
        for file in files:
            full_path = path + '/' + file
            print(f"Processing File {full_path}")
            cur.execute(f"""
                COPY public.{POSTGRES_TABLE_NAME}
                FROM '{full_path}'
                DELIMITER ','
                CSV HEADER
            """)

            conn.commit()
            files_to_move.append(file)
    except BaseException as e:
        raise e
    finally:
        [shutil.move(f"{INGESTION_FILE_PATH}/{processed_file}",INGESTION_PROCESSED_PATH) for processed_file in files_to_move]
        if NOTIFICATION_EMAIL_USER_LOGIN is not None:
            notifier = EmailNotification()
            notifier.send({"files_to_ingest": files, "files_ingested": files_to_move})
            print(f"ETL Processed Finished. An Report will be sent to {NOTIFICATION_EMAIL_USER_LOGIN}")