import psycopg2
from datetime import datetime
import requests

def append_db(nimi,alku,loppu,projekti_nimi,selite,saa,cursor):
    SQL = "INSERT INTO tyo_taulu (nimi,alku,loppu,projekti_nimi,selite,lampotila) VALUES (%s,%s,%s,%s,%s,%s);"
    data = (nimi,alku,loppu,projekti_nimi,selite,saa)
    cursor.execute(SQL,data)

def tietokantayhteys(nimi,alku,loppu,projekti_nimi,selite,saa):

        con = None
        try:
            sslmode = "require"
            conn_string = "host={0} user={1} dbname={2} password={3} sslmode={4}".format(host, user, dbname, password, sslmode)

            con = psycopg2.connect(conn_string) 
            cursor = con.cursor()

            append_db(nimi,alku,loppu,projekti_nimi,selite, saa, cursor)
            print()
            print("Työtuntisi on kirjattu tietokantaan")
            print()

            con.commit()
            cursor.close()
            con.close()

        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
        finally:
            if con is not None:
                con.close()

def get_weather():
    
    with open("./ignore.txt", 'r') as file:
        lines = [line.rstrip() for line in file]
    apikey = lines[2]

    city = 'helsinki'

    url = 'http://api.openweathermap.org/data/2.5/weather?q={}&appid={}&units=metric'.format(city,apikey)
    res = requests.get(url)
    data = res.json()
    
    lampotila = str(data['main']['temp'])

    return lampotila

def kayttoliittyma():
    while (True):

        print("\n'Työajanhallinta v1.0'\n")

        nimi = input("Aloita syöttämällä käyttäjänimi: ")
        while (True):
            alkua = input("Aloitusaika YYYY/MM/DD HH:MM: ")
            try:
                alku = datetime.strptime(alkua, '%Y/%m/%d %H:%M')
            except:
                print("Virheellinen aikasyöte, tarkista formaatti (YYYY/MM/DD HH:MM)")
                continue
            break
  
        while (True):
            while(True):        
                loppua = input("Lopetusaika: YYYY/MM/DD HH:MM: ")

                try:
                    loppu = datetime.strptime(loppua, '%Y/%m/%d %H:%M')
                except:
                    print("Virheellinen aikasyöte, tarkista formaatti (YYYY/MM/DD HH:MM)")
                    continue
                break           

            if loppua < alkua:
                print("Lopetusaika ei saa olla aiemmin kuin aloitusaika.")
                continue
            elif loppua == alkua:
                print("Alku ja lopetusajat samat.")
            else:
                break

        projekti_nimi = input("projekti: ")
        selite = input("Tehdyt tehtävät: ")
        saa = str(get_weather())
        
        tietokantayhteys(nimi,alku,loppu,projekti_nimi,selite,saa)
        

if __name__ == "__main__":

    with open("DBfiles/DBignore.txt", 'r') as file:
        lines = [line.rstrip() for line in file]
    password = lines[0]
    host = lines[1]
    user = lines[2]
    dbname = "tyotunnit_db"
    kayttoliittyma()
    input("Paina Enter ja lopeta")
