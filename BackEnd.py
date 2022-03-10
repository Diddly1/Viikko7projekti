import psycopg2
import datetime
import smtplib
from email.message import EmailMessage
import time

def puuttuuko_tyoaikoja(lista: list):

    projektiinLiitetyt = ['Ville', 'Anna', 'Mike', 'Pietari']
    projektiinLiitetyt.sort(key = len)
    lista.sort(key = len)

    kirjaus_puuttuu = []

    for arvo in lista:
        if arvo[1] not in projektiinLiitetyt:
            kirjaus_puuttuu.append(arvo[1])

    return kirjaus_puuttuu

def haeSarakkeet(cursor, con):  
    
    #aloitus = time.strftime("%Y-%m-%d 00:00:00")
    #lopetus = time.strftime("%Y-%m-%d 23:59:59")

    aloitus = '2022/10/10 00:00:00'
    lopetus = '2022/10/10 23:59:59'

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

   

    with open("tyoaikaraportti.txt", "w") as tiedosto:
        for i in rivit:
            rivi = f'Koodari: {str(i[0])} {str(i[1])}\naloittanut: {str(i[2])}\nlopettanut: {str(i[3])}\nTunteja: {i[3]-i[2]}\n\nProjektissa: {str(i[4])}\nSelvitys: {str(i[5])}\nUlkoilma koodauksen aikana: {str(i[6])}\n\n=================================\n\n'
            tiedosto.write(rivi)
        tiedosto.write(f'Kokonaistunnit: {str(summa)}')

        if len(puuttuvat) != 0:
            tiedosto.write(f'\n\nTyöaikoja puuttuu:\n\n')
            for i in puuttuvat:
                tiedosto.write(f'{i}\n')    

    laheta_sahkoposti()

def laheta_sahkoposti():
    
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
    with open("./ignore.txt", 'r') as file:
        lines = [line.rstrip() for line in file]
    pw = lines[0]

    con = None
    try:
        con = psycopg2.connect("dbname=tyotunnit user=postgres password = {}".format(pw))
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
    db_connection()           