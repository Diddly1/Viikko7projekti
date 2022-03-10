import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

#DBcode contains (SQL statement,target database)
def runDBcode(host, user, password, DBcode):
    #Db info
    SQL,dbname = DBcode
    sslmode = "require"
    # Construct connection string
    conn_string = "host={0} user={1} dbname={2} password={3} sslmode={4}".format(host, user, dbname, password, sslmode)

    #Db connect and execute SQL code
    con = None
    try:
        con = psycopg2.connect(conn_string) 
        print("Connection established")
        con.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        cursor = con.cursor()

        cursor.execute(SQL)

        con.commit()
        cursor.close()
        con.close()
        print("Executed SQL code")
        print()

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if con is not None:
            con.close()

#returns SQL statement and target database
def create_db(newDBname):
    SQL = "CREATE DATABASE {};".format(newDBname)
    print('Running CREATE DATABASE')
    return SQL,"postgres"

#returns SQL statement and target database
def create_table(DBname,tablename):
    SQLtable_init ="CREATE TABLE {} (\
        id              SERIAL PRIMARY KEY, \
        nimi            varchar(255) NOT NULL, \
        alku            TIMESTAMP NOT NULL, \
        loppu           TIMESTAMP NOT NULL, \
        projekti_nimi   varchar(255) NOT NULL, \
        selite          varchar NOT NULL,\
        lampotila       DECIMAL(5,2)\
        );".format(tablename)
    print('Running CREATE TABLE')
    return SQLtable_init,DBname


if __name__ == '__main__':

    dbname = "tyotunnit_db"
    dbname.lower()
    tablename = "tyo_taulu"
    tablename.lower()

    #Db connection info
    with open("DBfiles/DBignore.txt", 'r') as file:
        lines = [line.rstrip() for line in file]
    password = lines[0]
    host = lines[1]
    user = lines[2]

    runDBcode(host,user,password,create_db(dbname))
    runDBcode(host,user,password,create_table(dbname,tablename))