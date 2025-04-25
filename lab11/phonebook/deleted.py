import psycopg2
from config import load_config


def delete_contact(first_name):
    """ Delete part by part id """

    sql = 'DELETE FROM contacts WHERE first_name = %s'
    config = load_config()

    try:
        with  psycopg2.connect(**config) as conn:
            with  conn.cursor() as cur:
                cur.execute(sql, (first_name,))
            conn.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
        
def delete_by_phone(phone_number):
    config = load_config()

    try:
        with psycopg2.connect(**config) as conn:
            with conn.cursor() as cur:
                cur.execute(
                    "SELECT contact_id FROM phone_numbers WHERE phone_number = %s",
                    (phone_number,)
                )
                contact_ids = [row[0] for row in cur.fetchall()]

                if not contact_ids:
                    return

                cur.execute(
                    "DELETE FROM phone_numbers WHERE phone_number = %s",
                    (phone_number,)
                )

                for contact_id in contact_ids:
                    cur.execute(
                        "SELECT 1 FROM phone_numbers WHERE contact_id = %s LIMIT 1",
                        (contact_id,)
                    )
                    if not cur.fetchone():
                        cur.execute(
                            "DELETE FROM contacts WHERE contact_id = %s",
                            (contact_id,)
                        )

            conn.commit()

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    

if __name__ == '__main__':
    
    #delete_contact("Bake")
    
    delete_by_phone("+77777777777")
