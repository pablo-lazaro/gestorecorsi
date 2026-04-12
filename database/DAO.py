from database.DB_connect import DBConnect
from model.corso import Corso
from model.studente import Studente

# Listone di metodi che faranno le query al databas

class DAO():

    """CI DARANNO SEMPRE UNO DI QUESTI ESEMPI GIA FATTI
    I MODO DA FARE COPIA INCOLLA"""
    @staticmethod
    def getCodins(): # Il dao non potendo piu delegare deve fare la query
        cnx = DBConnect.get_connection()
        cursor = cnx.cursor(dictionary=True)

        query = """select codins 
                    FROM corso"""

        cursor.execute(query)

        res = []
        for row in cursor:
            res.append(row["codins"])


        cursor.close()
        cnx.close()
        return res

    @staticmethod
    def getAllCorsi():
        cnx = DBConnect.get_connection()
        cursor = cnx.cursor(dictionary=True)

        query = """select * FROM corso"""

        cursor.execute(query)

        res = []
        for row in cursor:

            # Dovro fare l'append di un oggetto corso, quindi dovrò crearmi il DTO Corso (perche?)
            res.append(Corso(
                codins = row["codins"],
                crediti = row["crediti"],
                nome = row["nome"],
                pd = row["pd"]
            ))


        cursor.close()
        cnx.close()
        return res # Viene restituita una lista di oggetti di tipo corso

    @staticmethod
    def getCorsiPD(pd):
        cnx = DBConnect.get_connection()
        cursor = cnx.cursor(dictionary=True)

        query = """SELECT *
                    FROM corso c
                    WHERE c.pd = %s""" # %s è un parametro

        cursor.execute(query, (pd,))  # Quando chiameremo questa query dovremmo avere un parametro in input

        res = []
        for row in cursor:
            res.append(Corso(**row)) # Il ** fa l'unpack del dizionario e passa ad ogni proprietà di quell'oggetto l'equivalente valore la cui chiave è la stessa

        cursor.close()
        cnx.close()
        return res

    @staticmethod
    def getCorsiPDwIscritti(pd):
        cnx = DBConnect.get_connection()
        cursor = cnx.cursor(dictionary=True)

        query = """select c.codins , c.crediti , c.nome , c.pd , count(*) as n
                    from corso c, iscrizione i
                    where c.codins = i.codins 
                    and c.pd = %s
                    group by c.codins , c.crediti , c.nome , c.pd """

        cursor.execute(query, (pd,))

        res = []
        for row in cursor:
            res.append((Corso(codins=row["codins"],
                              crediti=row["crediti"],
                              nome=row["nome"],
                              pd=row["pd"]),
                        row["n"])) # Devo immaginarmi questo come una tabella nuova, con il count ho creato una nuova colonna

        cursor.close()
        cnx.close()
        return res

    @staticmethod
    def getStudentiCorso(codins):
        cnx = DBConnect.get_connection()
        cursor = cnx.cursor(dictionary=True)

        query = """SELECT s.*
                   FROM studente s, \
                        iscrizione i
                   WHERE s.matricola = i.matricola
                     and i.codins = %s"""

        cursor.execute(query, (codins,))

        res = []
        for row in cursor:
            res.append(Studente(**row))

        cursor.close()
        cnx.close()
        return res

    @staticmethod
    def getCDSofCorso(codins):
        cnx = DBConnect.get_connection()
        cursor = cnx.cursor(dictionary=True)

        query = """SELECT s.CDS, count(*) as n
                   FROM studente s, \
                        iscrizione i
                   WHERE s.matricola = i.matricola
                     and i.codins = %s
                     and s.CDS != ""
                   group by s.CDS """

        cursor.execute(query, (codins,))

        res = []
        for row in cursor:
            res.append((row["CDS"], row["n"]))

        cursor.close()
        cnx.close()
        return res