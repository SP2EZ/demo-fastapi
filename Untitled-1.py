import os, platform
from datetime import datetime, timedelta
import psycopg
from psycopg import rows
#print (int(5 / 2))

print (os.getenv("MY_TEST_VAR"))
#print (f"OS name : {os.name}")
#print (f"Platform name : {platform.platform()}")

#check_type = ['hello', 1, 'there']
#print (type(check_type))

#print(f"UTCNOW - {datetime.utcnow()}\nNOW - {datetime.now()}")
#Epoch = datetime.utcnow().isoformat()
#datetime.now(timezone.utc)

#expiration = datetime.utcnow() + timedelta(minutes=30)
#expiration = expiration.timestamp()
#print(f"UTCNOW Epoch- {expiration}")
search = "dev"
search = "%"+search+"%"
with psycopg.connect(host='localhost', dbname='fastapi', user='postgres', password='p@s!gre&', port='5432', row_factory=rows.dict_row) as conn:
    with conn.cursor() as cur:
        #record = cur.execute(""" SELECT * FROM posts WHERE user_id = %s LIMIT %s OFFSET %s """, (8, 2, 0)).fetchall()
        record = cur.execute(""" SELECT * FROM posts WHERE user_id = %s AND title ILIKE %s LIMIT %s OFFSET %s """, (8, search, 2, 0)).fetchall()

print (f"Data from DB: \n{record}")