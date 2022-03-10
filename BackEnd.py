from webbrowser import Konqueror
import psycopg2
import datetime
import smtplib
from email.message import EmailMessage
import time

def puuttuuko_tyoaikoja(lista: list):

    projektiinLiitetyt = ['Ville', 'Anna', 'Mike', 'Pietari']
    nimet = []
    kirjaus_puuttuu = []
    
    for arvo in lista:
        nimet.append(arvo[1])

    for arvo in projektiinLiitetyt:
        if arvo not in nimet:
            kirjaus_puuttuu.append(arvo)

    return kirjaus_puuttuu

def haeSarakkeet(cursor, con):
    print("Haetaan työaikoja...")
    
    aloitus = time.strftime("%Y-%m-%d 00:00:00")
    lopetus = time.strftime("%Y-%m-%d 23:59:59")

    SQL = "select * from tyo_taulu where alku between %s and %s"
    data = (aloitus, lopetus)
    cursor.execute(SQL, data)
    row = cursor.fetchall()

    aikalista = []

    for rivi in row:
        aikalista.append(rivi[3] - rivi[2])
    
    mysum = datetime.timedelta()
    for i in aikalista:
        s = i.total_seconds()
        d = datetime.timedelta(seconds=int(s))
        mysum += d

    puuttuuko_tyoaikoja(row)
    kirjoitaRaportti(mysum, row, puuttuuko_tyoaikoja(row))


def kirjoitaRaportti(summa: datetime.timedelta(), rivit: list, puuttuvat: list):
    print("Kirjoitetaan raportti...")

    with open("tyoaikaraportti.txt", "w") as tiedosto:
        for i in rivit:
            rivi = f'Koodari: {str(i[0])} {str(i[1])}\naloittanut: {str(i[2])}\nlopettanut: {str(i[3])}\nTunteja: {i[3]-i[2]}\n\nProjektissa: {str(i[4])}\nSelvitys: {str(i[5])}\nUlkoilma koodauksen aikana: {str(i[6])}\n\n=================================\n\n'
            tiedosto.write(rivi)
        tiedosto.write(f'Kokonaistunnit: {str(summa)}')

        if len(puuttuvat) != 4:
            tiedosto.write(f'\n\nTyöaikoja puuttuu:\n\n')
            for i in puuttuvat:
                tiedosto.write(f'{i}\n')    

    laheta_sahkoposti()

def laheta_sahkoposti():
    print("Lähetetään sähköposti...")
    with open("./ignore.txt", 'r') as file:
        lines = [line.rstrip() for line in file]
    pw = lines[1]
    
    with open("tyoaikaraportti.txt") as fp:
        msg = EmailMessage()
        msg['From'] = "linna.anna@gmail.com"
        msg['To'] = "ville.jouhten@saunalahti.fi"
        msg['Subject'] = 'Työaikaraportti'
        msg.set_content(fp.read())
      

    server = smtplib.SMTP('smtp.gmail.com', 587) 
    server.starttls()
    server.login("waffeloine@gmail.com", pw)
    server.sendmail("linna.anna@gmail.com", "ville.jouhten@saunalahti.fi", msg.as_string())

    server.quit() 

def db_connection():
    con = None
    try:
        sslmode = "require"
        conn_string = "host={0} user={1} dbname={2} password={3} sslmode={4}".format(host, user, dbname, password, sslmode)

        con = psycopg2.connect(conn_string) 
        print("Connection established")
        cursor = con.cursor()
        con.commit()
        haeSarakkeet(cursor, con)
        cursor.close()
        con.close()

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if con is not None:
            con.close()


if __name__ == "__main__":
    
    with open("DBfiles/DBignore.txt", 'r') as file:
        lines = [line.rstrip() for line in file]
    password = lines[0]
    host = lines[1]
    user = lines[2]
    dbname = "tyotunnit_db"

    db_connection()
