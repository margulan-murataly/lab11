import psycopg2
from config import load_config

def get_contacts():
    """ Retrieve data from the contacts table """
    config  = load_config()
    try:
        with psycopg2.connect(**config) as conn:
            with conn.cursor() as cur:
                
                #cur.execute("SELECT contact_id, first_name FROM contacts ORDER BY first_name")
                
                #cur.execute("SELECT contact_id, first_name FROM contacts ORDER BY contact_id")
                
                #cur.execute("SELECT contact_id, first_name FROM contacts WHERE contact_id > 5")
                
                #cur.execute("SELECT * FROM contacts WHERE first_name LIKE 'M%';")
                
                #cur.execute("SELECT c.first_name FROM contacts c JOIN phone_numbers p ON c.contact_id = p.contact_id WHERE p.phone_number = '+77777777777';")
                
                cur.execute("""SELECT
                                contacts.contact_id,
                                contacts.first_name,
                                phone_numbers.phone_id,
                                phone_numbers.phone_number
                            FROM contacts
                            LEFT JOIN phone_numbers
                                ON contacts.contact_id = phone_numbers.contact_id
                            ORDER BY contacts.contact_id;""")
                
                #print("The number of parts: ", cur.rowcount)
                row = cur.fetchone()

                while row is not None:
                    print(row)
                    row = cur.fetchone()

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)

if __name__ == '__main__':
    print("(contact_id|first_name|phone_id|phone_number)")
    get_contacts()