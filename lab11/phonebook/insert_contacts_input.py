import psycopg2
from config import load_config


def insert_contact(first_name, phone_number):
    """ Insert a new contact into the contacts table """

    sql = """INSERT INTO contacts(first_name)
             VALUES(%s) RETURNING contact_id;"""

    contact_id = None
    config = load_config()

    try:
        with  psycopg2.connect(**config) as conn:
            with  conn.cursor() as cur:  
                cur.execute(sql, (first_name,))

                rows = cur.fetchone()
                if rows:
                    contact_id = rows[0]
                    
                cur.execute(
                    "INSERT INTO phone_numbers (contact_id, phone_number) VALUES (%s, %s)",
                    (contact_id, phone_number)
                )

                conn.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        return contact_id
    
def get_contacts():
    """ Retrieve data from the contacts table """
    config  = load_config()
    a = []
    try:
        with psycopg2.connect(**config) as conn:
            with conn.cursor() as cur:
                
                cur.execute("SELECT first_name FROM contacts")
                
                #print("The number of parts: ", cur.rowcount)
                row = cur.fetchone()

                while row is not None:
                    a.append(row)
                    row = cur.fetchone()

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        return a
    
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
    
def get_phone_id_by_name(first_name):
    config = load_config()
    phone_id = None

    try:
        with psycopg2.connect(**config) as conn:
            with conn.cursor() as cur:
                cur.execute("""
                    SELECT pn.phone_id
                    FROM phone_numbers pn
                    JOIN contacts c ON pn.contact_id = c.contact_id
                    WHERE c.first_name = %s
                """, (first_name,))
                row = cur.fetchone()
                if row:
                    phone_id = row[0]
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        return phone_id
    


if __name__ == '__main__':
    
    first_name = input("Enter first name: ")
    phone_number = input("Enter phone number: ")

    a = get_contacts()
    
    names = [row[0] for row in a]
    
    if first_name in names:
        
        phone_id = get_phone_id_by_name(first_name)
        
        if phone_id:
            update_phone_num(phone_id, phone_number)
        
    else:
        insert_contact(first_name, phone_number)
    