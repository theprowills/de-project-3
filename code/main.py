import psycopg2
import csv
# Koneksi ke postgresql
conn = psycopg2.connect("host=localhost dbname=postgres user=postgres password=admin")

# Menggunakan kursor dan eksekusi query
cur = conn.cursor()

# cur.execute("""
# CREATE TABLE IF NOT EXISTS regions(
#             postalZip TEXT,
#             region TEXT,
#             country TEXT)
# """)

cur.execute("""
CREATE TABLE IF NOT EXISTS users(
            id SERIAL PRIMARY KEY,
            email TEXT,
            name TEXT,
            phone TEXT,
            postalZip TEXT)
""")
conn.commit()
cur.execute("SELECT postalZip FROM users")

# Memasukan data dari csv menggunakan METHOD execute - CARA 1
# with open('source/users_w_postal_code.csv') as f:
#     csv_reader = csv.reader(f, delimiter=',')
#     next(csv_reader) # skip baris pertama (header)
#     for row in csv_reader:
#         cur.execute('INSERT INTO users VALUES (default, %s, %s, %s, %s ) ON CONFLICT DO NOTHING', row)
    
# conn.commit()

# Memasukan data dari csv menggunakan METHOD copy_from- CARA 2
# with open('source/users_w_postal_code.csv') as f:
#     next(f) # skip baris pertama (header)
#     cur.copy_from(f, 'users', sep=',', columns=('email', 'name', 'phone', 'postalzip')) 
#     #Note: postgres otomatis meng-lowercase-kan jika tidak apit dengan kutip dua, jadi panggil postalzip dengan huruf kecil semua

# conn.commit()

# Memasukan data dari csv menggunakan METHOD to_sql - CARA 3
# import pandas as pd
# from sqlalchemy import create_engine
# df = pd.read_csv("source/users_w_postal_code.csv", sep=',')

# # create_engine membutuhkan parameter URL (database URL), "postgresql://user:password@host:port/database_name". Sesuaikan dengan database yang anda gunakan.
# engine = create_engine("postgresql://postgres:admin@127.0.0.1:5432/postgres")
# df.to_sql("from_table_file", engine, if_exists='replace')

# conn.commit()

# Memasukan data dari csv menggunakan METHOD - CARA 4
import pandas as pd
from sqlalchemy import create_engine
df = pd.read_csv("source/users_w_postal_code.csv", sep=',')
engine = create_engine("postgresql://postgres:admin@127.0.0.1:5432/postgres")
df.to_sql("from_table_file", engine, if_exists='replace')
df_read = pd.read_sql("SELECT * FROM from_table_file", engine)

# Menampilkan hasil
cur.execute("SELECT * FROM users")
one = cur.fetchone()
all = cur.fetchall()
print(one)

