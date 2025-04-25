import psycopg2
from config import load_config
    
def insert_many_contacts(contact_list):
    """ Insert multiple contacts into the contacts table  """

    contact_sql = "INSERT INTO contacts(first_name) VALUES(%s) RETURNING contact_id"
    phone_sql = "INSERT INTO phone_numbers (contact_id, phone_number) VALUES (%s, %s)"
    config = load_config()
    try:
        with  psycopg2.connect(**config) as conn:
            with  conn.cursor() as cur:
                for first_name, phone_number in contact_list:
                    cur.execute(contact_sql, (first_name,))
                    rows = cur.fetchone()
                    if rows:
                        contact_id = rows[0]

                    cur.execute(phone_sql, (contact_id, phone_number))
                
            conn.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)


if __name__ == '__main__':
    
    contacts = [
    ('Sake', '+77077170770'),
    ('Bake', '+77777077007'),
    ('Ereke', '+77011017171'),
    ('Make', '+77177771771'),
    ('Nureke', '+77777777777'),
    ('Edik', '+34343443'),
    ('Medik', '6060+00')
]
    
    def valid_phone(phone):
        return phone.startswith('+7') and len(phone) == 12 and phone[2:].isdigit()
        
    valid_contacts = []

    for name, phone in contacts:
        if valid_phone(phone):
            valid_contacts.append((name, phone))
        else:
            print(f"Invalid: {name}, {phone}")
        
    insert_many_contacts(valid_contacts)