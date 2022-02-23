import psycopg2

# https://pynative.com/python-cursor-fetchall-fetchmany-fetchone-to-read-rows-from-table/

#establishing the connection
conn = psycopg2.connect(
   database="nvd", user='postgres', password='tmddbs123', host='127.0.0.1', port= '5432'
)
#Creating a cursor object using the cursor() method
cursor = conn.cursor()

# COPY persons(first_name,last_name,email)
# TO 'C:\tmp\persons_partial_db.csv' DELIMITER ',' CSV HEADER;
command1 = "COPY training_final TO 'E:/training_final.csv' DELIMITER ',' CSV HEADER;"
command2 = "COPY testing_final TO 'E:/testing_final.csv' DELIMITER ',' CSV HEADER;"
# command3 = "COPY (SELECT cve, zdi_date, edb_date FROM edb_zdi WHERE zdi_date IS NOT NULL AND edb_date IS NOT NULL) TO 'E:/edb_zdi.csv' DELIMITER ',' CSV HEADER;"
command3 = "COPY (SELECT cve, zdi_date, edb_date, edb_date::DATE - zdi_date::DATE as date_diff FROM edb_zdi WHERE zdi_date IS NOT NULL AND edb_date IS NOT NULL) TO 'E:/edb_zdi.csv' DELIMITER ',' CSV HEADER;"
command4 = "COPY edb_zdi_samples TO 'E:/edb_zdi_samples.csv' DELIMITER ',' CSV HEADER;"

#Executing an MYSQL function using the execute() method
# cursor.execute("select version()")
cursor.execute(command4)

# Fetch a single row using fetchone() method.
# data = cursor.fetchone()
# print("Connection established to: ", data)

#Closing the connection
conn.close()
# Connection established to: ('PostgreSQL 11.5, compiled by Visual C++ build 1914, 64-bit',)
