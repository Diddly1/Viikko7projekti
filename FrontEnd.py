import psycopg2
from datetime import datetime
import requests

def append_db(nimi,alku,loppu,projekti_nimi,selite,saa,cursor):
    SQL = "INSERT INTO tyo_taulu (nimi,alku,loppu,projekti_nimi,selite,lampotila) VALUES (%s,%s,%s,%s,%s,%s);"
    data = (nimi,alku,loppu,projekti_nimi,selite,saa)
    cursor.execute(SQL,data)

def tietokantayhteys(nimi,alku,loppu,projekti_nimi,selite,saa):

        with open("./ignore.txt", 'r') as file:
            lines = [line.rstrip() for line in file]
        pw = lines[0]

        con = None
        try:
            con = psycopg2.connect("dbname=tyotunnit user=postgres password = {}".format(pw))
            cursor = con.cursor()

            append_db(nimi,alku,loppu,projekti_nimi,selite, saa, cursor)

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
        
        # nimi = 'aikablöb'
        # alku = "2022/10/10 09:00"
        # loppu = "2022/10/10 16:00"
        # projekti_nimi = "vko07"
        # selite = "sää"
        # saa = str(get_weather())
        # print(saa)
        
        tietokantayhteys(nimi,alku,loppu,projekti_nimi,selite,saa)
        

if __name__ == "__main__":
    kayttoliittyma()