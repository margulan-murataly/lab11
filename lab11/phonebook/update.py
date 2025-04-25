import psycopg2
from config import load_config


def update_contact(contact_id, first_name):
    """ Update contact name based on the contact id """

    updated_row_count = 0

    sql = """ UPDATE contacts
                SET first_name = %s
                WHERE contact_id = %s"""

    config = load_config()

    try:
        with  psycopg2.connect(**config) as conn:
            with  conn.cursor() as cur:

                cur.execute(sql, (first_name, contact_id))
                updated_row_count = cur.rowcount

            conn.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        return updated_row_count
    
def update_phone_num(phone_id, phone_number):
    """ Update vendor name based on the vendor id """

    updated_row_count = 0

    sql = """ UPDATE phone_numbers
                SET phone_number = %s
                WHERE phone_id = %s"""

    config = load_config()

    try:
        with  psycopg2.connect(**config) as conn:
            with  conn.cursor() as cur:

                cur.execute(sql, (phone_number, phone_id))
                updated_row_count = cur.rowcount

            conn.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        return updated_row_count

if __name__ == '__main__':
    update_contact(1, "Zaaakeee")
    update_phone_num(1, "+900909090")