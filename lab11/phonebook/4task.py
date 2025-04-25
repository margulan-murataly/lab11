import psycopg2
from config import load_config

def get_contacts_paginated(limit, offset):
    config = load_config()
    results = []

    try:
        with psycopg2.connect(**config) as conn:
            with conn.cursor() as cur:
                cur.execute(
                    "SELECT contact_id, first_name FROM contacts ORDER BY first_name LIMIT %s OFFSET %s",
                    (limit, offset)
                )
                results = cur.fetchall()

    except (Exception, psycopg2.DatabaseError) as error:
        print("Error:", error)

    return results

if __name__ == '__main__':
    page = 2
    page_size = 5
    offset = (page - 1) * page_size

    contacts = get_contacts_paginated(limit=page_size, offset=offset)
    for row in contacts:
        print(row)