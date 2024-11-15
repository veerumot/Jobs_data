import csv
import psycopg2
from datetime import date
import os

# Database connection details
DB_NAME = os.environ.get('DB_NAME')
DB_USER = os.environ.get('DB_USER')
DB_PASS = os.environ.get('DB_PASS')
DB_HOST = os.environ.get('DB_HOST')
DB_PORT = os.environ.get('DB_PORT')

# CSV file details
csv_file = 'data.csv'
# table_name = 'time_data'
Today_date = date.today()

# Connect to the database
conn = psycopg2.connect(
    host=DB_HOST,
    database=DB_NAME,
    user=DB_USER,
    password=DB_PASS
)
cur = conn.cursor()

# Read the CSV file
with open(csv_file, 'r') as f:
    reader = csv.reader(f)
    next(reader)  # Skip the header row if it exists
    # print(next(reader))
    for row in reader:
        month_jobs = row[0]
        week_jobs = row[1]
        day_jobs = row[2]
        print(month_jobs , week_jobs , day_jobs)
        query = """
                    INSERT INTO time_data (date, month_jobs, week_jobs, day_jobs)
                    VALUES (%s, %s, %s, %s)
                """
        cur.execute(query, (Today_date, month_jobs, week_jobs, day_jobs))
        conn.commit()
    cur.close()
    conn.close()
