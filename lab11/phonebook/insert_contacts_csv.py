import psycopg2
import csv
from config import load_config

def import_csv(file_path):
    config = load_config()
    contact_sql = "INSERT INTO contacts(first_name) VALUES(%s) RETURNING contact_id"
    phone_sql = "INSERT INTO phone_numbers (contact_id, phone_number) VALUES (%s, %s)"

    try:
        with psycopg2.connect(**config) as conn:
            with conn.cursor() as cur:
                with open(file_path, newline='') as csvfile:
                    reader = csv.DictReader(csvfile)
                    for row in reader:
                        first_name = row['first_name']
                        phone_number = row['phone_number']
                        cur.execute(contact_sql, (first_name,))
                        rows = cur.fetchone()
                        if rows:
                            contact_id = rows[0]
                            
                        cur.execute(phone_sql, (contact_id, phone_number))
            conn.commit()
            
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)

if __name__ == '__main__':
    import_csv("contacts.csv")